# DATA_PACK Şablonu — Faz 1 Çıktısı

## Faz 0 — 5 Dakikalık Ön Kontrol Listesi

> Her DCF'in en başında yapılacak hızlı kontrol. Bu liste tamamlanmadan Faz 1'e GEÇİLMEZ.

```
□ Şirket adı, ticker, sektör
□ KAP'tan ortaklık yapısı (birincil kaynak) — [DOĞRULANMADI] etiketi yoksa DURMA
□ Para birimi kararı (FX gelir payı)
□ Son çeyrek/yıl hangisi? → TTM hesaplanacak mı?
□ Faaliyet raporu erişilebilir mi? (PDF açılıyor mu, metin çıkarılabiliyor mu?)
□ KAP API çalışıyor mu? → python3 bbb_kap.py {TICKER} --kap-summary
□ Şirketin yatırımcı ilişkileri sayfası var mı? URL not et.
□ Yerli + yurt dışı en az 4-5 peer belirle
```

**⚠️ KAP API erişilemiyorsa → Odesus'a bildir, alternatif çözüm üret (browser tool, Can desteği). "Doğrulanamadı" yazıp geçme!**

---

## Faz 1 Veri Toplama Adımları

**Her adımda kaynak ve komut belirtilir. Adım atlanırsa Faz 2'ye GEÇİLMEZ.**

### ADIM 1: KAP Finansal Tablolar (ZORUNLU — İLK YAPILACAK İŞ)
```bash
cd ~/.openclaw/workspace-can/skills/bbb-finans/scripts
python3 bbb_kap.py {TICKER} --kap-summary       # Bilanço + Gelir (4 dönem)
python3 bbb_financials.py {TICKER} --full              # 147 kalem detay
python3 bbb_financials.py {TICKER} --dcf --json        # DCF input verileri
```

### ADIM 2: Faaliyet Raporları (ZORUNLU)
- KAP'tan son **yıllık** faaliyet raporu (PDF) → oku, özetle
- KAP'tan son **çeyrek** faaliyet raporu (PDF) → oku, karşılaştır
- Odak: CEO mektubu, segment gelirleri, capex planları, risk faktörleri, ilişkili taraf işlemleri

### ADIM 3: Şirket Yatırımcı İlişkileri (ZORUNLU)
- Şirket web sitesi → Yatırımcı İlişkileri bölümü → en güncel yatırımcı sunumları
- USD/EUR bazlı raporlama varsa indir (IAS 29 ülkeleri için KRİTİK)
- Ortaklık yapısı, yönetim kurulu, bağımsız üye oranı

### ADIM 4: Rekabet Analizi (ZORUNLU)
- **Yerli rakipler:** KAP'tan rakip şirketlerin finansallarını çek
- **Yurt dışı eşlenikler:** Yahoo Finance skill ile global peer'ları analiz et
- Minimum 4-5 peer (yerli + yabancı karışımı)
- Karşılaştırma: Gelir, EBITDA marjı, EV/EBITDA, ROIC, Net Borç/EBITDA

### ADIM 5: Sektör & Makro Veriler
- Sektör raporları (güvenilir dış kaynaklar)
- TCMB verileri: faiz, enflasyon beklentisi
- Damodaran: beta, ERP, CRP → web'den güncel tablo

### ADIM 6: Piyasa Verileri
- Hisse fiyatı, piyasa değeri → BBB Finans / Yahoo Finance
- Döviz kuru → TCMB
- CDS spread → web araştırma

### ADIM 7: TTM Hesaplama (Son çeyrek varsa ZORUNLU)
- Son çeyrek kümülatif + (önceki FY - önceki aynı çeyrek kümülatif)
- Bilanço: son çeyrek sonu değerleri

---

## DATA_PACK Dosya Şablonu

```markdown
# {TICKER} — Veri Paketi (DATA_PACK)
## Değerleme Tarihi: YYYY-MM-DD
## Para Birimi: [USD / TL]
## Döviz Kuru: [X.XX] (Kaynak: TCMB, Tarih: YYYY-MM-DD)
## Veri Kaynağı: KAP (birincil) + İş Yatırım (cross-check)

### 1. Şirket Profili (Faaliyet raporundan)
### 2. Finansal Tablolar — KAP (5Y + TTM)
### 3. Marj & Oran Analizi
### 4. Rekabet Analizi (yerli + yurt dışı peer'lar)
### 5. Sektör Analizi
### 6. WACC Ham Verileri (Beta, ERP, CDS, Rating, D/E)
### 7. Faaliyet Raporu Özeti (yıllık + çeyrek + yatırımcı sunumları)
### 8. Pay Bilgisi & Piyasa Verisi

---

## EBIT TANIMI DOKÜMANTASYONU (IAS 29 Şirketleri İçin ZORUNLU)

> **Neden zorunlu?** IAS 29 uygulayan BIST şirketlerinde gelir tablosundaki "EBIT" tanımı parasal pozisyon kazanç/kaybını içerebilir veya içermeyebilir. Bu tek fark, EBIT marjını 5-10pp değiştirebilir ve DCF sonucunu %40-60 etkileyebilir.

### Faz 1'de Zorunlu Çıktı: EBIT Köprüsü

```
## {TICKER} — EBIT Tanımı ve Köprüsü

