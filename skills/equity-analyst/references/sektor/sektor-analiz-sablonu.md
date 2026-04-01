# Sector Overview — Sektör Analizi Şablonu

## Amaç

İlk kez bir sektöre girildiğinde veya kapsamlı sektör raporu hazırlanırken kullanılır. Quick analysis'teki sektör bölümünden daha derin — tam bir sektör haritası.

---

## Şablon

### 1. Pazar Büyüklüğü & Büyüme

```
## Sektör: [ADI]

### Pazar Büyüklüğü
| Ölçüm | Değer | Kaynak |
|-------|-------|--------|
| Global TAM | $X milyar | [Kaynak, yıl] |
| Türkiye TAM | X milyar TL | [Kaynak, yıl] |
| Türkiye SAM | X milyar TL | [Açıklama] |
| CAGR (global, 5Y) | %X | [Kaynak] |
| CAGR (Türkiye, 5Y) | %X | [Kaynak] |

### Pazar Segmentasyonu
| Segment | Payı (%) | Büyüme | Trend |
|---------|---------|--------|-------|
| [Segment 1] | %X | %X | ↑/→/↓ |
| [Segment 2] | %X | %X | ↑/→/↓ |
```

**Kaynak hiyerarşisi:** Sektör kuruluşları (TAPDK, TÇD, OSD, BTK) > Araştırma firmaları (Euromonitor, Mordor) > Web araştırma
**TAM hype uyarısı:** "Addressable market" ile gerçek "reachable market" arasındaki farkı belirt. Araştırma firmalarının TAM'ları genellikle şişirilmiştir.

---

### 2. Endüstri Yapısı

```
### Yoğunlaşma
- Top 5 pazar payı: %X (konsolide / parçalı / oligopol)
- HHI (Herfindahl): [Hesaplanabilirse]
- Yoğunlaşma trendi: [Konsolidasyon / stabil / parçalanma]

### Değer Zinciri
[Hammadde → Üretim → Dağıtım → Perakende → Tüketici]
- Değer nerede birikiyor? [Hangi katman en kârlı]
- Entegrasyon trendi: [Dikey / yatay / yok]

### İş Modeli Türleri
| Tür | Örnekler | Marj Profili |
|-----|----------|-------------|
| [Tür 1] | [Şirketler] | Brüt %X, FAVÖK %X |
| [Tür 2] | [Şirketler] | Brüt %X, FAVÖK %X |
```

---

### 3. Giriş Bariyerleri & Moat Kaynakları

```
### Giriş Bariyerleri
| Bariyer | Seviye (1-5) | Açıklama |
|---------|-------------|----------|
| Sermaye gereksinimi | X/5 | [Minimum yatırım miktarı] |
| Düzenleyici lisans | X/5 | [Hangi lisanslar gerekli] |
| Ölçek ekonomisi | X/5 | [Minimum verimli ölçek] |
| Marka/itibar | X/5 | [Marka geçmişi ne kadar önemli] |
| Teknoloji/know-how | X/5 | [Teknik bariyer] |
| Dağıtım ağı | X/5 | [Dağıtım kurma süresi/maliyeti] |

### Sektörde Yaygın Moat Türleri
[Hangi moat türü sektörde en geçerli — duopoly, regulatory, switching cost, vb.]
```

---

### 4. Porter's Five Forces (Düzenleyici Ortam Dahil)

```
### Porter Analizi

| Güç | Skor (1-5) | Gerekçe |
|-----|-----------|---------|
| Mevcut rekabet | X/5 | [Düzenleyici bulgular dahil] |
| Yeni giriş tehdidi | X/5 | [Bariyerler referansıyla] |
| İkame ürün | X/5 | [Alternatif ürün/hizmetler] |
| Tedarikçi gücü | X/5 | [Tedarik konsantrasyonu] |
| Müşteri gücü | X/5 | [Müşteri konsantrasyonu] |
| **Genel Çekicilik** | **X/10** | |

⚠️ Düzenleyici ortam taraması ZORUNLU → references/ortak/duzenleyici-ortam-taramasi.md
```

---

### 5. Rekabet Haritası

```
### Pazar Payı Dağılımı

| Şirket | Pazar Payı (%) | Trend (3Y) | Stratejik Konum |
|--------|---------------|-----------|----------------|
| [Şirket 1] | %X | ↑/→/↓ | [Lider/Takipçi/Niche] |
| [Şirket 2] | %X | ↑/→/↓ | [Lider/Takipçi/Niche] |

### Pozisyonlama Matrisi (opsiyonel)
İki temel rekabet boyutunu seç ve 2×2 matris çiz:
- Fiyat × Kalite
- Ölçek × Uzmanlaşma
- Yerel × Global
- Dijital × Geleneksel
```

---

### 6. Trendler & Sürücüler

```
### Sekülyer Trendler (3-5 yıl+)
1. [Trend 1] — etki ve süre
2. [Trend 2] — etki ve süre
3. [Trend 3] — etki ve süre

### Rüzgâr Arkası (Tailwinds)
- [Olumlu faktör 1]
- [Olumlu faktör 2]

### Rüzgâr Önü (Headwinds)
- [Olumsuz faktör 1]
- [Olumsuz faktör 2]

### Düzenleyici Gelişmeler
- [Mevcut/beklenen düzenleme 1]
- [Mevcut/beklenen düzenleme 2]
```

---

### 7. Değerleme Bağlamı

```
### Sektör Çarpanları

| Çarpan | Güncel | 5Y Ort. | 5Y Min | 5Y Max | Not |
|--------|--------|---------|--------|--------|-----|
| EV/EBITDA | Xx | Xx | Xx | Xx | |
| P/E | Xx | Xx | Xx | Xx | |
| FD/Hasılat | Xx | Xx | Xx | Xx | |

### Premium/İskonto Sürücüleri
- Büyüme: Yüksek büyüme = premium
- Marj: Yüksek marj = premium
- Moat: Güçlü moat = premium
- Yönetişim: İyi yönetişim = premium (BIST'te özellikle önemli)

### M&A Geçmişi (varsa)
| Tarih | Alıcı | Hedef | EV/EBITDA | Not |
|-------|-------|-------|-----------|-----|
```

---

### 8. Yatırım İmplikasyonları

```
### Risk/Getiri Değerlendirmesi
- Sektörde en iyi risk/getiri nerede?
- Hangi tematik tezler bu sektörle ifade edilebilir?
- Temel tartışma (bull vs bear) nedir?

### Katalizörler
- [Olası katalizör 1 ve zamanlaması]
- [Olası katalizör 2 ve zamanlaması]
```

---

## Kullanım Notları
- Bu şablonun tamamının doldurulması gerekmez — sektöre göre ilgili bölümler genişletilir, ilgisiz olanlar kısaltılır
- Kaynak belirtilmeyen rakam yazılmaz
- Sektör-spesifik metrikler için → `references/ortak/bist-sektor-metrikleri.md`
- Düzenleyici tarama için → `references/ortak/duzenleyici-ortam-taramasi.md`
