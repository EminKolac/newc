---
name: bbb-finans
description: >-
  BBB Finans — BIST şirketleri için veri toplama araç seti.
  KAP finansal tablolar (147+ kalem), bildirimler, şirket lookup,
  döviz kurları (TCMB), yabancı peer analizi (Yahoo Finance).
  Equity-analyst ve bbb-dcf skill'leri bu skill'in veri katmanını kullanır.
---

# BBB Finans — Türkiye Finansal Veri Toplama Araçları

**Versiyon:** 2.1.0
**Tarih:** 2026-03-18
**Rol:** Veri toplama. Değerleme (DCF) → `bbb-dcf` skill'i. Analiz/rapor → `equity-analyst` skill'i.

---

## Modül Haritası (4 Dosya + kap/ package + dcf_tools)

| Dosya | Kaynak | Ne Yapar? |
|-------|--------|-----------|
| `bbb_financials.py` | İş Yatırım API | **Ana motor:** 147+ kalem, bilanço/gelir/nakit, 2019-güncel, cache, DCF JSON, fiyat verileri (OHLCV), endeks |
| `bbb_kap.py` | KAP REST API + SSR | **KAP CLI:** bildirimler, ÖDA, profil, arama, arşivleme, PDF indirme |
| `kap/` | — | **Modüler KAP paketi:** models, client, parser, fetcher, archiver, formatter (7 dosya) |
| `bbb_yfinance.py` | Yahoo Finance | **Yabancı peer:** fiyat, çarpan, earnings, peer karşılaştırma tablosu |
| `bbb_fx.py` | TCMB XML API | **Döviz:** güncel kurlar |
| `dcf_tools/` | — | **DCF yardımcıları:** beta, ERP, WACC, Monte Carlo, synthetic rating, dual track |

---

## Komut Referansı

### Çalışma dizini
```bash
cd ~/.openclaw/workspace/skills/bbb-finans/scripts
```

### 1. Finansal Tablolar (İş Yatırım — BİRİNCİL)
```bash
python3 bbb_financials.py {TICKER} --section all --full    # Tüm kalemler (147+)
python3 bbb_financials.py {TICKER} --section income        # Sadece gelir tablosu
python3 bbb_financials.py {TICKER} --section cashflow      # Sadece nakit akış
python3 bbb_financials.py {TICKER} --dcf --json            # DCF için JSON
python3 bbb_financials.py {TICKER} --price                 # Fiyat verileri (OHLCV)
python3 bbb_financials.py --index XU100                    # Endeks verileri
python3 bbb_financials.py {TICKER} --summary               # Özet kart: fiyat, market cap, çarpanlar
python3 bbb_financials.py {TICKER} --exchange USD          # USD bazlı
python3 bbb_financials.py {TICKER} --start-year 2022 --end-year 2025
```

### 2. KAP (Bildirimler + Arşivleme + Özet Finansal + Lookup)
```bash
# Bildirim listeleme
python3 bbb_kap.py {TICKER}                              # Son 20 bildirim
python3 bbb_kap.py {TICKER} --all                         # Tüm bildirimler (150+)
python3 bbb_kap.py {TICKER} --last 6m                     # Son 6 ay
python3 bbb_kap.py {TICKER} --last 3m --category ODA      # Son 3 ay ÖDA'lar
python3 bbb_kap.py {TICKER} --id 1564560                  # Bildirim detayı + ek dosyalar

# Arşivleme ve indirme
python3 bbb_kap.py {TICKER} --archive                     # Toplu arşivleme (son 6 ay, kap_docs/'a)
python3 bbb_kap.py {TICKER} --archive --last 1y           # Son 1 yıl arşivle
python3 bbb_kap.py {TICKER} --archive --ids 1560680,1561522  # Seçici arşivleme (AI filtreli)
python3 bbb_kap.py {TICKER} --download <objId>            # Tek ek dosya indir
python3 bbb_kap.py {TICKER} --download <objId> --dest /path  # Belirli klasöre indir

# Şirket bilgileri
python3 bbb_kap.py {TICKER} --kap-summary                 # KAP özet finansal tablo
python3 bbb_kap.py {TICKER} --lookup                      # Şirket bilgisi (memberOid, sektör)
python3 bbb_kap.py {TICKER} --profile                     # Şirket profili
python3 bbb_kap.py {TICKER} --summary                     # Özet görünüm

# Diğer
python3 bbb_kap.py --today                                 # Bugünün tüm bildirimleri
python3 bbb_kap.py search "temettü"                        # Anahtar kelime araması
python3 bbb_kap.py {TICKER} --json                         # JSON çıktı formatı
```

### 3. Yabancı Peer (Yahoo Finance)
```bash
python3 bbb_yfinance.py quote LVS              # Fiyat + çarpanlar
python3 bbb_yfinance.py compare LVS,WYNN,MGM   # Peer karşılaştırma tablosu
python3 bbb_yfinance.py earnings WYNN           # Earnings + sürpriz
python3 bbb_yfinance.py fundamentals WYNN       # PE, EPS, marjlar, ROE
python3 bbb_yfinance.py json LVS               # Ham JSON
```