### Son Dönem (FY/TTM): [dönem belirt]

| Kalem | Tutar (mn TL) | Marj (Gelire %) |
|-------|--------------|-----------------|
| Brüt Kâr | X | %Y |
| (−) Genel Yönetim + Pazarlama Giderleri | (A) | |
| (=) Çekirdek EBIT | B | %C |
| (−) Diğer Faaliyet Giderleri (net) | (D) | |
|   → Bunun içinden: Parasal Pozisyon Kaybı | (E) | |
|   → Bunun içinden: Diğer (kur farkı, değer düşüklüğü vb.) | (F) | |
| (=) GAAP EBIT (gelir tablosu) | G | %H |

### DCF İçin Kullanılacak EBIT

□ GAAP EBIT (parasal kayıp DAHİL) — Gerekçe: [...]
□ Operasyonel EBIT (parasal kayıp HARİÇ) — Gerekçe: [...]
□ Çekirdek EBIT (tüm Diğer Faal. HARİÇ) — Gerekçe: [...]

Seçilen: [X] — Marj: %Y
```

**⚠️ Faz 2'ye bu tablo OLMADAN geçiş YASAKTIR.** Faz 2'deki EBIT projeksiyonları bu tanıma göre yapılacak.

### IAS 29 Olmayan Şirketler

IAS 29 uygulamayan şirketlerde genellikle tek EBIT tanımı vardır. Bu durumda:
- Köprü tablosu basitleştirilir (Diğer Faaliyet ayrıştırması opsiyonel)
- Ancak one-off kalemlerin (varlık satışı, değer düşüklüğü) EBIT'ten arındırılması yine zorunludur

---

## ÖNERİLEN VARSAYIM SETİ (Faz 2 için — ONAY BEKLİYOR)

| Parametre | Önerilen Değer | Gerekçe |
|-----------|---------------|---------|
| Gelir büyümesi Y1 | X% | ... |
| Gelir büyümesi Y2-5 CAGR | X% | ... |
| Gelir büyümesi Y6-10 CAGR | X% | ... |
| Hedef EBIT marjı | X% | Peer medyan: Y%, tarihsel: Z% |
| Yakınsama yılı | N | ... |
| Sales/Capital (1-5) | X | Tarihsel ortalama: Y |
| Sales/Capital (6-10) | X | ... |
| Risksiz oran (Rf) | X% | Kaynak: ... |
| ERP (mature) | X% | Kaynak: ... |
| CRP | X% | Kaynak + hesaplama: ... |
| Beta (β_U) | X | Yöntem + cross-check: ... |
| Borç maliyeti (Kd) | X% | Rating: ... |
| D/E (piyasa) | X% | MCap: ..., Borç: ... |
| Efektif vergi (normalize) | X% | ... |
| Terminal büyüme (g) | X% | ... |
| Terminal ROC | X% | ... |
| Batma olasılığı | X% | ... |
```

---

## FAZ 1.5 PARAMETRE TUTARLILIK KONTROLLARI — ZORUNLU

> **Amaç:** Parametreler kilitlenmeden ÖNCE iç tutarlılığı kontrol et. Faz 2'den sonra düzeltmek çok pahalı.
> Bu kontroller her Faz 1.5'te TEK TEK yapılır ve sonuçları İlker'e sunulur.

### Kontrol 1: Terminal ROC vs Terminal WACC Spread'i

```
Spread = Terminal ROC - Terminal WACC

| Spread    | Yorum                          | Aksiyon                                    |
|-----------|--------------------------------|--------------------------------------------|
| ≤ 0       | Büyüme değer yaratmıyor/yıkıyor| Kabul edilebilir (muhafazakâr). g=0 düşün. |
| 0-2pp     | Hafif moat                     | ✅ Makul — kısa gerekçe yeterli            |
| 2-5pp     | Orta moat                      | ⚠️ Gerekçe zorunlu (pazar payı, marka, PL)|
| >5pp      | Güçlü moat iddiası             | 🔴 Detaylı moat analizi zorunlu            |
|           |                                | BIMAS/COCA-COLA seviyesi mi? Kanıtla.      |
```

**Sektör cross-check:** Terminal ROC, Damodaran sektör ROIC ortalamasından >2x yukarıdaysa → açıklama zorunlu.

