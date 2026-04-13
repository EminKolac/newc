# Equity Analyst — Düzenleyici Ortam Taraması

> CIMSA analizinde (11 Şubat 2026) İlker tarafından tespit edilen eksiklikten sonra eklendi. ATLANAMAZ.

---

## Neden Zorunlu?

Çimento'da Rekabet Kurulu 1999'dan bu yana onlarca kartel soruşturması açmış. Bu bilgi olmadan Porter "Rekabet Yoğunluğu" 4/5 çıkmıştı — düzenleyici bulgularla 2/5 (koordineli yapı). Tamamen farklı yatırım hikayesi.

**Kural:** Düzenleyici ortam taranmadan sektör analizi tamamlanmış sayılmaz.

---

## Sektör Bazlı Regülatör Haritası

| BIST Sektörü | Birincil Regülatör | İkincil Kaynak | Tipik Risk |
|-------------|-------------------|----------------|------------|
| Bira/Alkollü İçki | **TAPDK** (tapdk.gov.tr) | Sağlık Bakanlığı | ÖTV artışı, reklam yasağı, ruhsat kısıtlaması |
| Bankacılık | **BDDK** (bddk.org.tr) | TCMB, SPK | Sermaye yeterliliği, kredi büyüme sınırı, NIM baskısı |
| Telecom | **BTK** (btk.gov.tr) | Rekabet Kurulu | Frekans ihaleleri, ARPU düzenleme, fiberleşme yükümlülüğü |
| Enerji | **EPDK** (epdk.gov.tr) | Çevre Bakanlığı | Tarife düzenlemesi, YEKDEM/YEKSOB, emisyon standartları |
| Çimento/Maden | **Rekabet Kurulu** | Çevre Bakanlığı, AB | Kartel soruşturmaları, CBAM, çevre lisansı |
| Otomotiv | **OSD** (sektör), Sanayi Bakanlığı | AB, ABD | İhracat kotaları, emisyon standartları, EV teşvikleri |
| Havacılık | **SHGM**, DHMİ | IATA, AB havacılık | Slot tahsisi, yer hizmetleri lisans, yakıt vergisi |
| İlaç/Sağlık | **TİTCK**, SGK | Sağlık Bakanlığı | İlaç fiyat tavanı, SGK geri ödeme, lisans |
| Perakende | Ticaret Bakanlığı | Rekabet Kurulu | Haksız fiyat düzenlemeleri, pazar yeri (marketplace) kuralları |
| Sigorta | **SEDDK** | Hazine | Teknik karlılık düzenlemesi, zorunlu sigortalar |

---

## Zorunlu Kaynak Taraması (Her Sektör Analizinde)

| Kaynak | Ne Aranır | Araç |
|--------|-----------|------|
| **Rekabet Kurulu** (rekabet.gov.tr) | Sektöre yönelik soruşturmalar, kartel cezaları, birleşme izinleri | `web_search "rekabet kurulu [sektör] soruşturma"` |
| **SPK** (spk.gov.tr) | Sermaye piyasası düzenlemeleri, ek beyan yükümlülükleri | `web_search "SPK [sektör] düzenleme"` |
| **Sektörel Regülatör** | Fiyat tavanları, lisans koşulları, kapasite kısıtlamaları | Yukarıdaki tabloya göre |
| **AB Düzenlemeleri** | CBAM, anti-damping, Gümrük Birliği, dijital düzenleme | `web_search "EU [sector] regulation Turkey"` |
| **Vergi/Teşvik** | Sektörel vergi değişiklikleri (ÖTV, KDV), yatırım teşvikleri | Resmi Gazete, Hazine |

---

## Düzenleyici Risk Ölçeği

| Seviye | Tanım | Çıktı Etkisi |
|--------|-------|-------------|
| **Yüksek** | Aktif soruşturma, tarife değişikliği gündemde, lisans riski | Porter skoru değişir, DCF'te risk primi ekle |
| **Orta** | Sektörel tartışmalar var ama somut düzenleme yok | Porter'da dipnot, DCF'te senaryo analizi |
| **Düşük** | Stabil düzenleyici ortam, son 3 yılda değişiklik yok | Standart analiz yeterli |

---

## Porter's Five Forces — Düzenleyici Entegrasyon

Her Porter faktöründe düzenleyici boyut AYRI DEĞERLENDİRİLİR:

1. **Rekabet Yoğunluğu** → Kartel soruşturmaları, koordineli fiyatlama bulguları
2. **Yeni Giriş Tehdidi** → Lisans gereklilikleri, sermaye eşikleri, regülatör onayı
3. **İkame Ürün Tehdidi** → Vergilendirme farkları (ÖTV: bira vs şarap vs rakı)
4. **Tedarikçi Gücü** → Hammadde düzenlemeleri, ithalat kısıtlamaları
5. **Müşteri Gücü** → Fiyat tavanları (enerji, ilaç), SGK geri ödeme oranları

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-02-11 | v1.0 CIMSA dersinden oluşturuldu |
| 2026-03-17 | v2.0 Sektör bazlı regülatör haritası, risk ölçeği, Porter entegrasyonu eklendi |