### 4. Döviz Kurları (TCMB)
```bash
python3 bbb_fx.py                               # Tüm kurlar
python3 bbb_fx.py USD                            # Tek kur
```

### 5. bbb CLI (Router)
```bash
python3 bbb financials THYAO --section all --full
python3 bbb kap THYAO --kap-summary
python3 bbb yf compare LVS,WYNN,MGM
python3 bbb fx USD
python3 bbb full THYAO                           # Tam özet: finansal + bildirimler + döviz
```

---

## ⚠️ Kritik Uyarılar

### 🔴 IAS 29 — İki Veri Kaynağı, İki Farklı Rakam
`bbb_financials.py` (İş Yatırım API, group=1/XI_29) → **IAS 29 düzeltmeli** rakamlar döndürür.
`bbb_kap.py --kap-summary` (KAP SSR sayfası) → **nominal (düzeltmesiz)** rakamlar döndürebilir.

**Örnek (THYAO 2024/FY Hasılat):** İş Yatırım: 975.7B TL | KAP SSR: 745.4B TL → **%31 fark** (IAS 29 düzeltme etkisi).

**Neden farklı?** KAP finansal tabloları statik snapshot: her dönem sadece o tarihteki enflasyon düzeltmesiyle yayınlanır, geçmişe taşınmaz. Örneğin 2022/12 tablosu 2022 sonundaki düzeltmeyi içerir ama 2025'teki enflasyona göre güncellenmez. İş Yatırım ise IAS 29 düzeltmeli serileri tutarlı şekilde sunar.

**Kural:**
- **BİRİNCİL:** `bbb_financials.py` — tüm modelleme ve metrik hesaplamaları buradan. Tarihsel karşılaştırma güvenilir.
- **İKİNCİL:** `bbb_kap.py --kap-summary` — sadece quick scan / bildirim takibi. Buradaki rakamları modele girme.
- Aynı şirket için iki kaynaktan farklı rakam gelirse → **her zaman `bbb_financials.py`'yi baz al.**

### 🔴 IAS 29 — Yahoo Finance BIST Çarpanları GÜVENİLMEZ
IAS 29 düzeltmeli finansallar + nominal fiyat → Yahoo çarpanları absürt çıkar.
Örnek (THYAO): PD/DD=19.09, FD/FAVÖK=144.93 → **hepsi yanlış**.
**Kural:** BIST çarpanları → `bbb_financials.py`. Yahoo → **sadece yabancı peer**.

### 🔴 KAP'a web_fetch ile GİRME
Cloudflare engelliyor. Bu skill'in araçlarını kullan.

### 🔴 TTM Hesaplama (Manuel)
```
TTM = Son Kümülatif Dönem + (Önceki FY − Önceki Yılın Aynı Kümülatif Dönemi)
Bilanço kalemleri → TTM YAPILMAZ, son çeyrek sonu değeri kullanılır
```

### 🔴 Veri Hiyerarşisi
1. **KAP/İş Yatırım** (bbb_financials.py, bbb_kap.py) → BİRİNCİL
2. **Şirket IR** → İKİNCİL
3. **Yahoo Finance** (bbb_yfinance.py) → Sadece yabancı peer
4. **StockAnalysis, TradingView vb.** → ASLA birincil kaynak

---

## Veri Tazeliği (Cache Davranışı)

Script'ler API çağrılarını diske cache'ler — her istekte yeniden çekmez.

| Veri Tipi | Cache Süresi | Otomatik Yenileme | Cache Konumu |
|-----------|-------------|-------------------|--------------|
| Finansal tablolar (İş Yatırım) | 7 gün | Kazanç sezonunda (Şub, Mar, May, Ağu, Kas) → 2 gün | `scripts/bbb_cache/financials.db` |
| KAP şirket listesi | 24 saat | — | `~/.bbb/cache/kap/` |
| KAP memberOid | 24 saat | — | `~/.bbb/cache/kap/` |
| KAP özet finansal | 12 saat | — | `~/.bbb/cache/kap/` |
| KAP bildirimler | 5 dakika | — | `~/.bbb/cache/kap/` |
| KAP profil/arama | 1 saat | — | `~/.bbb/cache/kap/` |
| Döviz kurları (TCMB) | Anlık (cache yok) | — | — |

**Manuel temizleme:**
- Finansal tablolar: `python3 bbb_financials.py --cache-clear THYAO` (tek ticker) veya `--cache-clear ALL`
- Tüm cache: `rm -rf scripts/bbb_cache/ ~/.bbb/cache/kap/`
- Cache bypass: `python3 bbb_financials.py {TICKER} --no-cache`

---

## Dosya Yapısı

```
bbb-finans/
├── SKILL.md
├── scripts/
│   ├── bbb                     # CLI router (5 komut: financials, kap, yf, fx, full)
│   ├── bbb_financials.py       # İş Yatırım 147+ kalem + fiyat + endeks
│   ├── bbb_kap.py              # KAP birleşik: bildirimler + lookup + özet finansal
│   ├── bbb_yfinance.py         # Yahoo Finance yabancı peer
│   ├── bbb_fx.py               # TCMB döviz
│   ├── dcf_tools/              # DCF yardımcı modüller (11 dosya)
│   └── kap/                    # Modüler KAP paketi (7 dosya: client, fetcher, parser, archiver, formatter, models, __init__)
```

