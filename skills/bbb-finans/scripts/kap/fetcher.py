"""KAP veri cekme - bildirimler, detay, profil, finansal."""

import json
import logging
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .client import KAPClient
from .models import (
    KAP_BASE, CATEGORIES, KAPCompanyProfile, KAPDetail, KAPDisclosure,
)
from .parser import (
    decode_rsc_chunks, fix_turkish_encoding, parse_attachments,
    parse_disclosure_detail, parse_disclosure_list,
    parse_kap_financial_page, parse_rsc_stream,
)

logger = logging.getLogger(__name__)


def _tr_lower(s: str) -> str:
    """Turkce buyuk/kucuk harf donusumu (Python .lower() İ→i̇ hatasi duzeltmesi)."""
    return s.replace("İ", "i").replace("I", "ı").replace("Ğ", "ğ").replace(
        "Ü", "ü").replace("Ş", "ş").replace("Ö", "ö").replace("Ç", "ç").lower()

# Is Yatirim modulu (tam finansal tablolar icin)
try:
    sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))
    from bbb_financials import (
        fetch_financials as isyatirim_fetch,
        print_financials,
        print_all_items,
        BANK_TICKERS,
    )
    HAS_ISYATIRIM = True
except ImportError:
    HAS_ISYATIRIM = False

# BIST sirket listesi cache (modul seviyesinde)
_COMPANY_CACHE: List[dict] = []

# --last parametresi icin zaman dilimi esleme
LAST_DURATIONS = {
    "1w": timedelta(weeks=1),
    "2w": timedelta(weeks=2),
    "1m": timedelta(days=30),
    "3m": timedelta(days=90),
    "6m": timedelta(days=180),
    "1y": timedelta(days=365),
}


