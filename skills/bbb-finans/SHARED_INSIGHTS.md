# BBB Finans - Shared Insights

## Fintables.com Araştırması (2026-02-10)

### Erişim
- Fintables.com Cloudflare koruması altında, web_fetch ile 403 döndürüyor
- Muhtemelen JavaScript rendering gerektiren bir SPA

### Bilinen Özellikler (web araştırmasından)
- Türk hisselerinin finansal tablolarını gösteriyor
- Şirket bazlı sayfalar: `fintables.com/sirketler/THYAO/finansal-tablolar/bilanco`
- Bilanço, gelir tablosu, nakit akış tablosu ayrı ayrı
- Yıllık ve çeyreklik veriler
- Karşılaştırmalı dönemler

### API
- Cloudflare koruması nedeniyle doğrudan API erişimi test edilemedi
- Muhtemelen backend API var ama Cloudflare arkasında

---

## KAP.org.tr Finansal Tablo Yapısı

### Mimari
- **Frontend**: Next.js (React Server Components / RSC)
- **Backend**: `kapsitebackend.mkk.com.tr` (internal, public erişim yok)
- **Veri Aktarımı**: RSC stream (HTML içinde embedded React component data)

### Keşfedilen API Endpoints (kap.org.tr)
Çalışan public endpointler:
- `GET /tr/api/member/filter/{TICKER}` → Şirket bilgisi + memberOid + permaLink
- `GET /tr/api/member/logo/{memberOid}` → Logo
- `GET /tr/api/disclosure/list/light` → Günün bildirimleri

Backend (internal only, Next.js server-side):
- `api/company-detail/sgbf-data/{oid}` → Özet finansal bilgiler
- `api/company/items/{oid}` → Şirket kalemleri
- `api/export/compareItems` → Kalem karşılaştırma export
- `api/financialTable/download` → Finansal tablo indirme
- `api/analysis/compare-items-by-sector` → Sektörel karşılaştırma
- `api/analysis/companies-by-sector` → Sektör şirketleri

### Finansal Veri Sayfası
- **URL Pattern**: `https://www.kap.org.tr/tr/sirket-finansal-bilgileri/{permaLink}`
- **Veri Yapısı**: RSC stream içinde HTML tablo olarak render edilir
- **Tablo Tipleri**: `bilanco` (bilanço), `gelir` (gelir tablosu)
- **Cell Key Formatı**: `{tablo}_{dönem}_{satır_idx}` (örn: `bilanco_2024/12_2`)
- **Dönemler**: Genelde son 3-4 yıllık veriler + en güncel ara dönem

### Bilanço Kalemleri (Sanayi Şirketleri)
- Dönen Varlıklar
- Duran Varlıklar
- Toplam Varlıklar
- Kısa Vadeli Yükümlülükler
- Uzun Vadeli Yükümlülükler
- Toplam Yükümlülükler
- Ana Ortaklığa Ait Özkaynaklar
- Ödenmiş Sermaye
- Kontrol Gücü Olmayan Paylar
- Toplam Özkaynaklar
- Toplam Kaynaklar

### Bilanço Kalemleri (Bankalar)
- Finansal Varlıklar (Net)
- İtfa Edilmiş Maliyeti ile Ölçülen Finansal Varlıklar (Net)
- Maddi Duran Varlıklar
- Varlıklar Toplamı
- Mevduat
- Alınan Krediler
- Özkaynaklar
- Yükümlülükler Toplamı

### Gelir Tablosu Kalemleri (Sanayi)
- Hasılat
- Satışların Maliyeti
- Brüt Kâr (Zarar)
- Esas Faaliyet Kârı
- FVÖK (Finansman Geliri/Gideri Öncesi Faaliyet Kârı)
- VÖK (Sürdürülen Faaliyetler Vergi Öncesi Kâr)
- Net Dönem Kârı
- Diğer Kapsamlı Gelir
- Toplam Kapsamlı Gelir

### IAS 29 (Enflasyon Muhasebesi) Notu
KAP'ın kalem-karsilastirma sayfasındaki uyarı:
> Bu sayfadan yapılacak sorgu sonuçlarında yer alan veriler, ilgili yıl ve döneme ilişkin
> KAP'ta en son yayınlanan finansal tabloda yer alan "cari dönem" sütunundaki verileri
> içermekte olup, ilgili cari yıl ve döneme ilişkin tablolar yayınlanırken "önceki dönem"
> bilgilerinde yapılan düzeltmeler dikkate alınmamaktadır.

Bu, KAP özet sayfasındaki karşılaştırmalı verilerin IAS 29 restate edilmiş 
(enflasyon düzeltmeli) veriler **olmadığı** anlamına gelir. Her dönemin kendi 
"cari" değeri gösterilir. Tam restate edilmiş karşılaştırmalı tablolar için 
şirketin detaylı XBRL raporuna bakmak gerekir.

### Kısıtlamalar
1. Özet finansal bilgiler sayfası sadece ana kalemleri gösterir (detaylı alt kalemler yok)
2. Nakit akış tablosu bu sayfada bulunmuyor
3. TTM hesaplaması için önceki yılın ara dönemi gerekli ama özet sayfada yok
4. `$undefined` değerler: bazı şirketlerde bazı kalemler raporlanmıyor

### Alternatif Veri Kaynakları
- **İş Yatırım API** (isyatirimhisse): Daha detaylı finansal tablolar, XBRL bazlı
- **XBRL Raporları**: KAP'tan indirilebilir (api/financialTable/download)
- **pykap** kütüphanesi: KAP wrapper (pip install pykap)