### Kontrol 2: Terminal Büyüme vs WACC

```
g ≥ WACC       → ENGELLE (matematiksel imkansızlık)
g ≥ Rf          → UYAR (ekonomiden hızlı büyüyorsun)
g > Reel GDP    → UYAR (sektör neden ekonomiden hızlı büyür?)
WACC - g < 3pp  → UYAR (TV çok hassas — küçük g değişimi büyük etki)
```

### Kontrol 3: Y1 Büyüme vs Terminal Büyüme Tutarlılığı

```
Y1 büyüme / Terminal büyüme > 5x   → UYAR (çok agresif yavaşlama)
Y1 büyüme / Terminal büyüme < 1.5x → UYAR (neden büyüme düşmüyor?)
```

### Kontrol 4: Senaryo Aralığı Makullüğü

```
Bull WACC < Bear WACC              → ✅ (doğru yön)
Bull ROC > Bear ROC                → ✅ (doğru yön)
Bull hedef / Bear hedef > 3x       → UYAR (çok geniş aralık, varsayımları daralt)
Bull hedef / Bear hedef < 1.3x     → UYAR (senaryolar anlamlı fark yaratmıyor)
```

### Kontrol 5: Kd Kaynak Tutarlılığı

```
|Sentetik Kd - Gerçek Kd (reel)| > 10pp → UYAR (Damodaran vs piyasa farkı raporlanmalı)
Kd > Ke                               → 🔴 (borç özsermayeden pahalı — anormal, kontrol et)
```

### Kontrol 6: Çelişki Matrisi Doğrulaması (equity-analyst T3 Ön Kontrol'den)

```
Çelişki matrisi dosyası mevcut mu?     → research/companies/{TICKER}/{TICKER}_celiski_matrisi.md
Matris en az 2 çelişki tespit etti mi?  → EVET ise devam, HAYIR ise T3'e geri dön
Çelişkiler çözüm yolu içeriyor mu?      → Her ✗ hücresinde (a), (b) veya (c) çözümü var mı?
Varsayım revizyonu gerekli mi?          → Çözüm (a) ise ilgili parametreyi düzelt
```

**⛔ Bu kontrol başarısız olursa parametreler KİLİTLENMEZ.** equity-analyst T3 Ön Kontrol'e geri dön.

### Kontrol 7: Guidance Rekonsilasyonu (IAS 29 veya Reel/Nominal Farkı Olan Şirketlerde ZORUNLU)

```
Yönetim guidance mevcut mu?
  → HAYIR: "Firma rehberlik açıklamıyor" notu ile GEÇ.
  → EVET: Aşağıdaki rekonsilasyonu yap.

1. Guidance hangi birimde? (Nominal / IAS 29 Dec YYYY / Reel / USD)
2. DCF hangi birimde? (Reel Dec YYYY / Nominal / USD)
3. Birimler FARKLI ise → guidance'ı DCF birimine çevir:
   Reel Eşdeğer = Guidance_Nominal / (1 + π_beklenen)
   π = Şirketin kendi enflasyon varsayımı VEYA TCMB beklenti anketi
4. DCF Y1 projeksiyonu ile çevrilmiş guidance'ı karşılaştır:
   Sapma = (DCF_Y1 / Guidance_Reel - 1) × 100
5. Sapma > %15 → UYARI: Sapma yönünü ve sebebini açıkla.
   "DCF guidance'ın %X üstünde çünkü [tarihsel momentum / pazar payı kazanımı / ...]"
   VEYA "DCF guidance'ın %X altında çünkü [makro baskı / rekabet / ...]"
6. Sapma kontrol edilmeden parametreler KİLİTLENMEZ.

ÖRNEK (EBEBK):
  Guidance: 37B TL nominal (şirketin %25 enflasyon varsayımı)
  Reel eşdeğer: 37 / 1,25 = 29,6B TL → ima edilen reel büyüme %7
  DCF Y1: 31,8B TL reel → %15 reel büyüme
  Sapma: +%7,5 → DCF guidance'ın üstünde.
  Neden: FY2025 reel büyüme %15,4; momentum varsayımı. Şirket muhafazakar guidance veriyor (tarihsel %4-6 beat).
```

**⛔ Guidance sapması açıklanmadan parametreler KİLİTLENMEZ.** Sapma bilinçli bir karar olmalı, fark edilmemiş bir tutarsızlık değil.

---

## Token Bütçesi Tahmini

| Faz | Tahmini Token | Açıklama |
|-----|--------------|----------|
| Faz 1 | 80-120K | Web fetch + veri toplama en büyük tüketici |
| Faz 1.5 | ~5K | Orchestrator review |
| Faz 2 | 50-80K | Hesap kompakt, veri zaten dosyada |
| Faz 3 | 50-80K | 17 soru + sanity check + olası revizyon |