class KAPFetcher:
    """KAP.org.tr'den veri ceken ana sinif."""

    def __init__(self, client: KAPClient):
        self.client = client

    # ── Bildirim Listeleme (BIRINCIL: bildirim-sorgu-sonuc) ──

    def fetch_all_disclosures(self, ticker: str) -> List[KAPDisclosure]:
        """
        bildirim-sorgu-sonuc?member= ile sirketin TUM bildirimlerini cek.
        Yapilandirilmis JSON - 150+ bildirim tek istekte.
        """
        oid = self.get_member_oid(ticker)
        if not oid:
            return []

        cache_key = f"all_disc_{ticker.upper()}"
        cached = self.client.cache_read(cache_key, max_age=600)  # 10 dk
        if cached:
            return [self._dict_to_disclosure(d) for d in cached]

        html = self.client.get_html(
            f"{KAP_BASE}/tr/bildirim-sorgu-sonuc?member={oid}",
            timeout=25,
        )
        if not html:
            return []

        disclosures = parse_disclosure_list(html)
        if disclosures:
            self.client.cache_write(cache_key, [self._disclosure_to_dict(d) for d in disclosures])

        return disclosures

    # ── Sinyal Filtreleme ──

    # Blacklist: kesinlikle gürültü (subject tam eşleşme, lower)
    _BLACKLIST_EXACT = {
        "şirket genel bilgi formu",
    }

    # Blacklist: keyword bazlı
    _BLACKLIST_KW = [
        "piyasa yapıcılığı kapsamında",
        "likidite sağlayıcılık kapsamında",
        "volatilite bazlı tedbir",
        "devre kesici",
        "satılabilir varant adedinin bitmesi",
        "varant alim satim",                # TEBYT günlük gürültü (KAP ASCII)
        "varant alım satım",               # Türkçe varyant
        "borsada işlem gören tipe dönüşüm",
        "ağırlıklı ortalama fiyat",        # GYO/fon NAV bildirimleri
        "katılım finansı ilkeleri bilgi",   # form doldurma
        "kurumsal yönetim bilgi formu",     # KYÖBF güncelleme → SGF benzeri form
        "pay alım satım bildirimi",         # KAP zorunlu bildirim, düşük sinyal
        "itfası tamamlanan borçlanma",      # geçmiş itfa → arşivsel bildirim
    ]

    # Blacklist: title tam eşleşme (lower+tr) — _BLACKLIST_EXACT'a ek
    _BLACKLIST_TITLE_PREFIX = [
        "yatırım kuruluşu varant",          # aracı kurum türev ürünü ihracı
        "sorumluluk beyanı",                # FR ile otomatik gelen boilerplate
        "faaliyet raporu sorumluluk",       # FR sorumluluk beyanı varyantı
        "bağımsız denetim kuruluşunun",     # GK rutin: her GK'da aynı
        "genel kurul bildirimi",            # GK rutin: "GK İşlemleri" zaten var
        "yönetim kurulu komiteleri",        # GK rutin: komite atama (önemli atama ODA'da)
    ]

    # GK paketi daraltma: subject tam eşleşme ile elenen ama
    # summary'de bağımsız sinyal varsa kurtarılan bildirimler.
    # Bu prefix'ler sadece summary'de rescue keyword yoksa elenir.
    _GK_ROUTINE_PREFIX = [
        "sürdürülebilirlik denetçi",        # compliance rutin
        "tsrs uyumlu sürdürülebilirlik",    # compliance raporu
    ]
    # GK paketi: summary'de bunlar varsa elenmez (bağımsız sinyal)
    _GK_RESCUE_KW = [
        "istifa", "görevden ayrıl", "atama", "seçim",
        "ihraç tavan", "ilişkili taraf",
    ]

    # Kupon/itfa gürültü (pay dışı sermaye aracı kategorisinde)
    _COUPON_NOISE_KW = [
        "kupon faiz", "kupon oran",        # kupon faiz oranı/ödemesi
        "kupon ödeme", "kupon ödemesi",
        "itfası tamamlan", "itfa ödemesi", "itfası",
        "kupon dönemine",
        "varlık finansmanı fonu",           # TMKS varlık fonu bildirimleri
        "finansman bonosu",                 # finansman bonosu kupon/ihraç
    ]

    # Sinyal kuralları — öncelik sırasıyla
    _SIGNAL_RULES = [
        ("TEZ", [
            "kar payı", "temettü", "kar dağıtım", "geleceğe dönük",
            "beklenti", "guidance", "revize", "bedelsiz sermaye",
            "bedelli sermaye", "sermaye artırım", "sermaye azaltım",
            "birleşme", "devralma", "bölünme", "tasfiye",
        ]),
        ("YAPISAL", [
            "geri al",                      # geri alım, geri alınan, geri alınması
            "finansal duran varlık", "yeni iş ilişkisi",
            "kredi derecelendirme", "kayıtlı sermaye tavan",
            "kira sertifika", "sukuk", "halka arz",
            "özkaynak", "ana sermaye",      # büyük tahvil ihraçları
            "toplu iş sözleşme",
            "ihraç kararı", "ihraç edilmesi",  # yeni ihraç (kupon değil)
        ]),
        ("FINANSAL", [
            "finansal rapor", "faaliyet raporu", "sorumluluk beyanı",
            "finansal raporlama",
        ]),
        ("KURUMSAL", [
            "genel kurul", "esas sözleşme",
            "yönetim kurulu", "atama", "istifa", "görevden",
            "kurumsal yönetim", "ilişkili taraf",
            "ihraç tavanı", "pay satış bilgi formu",
            "ihraç belgesi",
        ]),
    ]

    def filter_signals(self, disclosures: List[KAPDisclosure],
                       ) -> List[tuple]:
        """Bildirim listesinden anlamlı sinyalleri filtrele ve sınıflandır.

        Returns:
            List of (signal_type, disclosure) tuples.
            signal_type: "TEZ" | "YAPISAL" | "FINANSAL" | "KURUMSAL" | "DIGER"
        """
        results = []

        for d in disclosures:
            # Ticker yoksa fon/BİAŞ → atla
            if not d.ticker:
                continue

            text = _tr_lower((d.title or "") + " " + (d.summary or ""))
            subject = _tr_lower((d.title or "").strip())

            # Sert blacklist
            if subject in self._BLACKLIST_EXACT:
                continue

            # Title prefix blacklist
            if any(subject.startswith(pfx) for pfx in self._BLACKLIST_TITLE_PREFIX):
                continue

            # GK rutin bileşen (summary'de bağımsız sinyal yoksa ele)
            if any(subject.startswith(pfx) for pfx in self._GK_ROUTINE_PREFIX):
                summary_lower = _tr_lower(d.summary or "")
                if not any(rk in summary_lower for rk in self._GK_RESCUE_KW):
                    continue

            # Keyword blacklist
            if any(kw in text for kw in self._BLACKLIST_KW):
                continue

            # Kupon/itfa gürültü (pay dışı sermaye aracı)
            # Ama özkaynak/yeni ihraç/tamamlanma → sinyal, kurtarılır
            if "pay dışında sermaye piyasası aracı" in text:
                rescue = any(rk in text for rk in [
                    "özkaynak", "ihraç tamamlan", "ihracının tamamlan",
                    "ihracı tamamlan",
                ])
                if not rescue and any(nk in text for nk in self._COUPON_NOISE_KW):
                    continue

            # Sınıflandır
            signal_type = "DIGER"
            for stype, keywords in self._SIGNAL_RULES:
                if any(kw in text for kw in keywords):
                    signal_type = stype
                    break

            results.append((signal_type, d))

        return results

    def fetch_disclosures(self, ticker: str,
                          category: str = None,
                          last: str = None,
                          limit: int = None) -> List[KAPDisclosure]:
        """
        Filtrelenmis bildirim listesi.
        Birincil kaynak: bildirim-sorgu-sonuc (yapilandirilmis JSON).
        """
        disclosures = self.fetch_all_disclosures(ticker)

        # Kategori filtresi
        if category:
            cat_upper = category.upper()
            disclosures = [d for d in disclosures if d.category == cat_upper]

        # Tarih filtresi
        if last:
            delta = LAST_DURATIONS.get(last)
            if delta:
                cutoff = datetime.now() - delta
                disclosures = [d for d in disclosures if d.date >= cutoff]

        # Limit
        if limit:
            disclosures = disclosures[:limit]

        return disclosures

    # ── Bildirim Detay ──

    def fetch_detail(self, disc_id: str) -> Optional[KAPDetail]:
        """Bildirim detayi + ek dosya listesi."""
        cache_key = f"detail_{disc_id}"
        cached = self.client.cache_read(cache_key, max_age=3600)
        if cached:
            detail = KAPDetail(
                id=cached["id"],
                title=cached["title"],
                company=cached["company"],
                date=datetime.fromisoformat(cached["date"]) if isinstance(cached["date"], str) else datetime.now(),
                content=cached["content"],
                raw_fields=cached.get("raw_fields", {}),
            )
            # Attachments
            for a in cached.get("attachments", []):
                from .models import KAPAttachment
                detail.attachments.append(KAPAttachment(**a))
            return detail

        html = self.client.get_html(f"{KAP_BASE}/tr/Bildirim/{disc_id}", timeout=20)
        if not html:
            return None

        detail = parse_disclosure_detail(html)
        if detail:
            detail.id = disc_id
            # Cache
            cache_data = {
                "id": detail.id,
                "title": detail.title,
                "company": detail.company,
                "date": detail.date.isoformat(),
                "content": detail.content,
                "raw_fields": detail.raw_fields,
                "attachments": [{"obj_id": a.obj_id, "file_name": a.file_name,
                                 "file_extension": a.file_extension} for a in detail.attachments],
            }
            self.client.cache_write(cache_key, cache_data)

        return detail

    # ── Bugunun Bildirimleri (REST API) ──

    def _build_company_name_index(self) -> Dict[str, str]:
        """Sirket adi -> ticker eslestirme tablosu olustur.
        BIST sirket listesinden company title (upper) -> ticker mapping."""
        companies = self._load_bist_companies()
        index: Dict[str, str] = {}
        for c in companies:
            title = c.get("title", "").upper().strip()
            ticker = c.get("ticker", "").upper().strip()
            if title and ticker:
                index[title] = ticker
        return index

    def fetch_today(self, category: str = None) -> List[KAPDisclosure]:
        """GET /tr/api/disclosure/list/light - bugunun tum bildirimleri.
        Sirket adi -> ticker eslestirmesi otomatik yapilir."""
        cache_key = f"today_all_{datetime.now().strftime('%Y%m%d_%H')}"
        cached_data = self.client.cache_read(cache_key, max_age=120)

        if cached_data:
            disclosures = [self._dict_to_disclosure(d) for d in cached_data]
        else:
            resp = self.client.get(f"{KAP_BASE}/tr/api/disclosure/list/light", timeout=15)
            if not resp or resp.status_code != 200:
                return []

            # Sirket adi -> ticker eslestirme tablosu
            name_index = self._build_company_name_index()

            disclosures = []
            try:
                data = resp.json()
                for item in data:
                    subject = item.get("subject", "") or ""
                    summary = item.get("summary", "") or ""
                    disc_id = str(item.get("disclosureIndex", ""))
                    cat = self._classify_category(subject)

                    company_name = item.get("title", "") or ""
                    ticker = name_index.get(company_name.upper().strip(), "")

                    date_str = item.get("publishDate", "") or ""
                    try:
                        date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
                    except ValueError:
                        date = datetime.now()

                    disclosures.append(KAPDisclosure(
                        id=disc_id,
                        title=subject,
                        company=company_name,
                        ticker=ticker,
                        date=date,
                        summary=summary.strip(),
                        category=cat,
                        url=f"{KAP_BASE}/tr/Bildirim/{disc_id}",
                    ))
                self.client.cache_write(cache_key, [self._disclosure_to_dict(d) for d in disclosures])
            except Exception as e:
                logger.warning("KAP API hatasi: %s", e)

        if category:
            disclosures = [d for d in disclosures if d.category == category.upper()]
        return disclosures

    # ── Tarihli Bildirim Sorgu (Tüm BIST) ──

    def fetch_by_date(self, date: str, category: str = None) -> List[KAPDisclosure]:
        """Belirli bir tarihin tum BIST bildirimlerini cek.

        POST /tr/api/disclosure/members/byCriteria endpoint'i.
        Today API'den farkli olarak gecmis tarihler icin de calisir.

        Args:
            date: Tarih (YYYY-MM-DD veya DD.MM.YYYY)
            category: Opsiyonel filtre (ODA, FR, GK, TEM, SA, YON, DG)

        Returns:
            Tum bildirimlerin listesi (stockCodes alani olanlar ticker ile eslenir)
        """
        # Tarih normalizasyonu
        if "-" in date:
            # YYYY-MM-DD -> DD.MM.YYYY
            parts = date.split("-")
            api_date = f"{parts[2]}.{parts[1]}.{parts[0]}"
            cache_date = date
        else:
            api_date = date
            parts = date.split(".")
            cache_date = f"{parts[2]}-{parts[1]}-{parts[0]}"

        cache_key = f"bydate_{cache_date}"
        cached_data = self.client.cache_read(cache_key, max_age=3600)

        if cached_data:
            disclosures = [self._dict_to_disclosure(d) for d in cached_data]
        else:
            payload = {"fromDate": cache_date, "toDate": cache_date}
            try:
                resp = self.client.session.post(
                    f"{KAP_BASE}/tr/api/disclosure/members/byCriteria",
                    json=payload, timeout=20,
                    headers={"Content-Type": "application/json"},
                )
                if not resp or resp.status_code != 200:
                    return []

                data = resp.json()
            except Exception as e:
                logger.warning("KAP byCriteria hatasi: %s", e)
                return []

            disclosures = []
            for item in data:
                stock_codes = item.get("stockCodes", "") or ""
                subject = item.get("subject", "") or ""
                summary = item.get("summary", "") or ""
                disc_id = str(item.get("disclosureIndex", ""))
                company_name = item.get("kapTitle", "") or ""

                date_str = item.get("publishDate", "") or ""
                try:
                    pub_date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
                except ValueError:
                    pub_date = datetime.now()

                # disclosureCategory (byCriteria endpoint'inde var)
                disc_cat = item.get("disclosureCategory", "") or ""
                # Normalize
                cat = disc_cat if disc_cat in ("ODA", "FR", "GK", "TEM", "SA",
                                                "YON", "ORT", "DG", "STT") \
                    else self._classify_category(subject)

                disclosures.append(KAPDisclosure(
                    id=disc_id,
                    title=subject,
                    company=company_name,
                    ticker=stock_codes,
                    date=pub_date,
                    summary=summary.strip(),
                    category=cat,
                    attachment_count=item.get("attachmentCount", 0) or 0,
                    is_late=item.get("isLate", False) or False,
                    has_multilang=(item.get("hasMultiLanguageSupport", "") == "Y"),
                    url=f"{KAP_BASE}/tr/Bildirim/{disc_id}",
                ))

            self.client.cache_write(cache_key,
                                    [self._disclosure_to_dict(d) for d in disclosures])

        if category:
            cat_upper = category.upper()
            disclosures = [d for d in disclosures if d.category == cat_upper]

        return disclosures

    # ── Sirket Bilgileri ──

    def fetch_profile(self, ticker: str) -> Optional[KAPCompanyProfile]:
        """Sirket profili cek."""
        ticker = ticker.upper()
        cache_key = f"profile_{ticker}"
        cached = self.client.cache_read(cache_key, max_age=3600)
        if cached:
            prof = KAPCompanyProfile(**{k: v for k, v in cached.items()
                                        if k != "recent_disclosures"})
            return prof

        oid = self.get_member_oid(ticker)
        if not oid:
            return None

        oid_data = self.client.cache_read(f"oid_{ticker}", max_age=86400)
        company_name = oid_data.get("title", "") if oid_data else ""

        profile = KAPCompanyProfile(
            ticker=ticker,
            name=company_name,
            member_oid=oid,
        )

        # yfinance'dan ek bilgi
        try:
            import yfinance as yf
            stock = yf.Ticker(f"{ticker}.IS")
            info = stock.info
            profile.sector = info.get("sector", "") or ""
            profile.website = info.get("website", "") or ""
        except Exception:
            pass

        profile.recent_disclosures = self.fetch_disclosures(ticker, limit=5)

        cache_data = {k: v for k, v in profile.__dict__.items() if k != "recent_disclosures"}
        self.client.cache_write(cache_key, cache_data)
        return profile

    def fetch_summary(self, ticker: str) -> Dict:
        """Ozet gorunum: profil + onemli bildirimler."""
        profile = self.fetch_profile(ticker)
        disclosures = self.fetch_disclosures(ticker, limit=20)
        important = [d for d in disclosures if d.importance in ("high", "medium")]
        if not important:
            important = disclosures[:5]
        return {
            "profile": profile,
            "important_disclosures": important[:5],
            "all_disclosures": disclosures[:10],
        }

    def fetch_kap_summary(self, ticker: str) -> Optional[dict]:
        """KAP SSR sayfasindan finansal ozet cek."""
        member_oid = self.get_member_oid(ticker)
        if not member_oid:
            return None

        cache_key = f"kap_summary_{member_oid}"
        cached = self.client.cache_read(cache_key, max_age=43200)
        if cached:
            return cached

        html = self.client.get_html(
            f"{KAP_BASE}/tr/sirket-finansal-bilgileri/{member_oid}",
            timeout=10,
        )
        if not html:
            return None

        result = parse_kap_financial_page(html, ticker)
        if result:
            self.client.cache_write(cache_key, result)
        return result

    def fetch_financials(self, ticker: str, start_year: int = None,
                         end_year: int = None, exchange: str = "TRY",
                         source: str = "auto") -> dict:
        """Tam finansal tablolar (Is Yatirim delegation)."""
        result = {"ticker": ticker.upper(), "source": None, "data": None,
                  "kap_summary": None, "error": None}

        if source in ("auto", "isyatirim") and HAS_ISYATIRIM:
            try:
                data = isyatirim_fetch(ticker, start_year=start_year,
                                       end_year=end_year, exchange=exchange)
                if data:
                    result["source"] = "isyatirim"
                    result["data"] = data
            except Exception as e:
                if source == "isyatirim":
                    result["error"] = str(e)

        if source in ("auto", "kap"):
            try:
                kap = self.fetch_kap_summary(ticker)
                if kap:
                    result["kap_summary"] = kap
                    if not result["data"]:
                        result["source"] = "kap_summary"
            except Exception as e:
                if source == "kap":
                    result["error"] = str(e)

        if not result["data"] and not result["kap_summary"]:
            result["error"] = f"Veri bulunamadi: {ticker}"
        return result

    def fetch_financial_disclosures(self, ticker: str, limit: int = 5) -> List[KAPDisclosure]:
        """Sadece finansal rapor bildirimleri."""
        return self.fetch_disclosures(ticker, category="FR", limit=limit)

    # ── Sirket Lookup ──

    def lookup_company(self, ticker: str) -> Optional[dict]:
        """BIST sirket listesinden lookup."""
        global _COMPANY_CACHE
        companies = _COMPANY_CACHE or self._load_bist_companies()
        ticker_upper = ticker.upper()
        for company in companies:
            tickers = [t.strip() for t in company["ticker"].split(",")]
            if ticker_upper in tickers:
                return company
        return None

    def get_member_oid(self, ticker: str) -> Optional[str]:
        """Ticker -> memberOid donusumu."""
        ticker = ticker.upper()

        # 1. BIST listesinden
        company = self.lookup_company(ticker)
        if company and company.get("memberOid"):
            return company["memberOid"]

        # 2. REST API fallback
        cached = self.client.cache_read(f"oid_{ticker}", max_age=86400)
        if cached:
            return cached.get("oid")

        resp = self.client.get(f"{KAP_BASE}/tr/api/member/filter/{ticker}", timeout=10)
        if resp and resp.status_code == 200:
            try:
                data = resp.json()
                if data and isinstance(data, list) and len(data) > 0:
                    oid = data[0].get("mkkMemberOid", "")
                    self.client.cache_write(f"oid_{ticker}", {
                        "oid": oid,
                        "title": data[0].get("title", ""),
                        "code": data[0].get("companyCode", ""),
                    })
                    return oid
            except Exception:
                pass
        return None

    def search(self, keyword: str, limit: int = 20,
               tickers: List[str] = None, last: str = "3m") -> List[KAPDisclosure]:
        """Anahtar kelime ile bildirim ara.

        Iki katmanli arama:
        1. Bugunun tum bildirimleri (today API)
        2. Belirtilen ticker'larin gecmis bildirimleri (guvenilir bildirim-sorgu-sonuc API)

        Args:
            keyword: Aranacak kelime (baslik + ozet + sirket adinda)
            limit: Maksimum sonuc sayisi
            tickers: Aranacak ticker listesi (None = sadece today)
            last: Gecmis zaman dilimi (1w/1m/3m/6m — ticker aramasi icin)
        """
        kw = keyword.lower()

        # Katman 1: Bugunun tum bildirimleri
        today = self.fetch_today()
        results = [d for d in today if kw in
                   (d.title + " " + d.summary + " " + d.company).lower()]

        # Katman 2: Ticker bazli gecmis arama (guvenilir API)
        if tickers and len(results) < limit:
            existing_ids = {d.id for d in results}
            for ticker in tickers:
                if len(results) >= limit:
                    break
                discs = self.fetch_disclosures(ticker, last=last)
                for d in discs:
                    if d.id not in existing_ids and kw in \
                       (d.title + " " + d.summary + " " + d.company).lower():
                        results.append(d)
                        existing_ids.add(d.id)
                        if len(results) >= limit:
                            break

        return results[:limit]

    # ── Yardimci ──

    def _load_bist_companies(self) -> List[dict]:
        """BIST sirket listesi yukle."""
        global _COMPANY_CACHE
        cached = self.client.cache_read("bist_companies_all", max_age=86400)
        if cached:
            _COMPANY_CACHE = cached
            return cached

        html = self.client.get_html(f"{KAP_BASE}/tr/bist-sirketler", timeout=10)
        if not html:
            return []

        companies = []
        pattern = (
            r'mkkMemberOid\\?":\\?"([^"\\]+)\\?"[^}]*'
            r'kapMemberTitle\\?":\\?"([^"\\]+)\\?"[^}]*'
            r'stockCode\\?":\\?"([^"\\]+)\\?"[^}]*'
            r'cityName\\?":\\?"([^"\\]*?)\\?"'
        )
        for match in re.finditer(pattern, html):
            companies.append({
                "memberOid": match.group(1),
                "title": match.group(2),
                "ticker": match.group(3),
                "city": match.group(4),
            })

        if companies:
            self.client.cache_write("bist_companies_all", companies)
            _COMPANY_CACHE = companies
        return companies

    @staticmethod
    def _classify_category(subject: str) -> str:
        """Bildirim konusunu kategorize et (today API icin - JSON'da class yok)."""
        s = subject.lower()
        if "ozel durum" in s:
            return "ODA"
        elif any(k in s for k in ["finansal rapor", "finansal tablo", "sorumluluk beyani"]):
            return "FR"
        elif "genel kurul" in s:
            return "GK"
        elif any(k in s for k in ["temettu", "kar payi", "kar dagitim"]):
            return "TEM"
        elif any(k in s for k in ["sermaye artirimi", "bedelli", "bedelsiz"]):
            return "SA"
        elif any(k in s for k in ["yonetim", "atama", "istifa"]):
            return "YON"
        elif any(k in s for k in ["pay alim", "pay satim", "ortaklik"]):
            return "ORT"
        return "DG"

    @staticmethod
    def _disclosure_to_dict(d: KAPDisclosure) -> dict:
        return {
            "id": d.id, "title": d.title, "company": d.company,
            "ticker": d.ticker, "date": d.date.isoformat(),
            "category": d.category, "summary": d.summary,
            "attachment_count": d.attachment_count, "is_late": d.is_late,
            "has_multilang": d.has_multilang, "url": d.url,
        }

    @staticmethod
    def _dict_to_disclosure(d: dict) -> KAPDisclosure:
        date = d.get("date", "")
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                date = datetime.now()
        return KAPDisclosure(
            id=d["id"], title=d.get("title", ""), company=d.get("company", ""),
            ticker=d.get("ticker", ""), date=date,
            category=d.get("category", "DG"), summary=d.get("summary", ""),
            attachment_count=d.get("attachment_count", 0),
            is_late=d.get("is_late", False),
            has_multilang=d.get("has_multilang", False),
            url=d.get("url", ""),
        )