---

## Changelog

- **2.3.0** (2026-03-25) — KAP tarihli tarama + sinyal filtreleme:
  - `fetch_by_date(date)` YENİ: byCriteria POST API ile herhangi bir tarihte tüm BIST bildirimlerini çek (0.2sn, 300+ bildirim)
  - `filter_signals(disclosures)` YENİ: 5 seviye sinyal sınıflandırma (TEZ/YAPISAL/FINANSAL/KURUMSAL/DIGER)
  - `_tr_lower()` YENİ: Python İ→i̇ Unicode hatasını düzelten Türkçe lowercase (171/326 bildirimi etkileyen bug fix)
  - Kupon/itfa noise filtresi: rutin kupon ödemesi/oranı elenir, özkaynak/yeni ihraç korunur (rescue kuralı)
  - Blacklist: SGF, NAV bildirimi, piyasa yapıcılığı, varant ticareti, katılım finans formu
  - CLI: `bbb_kap.py --date YYYY-MM-DD [--category ODA] [--json]`
- **2.2.0** (2026-03-25) — KAP bugfix + arşiv temizliği:
  - `fetch_today()` artık şirket adı → ticker otomatik eşleştiriyor (725 BIST şirketi, %48 hit rate)
  - Çoklu ticker bug fix: KAP'ın `ALBRK, ALK` gibi virgüllü döndürdüğü ticker'lar artık doğru filtreleniyor
  - archive/ ve scripts/archive/ tamamen silindi (~12K satır ölü kod, git'te mevcut)
  - KAP detay parse: raw_fields encoding fix (Türkçe karakterler artık düzgün)
  - search() iyileştirmesi: ticker listesi + geçmiş arama desteği (sadece today'e bağımlı değil)
  - Segment gelir notu: API'den gelmez, `--archive` ile faaliyet raporu PDF indirilerek elde edilir
  - IAS 29 açıklaması genişletildi: KAP snapshot'ları statik, İş Yatırım tutarlı seri
- **2.1.0** (2026-03-18) — Audit v2 düzeltmeleri:
  - `bbb_financials.py --summary` YENİ: Tek komutla fiyat, market cap ($+TL), pay sayısı, TTM finansallar, marjlar, çarpanlar (P/E, EV/EBITDA, P/BV), ROIC, ICR, EPS
  - IAS 29 uyarısı: KAP SSR (nominal) vs İş Yatırım (IAS 29 düzeltmeli) farkı belgelendi, İş Yatırım birincil kural yazıldı
  - Cache TTL düzeltmesi: 30 gün → 7 gün (gerçek kod), 6 saat → 2 gün, cache konumları düzeltildi
  - `__pycache__` temizlendi
- **2.0.1** (2026-03-18) — Audit düzeltmeleri:
  - `bbb_kap.py` memberOid lookup dedup: `_get_member_oid()` artık önce `lookup_company()` dener, bulamazsa REST API fallback
  - Cache TTL tablosu SKILL.md'ye eklendi
  - TCMB EVDS API notu: faiz/enflasyon fonksiyonu EVDS key gelince eklenecek
- **2.0.0** (2026-03-18) — Konsolidasyon:
  - 16 script → 4 dosya (%78 küçülme, 26K → 5.8K satır)
  - `bbb` CLI sadeleştirildi: 5 komut (financials, kap, yf, fx, full)
  - SKILL.md tamamen yeniden yazıldı
- **1.0.0** (2026-03-18) — İlk audit, providers/ ve terminal backend temizliği
- **0.2.0** (2026-02-10) — İlk versiyon

---

## BBB Öğrenmeler

- [2026-03-18] [Kaya] 16 script çakışması: 6 farklı veri kaynağı aynı türde veri çekiyordu. Birleştirme sonrası 4 dosya yeterli.
- [2026-03-18] [Kaya] Yahoo Finance BIST çarpanları IAS 29 nedeniyle absürt. Sadece yabancı peer için.
- [2026-03-18] [Kaya] MKK API çalışıyor ama sadece 2022 verisi döndürüyor — güncel değil, kaldırıldı.
- [2026-03-18] [Kaya] bbb_isyatirim.py ve bbb_financials.py aynı İş Yatırım API'sini kullanıyordu — çakışma.
- [2026-03-25] [Kaya] STT kategorisini toptan elemek YANLIŞ — içinde kar payı dağıtım (16x), sermaye artırım (2x), geri alım (6x) var. Subject bazlı filtreleme doğru.
- [2026-03-25] [Kaya] Python `'İ'.lower()` = `'i̇'` (dotted i) — Türkçe keyword eşleştirmede 171/326 bildirim etkileniyor. `_tr_lower()` zorunlu.
- [2026-03-25] [Kaya] KAP today API gece 00:00'da sıfırlanıyor, 03:00 taraması dünü kaçırıyor. `byCriteria` POST API ile çözüldü.
