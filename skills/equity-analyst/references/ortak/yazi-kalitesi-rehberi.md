# Yazım Kalitesi Rehberi — Fikir İnşası Standartı v1.0

> Goldman Sachs, Bernstein, Damodaran Blog'unun farkı rakam üretimi değil — fikir inşasıdır.
> Bu rehber "nasıl yazarım?" değil, "nasıl düşünürüm ve bunu nasıl aktarırım?" sorusuna cevap verir.
> Tüm T5 çıktıları bu standartı karşılamalıdır.

---

## Temel Prensip: İçgörü Merdiveni

Her finansal analiz ifadesi şu merdivenin bir basamağında durur. **Biz en az Seviye 3'te konuşuruz.**

```
Seviye 1 — VERİ:        "TBORG'un geliri 2024'te 18.4 milyar TL oldu."
Seviye 2 — GÖZLEM:      "TBORG'un geliri 2024'te %47 büyüdü."
Seviye 3 — İÇGÖRÜ:      "TBORG'un büyümesinin %35'i hacim değil fiyat artışından geldi — bu duopol fiyatlama gücünün kanalın arkasındaki onayıdır."
Seviye 4 — İMPLİKASYON: "ÖTV artışını rakiplerle eş zamanlı geçirme kapasitesi, marjın yapısal olduğunu — döngüsel değil — gösteriyor."
Seviye 5 — AKSİYON:     "Terminal marjı %18 değil %21 almak için somut gerekçe bu. Consensus bu farkı fiyatlamıyor."
```

**Kural:** Sadece Seviye 1-2'de kalmak = veri girişi, analistlik değil.

---

## 1. Argüman İnşa Yapısı

### 1A. Tez Pillar'ı Nasıl Yazılır?

Her pillar üç bileşenden oluşur:

```
[İDDİA] + [KANIT] + [NEDEN ÖNEMLİ?]
```

**Kötü örnek:**
> "TBORG güçlü pazar payına sahip ve duopol yapı koruyor."

**İyi örnek:**
> "TBORG'un %50 pazar payı, son 5 yılda ±2pp aralığında kalmıştır — bu sadece güç değil, yapısal bir denge noktasıdır. AEFES'in 2022 Rusya krizinde bile bu oran kırılmadı; ithal üreticiler %4-5'in altında takılı kaldı. Duopol fiyatlama gücünün somut kanıtı: sektördeki son 4 ÖTV artışının tamamı 2 ay içinde perakende fiyata yansıdı, marj erozyonu yaşanmadı. Bu, giriş bariyerinin ne kadar yüksek olduğunu — dağıtım ağı + soğuk zincir altyapısı + marka sadakati — gösteriyor."

---

### 1B. "Consensus Nerede Yanılıyor?" Çerçevesi

Her tez için sor: **Piyasa ne düşünüyor? Ben neden farklı düşünüyorum?**

Bu soruyu cevaplayamazsan tezin fikir değil, konsensüs tekrarıdır.

```
Consensus görüşü: [Piyasanın mevcut beklentisi — spesifik rakamla]
Bizim görüşümüz: [Fark nerede, ne kadar büyük]
Neden consensus yanılıyor: [Gözden kaçırdıkları spesifik faktör]
Nasıl ortaya çıkacak: [Katalizör ve zaman dilimi]
```

**Örnek:**
```
Consensus görüşü: TBORG için 2025 gelir büyümesi konsensüs %28, FAVÖK marjı %17.5.
Bizim görüşümüz: Gelir büyümesi %32, FAVÖK marjı %20.1.
Neden consensus yanılıyor: Ruhsat adet kısıtı TAPDK'nın kararıyla 2024'te fiilen donduruldu.
  Yeni giricilerin 2025 hacim katkısı consensus'ın varsaydığı %3 değil, <%1.
  Ayrıca premium segment karmasının marj üzerindeki 240bp katkısı modellere girmiyor.
Nasıl ortaya çıkacak: Q1 2025 sonuçları ve TAPDK yıllık ruhsat verisi (Mart).
```

---

### 1C. Bull vs. Bear — Gerçek Denge

Kötü analist: Sadece bull case yazar, bir paragraf "riskler" ekler.
İyi analist: Bear case'i, bull case kadar titizlikle yazar.

**Yapı:**

```
## Bull Tezi
[Gerçekleşirse ne olur — spesifik sayılarla]

## Bear Tezi
[Gerçekleşirse ne olur — spesifik sayılarla, aynı uzunlukta]

## Neden Bull'da Duruyoruz?
[İki tez arasındaki fark nedir? Olasılık ağırlıklandırması neden bu yönde?]
```

**Kritik kural:** Bear case'i küçümseme. "Hisse zaten ucuz, düşme riski sınırlı" gibi ifadeler kabul edilmez. En kötü senaryoda ne olur? Sayılarla yaz.

---

## 2. Yazım Dili Standartı

### 2A. Spesifik Ol — Her Zaman

| ❌ Yanlış | ✅ Doğru |
|-----------|---------|
| "Güçlü büyüme bekliyoruz" | "FY2026 gelirinin %31 büyüyeceğini tahmin ediyoruz" |
| "Marjlar iyileşti" | "EBIT marjı 5 yılda 380bp genişledi: 2019'da %13.2, 2024'te %16.8" |
| "Değerleme cazip" | "EV/FAVÖK'ü 7.2x, 5 yıllık tarihsel ortalaması 9.8x — %26 iskonto" |
| "Riskler mevcut" | "Lisans sayısının iki katına çıkması pazar payını %42'ye basabilir; bu senaryoda hedef fiyat 48 TL" |
| "Yönetim kaliteli" | "Son 4 yılda açıklanan 3 major guidance'ın ortalama sapması -%3.2 — muhafazakâr ancak güvenilir" |

### 2B. Damodaran Tonu — Hem Teknik Hem Anlaşılır

Damodaran'ın blog yazıları referans: teknik terim doğru kullanılır, ama her kişi anlayabilir.

**Kural:** Bir terimi kullanıyorsan, ilk geçişte parantez içinde kısa tanımla.
> "Sales/Capital oranı (yatırılan her TL sermaye için kaç TL gelir üretiliyor) 5 yılda 2.1x'ten 1.8x'e geriledi — sermaye verimliliğinde yapısal baskı var."

### 2C. Sayısal Kesinlik

- Para birimi ve zaman dilimi her zaman belirtilir: "12.4 milyar TL (FY2024)"
- Büyüme rakamları nominal/reel ayrımı ile: "%47 nominal, ~%8 reel (2024 TÜFE %65 baz)"
- Çarpan karşılaştırmalarında peer ortalaması zorunlu: "EV/FAVÖK 7.2x (sektör medyanı 9.1x)"

---

## 3. Yapısal Kurallar — Bir Raporu Oluşturan Bölümler

### 3A. Başlık Kuralı: İçgörü Başlığı Zorunlu

| ❌ Yanlış | ✅ Doğru |
|-----------|---------|
| "Rekabet Analizi" | "Duopol Yapısı Yeni Girişimcilere Kapalı Kapıyı Koruyor" |
| "Finansal Analiz" | "Marj Genişlemesi Hacim Değil Fiyat Gücünden Geliyor — Yapısal" |
| "Değerleme" | "Consensus %26 İskonto Fırsatını Fiyatlamıyor" |
| "Riskler" | "İki Senaryo Tezi Çöker: Lisans Patlaması veya İthalat Serbestisi" |

**Başlık testi:** Başlığı okuyunca "bu hisseyi al/alma" yönünde bir fikir oluşuyor mu? Oluşmuyorsa yeniden yaz.

### 3B. Paragraf Yapısı

Her paragraf bir fikri taşır. Üç yapı:

**Yapı A — Deductive (Genel→Özel):**
```
[Ana iddia] → [Kanıt 1] → [Kanıt 2] → [Sonuç/İmplikasyon]
```
> "Premium segment TBORG'un marj genişlemesinin motoru. 2021'de %18 olan premium pay 2024'te %29'a çıktı. Birim FAVÖK'ü standart segment bira maliyet baskısına karşı ortalama %40 daha yüksek. Karması değişmeye devam ederse terminal marj consensus'ın 180-240bp üzerinde çıkacak."

**Yapı B — Inductive (Özel→Genel):**
```
[Anomali/Veri noktası] → [Pattern] → [İma Edilen Gerçek]
```
> "TBORG 2021-2024 döneminde 4 ÖTV artışını 8 haftadan kısa sürede perakende fiyata yansıttı. Aynı dönemde rakipler 14-22 hafta aldı. Bu fark tesadüf değil: dağıtım ağının derinliği + marka sadakati birleşince fiyat geçirgenliği bu kadar hızlı olabiliyor. Bu, fiyatlama gücünün sektördeki en güçlü kanıtlarından biri."

**Yapı C — Contrast (Beklenti vs Gerçek):**
```
[Piyasanın beklentisi] → [Gerçekte olan] → [Fark neden önemli?]
```
> "2022'de consensus gelir büyümesinin %12 yavaşlayacağını bekliyordu — Rusya etkisi, global belirsizlik, hammadde maliyeti. Gerçekleşme: %24 büyüme. Fark neden? Domestik talebin enflasyona karşı bu kadar dirençli olduğunu kimse modellemedi. Alkollü içeceklerin fiyat esnekliği —0.3 ile —0.6 arasında: fiyat ikiye katlansa bile tüketim %30-60 düşüyor, yani talep kalıcı."

### 3C. Geçiş Cümleleri — Bölümler Arası Köprü

Bölümler arasında bağlantı zorunlu. "Bir sonraki bölümde..." değil, fikri ilerlet:

> "Moat analizimiz duopol yapının kalıcı olduğunu gösteriyor. Bu, finansal model için kritik bir önkabul: terminal büyüme oranını sektör büyümesinin altında almak yerine paralel alabiliriz, çünkü pazar payı riski minimuma indi."

---

## 4. Kontraryen Fikir Standartı

### 4A. Kontraryen Fikir Nedir, Ne Değildir?

**Kontraryen DEĞİL:**
- "Hisse düştü, dolayısıyla ucuz."
- "Piyasa aşırı tepki verdi." (Kanıtsız)
- "Uzun vadede toparlar." (Her şey uzun vadede toparlar)

**Gerçek Kontraryen:**
- "Consensus yanlış bir şeyi hesaba katıyor — işte kanıtı ve ölçüsü."
- "Piyasa şu faktörü görmezden geliyor — işte neden ve ne zaman fark edilecek."
- "Bu fiyat, hangi büyüme oranını ima ediyor? Bu büyüme gerçekçi mi, değil mi?"

### 4B. Ters İNA — Kontraryen Düşüncenin Aracı

Mevcut fiyatı alıp ne büyümeyi fiyatladığını hesapla:

```
Mevcut Hisse Fiyatı: 155 TL
Ters İNA sorusu: Bu fiyat hangi büyümeyi fiyatlıyor?
Hesaplama: WACC %14, terminal büyüme %4, terminal marj %17 sabitleyince
           gelir büyümesi %8 çıkıyor.
Değerlendirme: Tarihsel 5Y büyüme %22, sektör büyümesi %14.
               Piyasa yapısal büyüme hikayesini görmezden geliyor.
```

Bu analiz olmadan "ucuz" iddiası boştur.

---

## 5. Özel Durum Yazım Kuralları

### 5A. İlk Kez Kapsama (Initiation) — Tez Manifestosu Tonu

Initiation raporu bir manifesto gibi yazılır. Okuyucu şunu hissetmeli: "Bu analist bu şirketi gerçekten anlıyor ve benim duymadığım bir şeyi söylüyor."

**İlk paragraf standardı:** Bir metafor veya anomali ile aç, sonra direkt teze gir.

> "Türkiye'de bir bira içmek istediğinizde iki markayla karşı karşıyasınız. Lisans dondurulmuş, ithal markaların rafları %4-5'te takılı. Bu tesadüf değil — 30 yıllık altyapı yatırımı, dağıtım tekeli ve marka sadakatinin oluşturduğu bir duvar. TBORG bu duvarın iki inşaatçısından biri; ve bu analizde, piyasanın görmezden geldiği bir şeyi bulduğumuzu düşünüyoruz: terminal marjın consensus'ın %18'i değil, %21 olacağını."

### 5B. Çeyreklik Güncelleme — "Ne Değişti?" Odağı

Çeyreklik güncelleme geçmişi tekrar etmez, **delta'yı** yazar.

Kötü açılış: "TBORG'un bira sektöründe güçlü konumu..."
İyi açılış: "Q4 2024 beklentimizden 190bp daha yüksek FAVÖK marjı ile geldi. Fark nerede oluştu ve bu tezimizi nasıl etkiliyor?"

**Delta yazım kuralı:**
```
Beklenti: [Ne bekliyorduk, sayıyla]
Gerçekleşme: [Ne oldu, sayıyla]
Fark neden: [1-2 spesifik faktör]
Teze etkisi: [Güçlendirdi mi, zayıflattı mı, conviction değişti mi?]
```

### 5C. Risk Bölümü — Dürüst Ol

Risk bölümü "yatırımcıyı ürkütmeme" amaçlı yazılmaz. Amacı: gerçek riskleri, gerçek ölçüsüyle göstermek.

**Risk yazım standardı:**

| ❌ Kabul Edilmez | ✅ Standart |
|-----------------|------------|
| "Makroekonomik belirsizlik risk oluşturabilir" | "Enflasyonun %35'in üzerinde kalması durumunda tüketici bütçesi baskısı hacimleri %8-12 aşağı çekebilir; bu FAVÖK'ü ~1.8 milyar TL etkiler" |
| "Rekabet artabilir" | "Yeni lisans izni verilmesi halinde 3. büyük oyuncu TAPDK verilerine göre 2 yılda %6-8 pay alabilir; bu durumda hedef fiyatımız 48 TL'ye geriler" |
| "Regülasyon riski var" | "ÖTV oranının %25 artması, geçmiş veriye göre, 3 ay içinde tam geçiş sağlansa bile hacimi geçici olarak %5-7 düşürür" |

---

## 6. Yasak Karakterler ve Format Kısıtlamaları

### 6A. Rapor Metninde Yasak Özel Karakterler

Profesyonel equity research raporlarında (JP Morgan, Goldman Sachs, Morgan Stanley referans) belirli karakterler düzyazı akıcılığını bozar ve "kısayol" hissi verir. Bu karakterler **rapor gövde metninde YASAKTIR.**

| Karakter | Ad | Yasak mı? | Alternatif |
|----------|-----|-----------|-----------|
| — | Em dash | **YASAK** (rapor metni) | Noktalı virgül (;), virgüllü yeni cümle veya parantez |
| → | Arrow | **YASAK** (rapor metni) | "X'ten Y'ye", "X seviyesinden Y seviyesine geriledi/yükseldi" |
| ▲ ▼ | Üçgen simge | Sadece tablo içi | Rapor metninde YASAK |
| – | En dash | **YASAK** | Noktalı virgül veya "ile" bağlacı |

**Örnekler:**

| ❌ Yasak | ✅ Doğru |
|----------|---------|
| "FAVÖK marjı %3,4→%12,8" | "FAVÖK marjı %3,4'ten %12,8'e yükseldi" |
| "CEO geçişi — kurucu ayrıldı" | "CEO geçişi kurucunun ayrılmasını beraberinde getirdi" |
| "Demografik risk — TDH 2,19→1,48" | "Demografik baskı ciddi boyuttadır; toplam doğurganlık hızı 2,19'dan 1,48'e gerilemiştir" |
| "Stok devir hızı 86→68 gün — iyileşme" | "Stok devir hızı 86 günden 68 güne inerek belirgin iyileşme göstermiştir" |
| "Üç faktör: (1) X — (2) Y — (3) Z" | "Üç faktör öne çıkmaktadır. Birincisi, X. İkincisi, Y. Üçüncüsü, Z." |

**İstisna:** Tablo başlıkları (Tablo N —) ve grafik başlıkları (Grafik N —) em dash kullanabilir; bunlar düzyazı değil, etiket formatıdır.

**Kontrol:** Assembly tamamlandıktan sonra DOCX metninde em dash ve arrow sayısı 0 olmalıdır (tablo/grafik başlıkları hariç).

### 6B. Paragraf Başında Bold Lead-In

Her analitik paragrafın ilk 3-8 kelimesi koyu (bold) olmalıdır. Bu format, okuyucunun sayfayı tarayarak kilit bulguları hızla yakalamasını sağlar. JP Morgan ve Goldman Sachs raporlarında standart uygulamadır.

**Format:** `**[Konu veya Bulgu]:** Normal cümle devamı...`

**Örnekler:**
- **Bilanço güçlüdür:** Nakit 2,34 mrd TL, net borç sadece 333M TL...
- **Stok optimizasyonu çalışmaktadır:** CCC negatife dönmüş olup perakende için ideal...
- **Terminal değer kontrolü:** Terminal değerin toplam içindeki payı %49,1 olup kabul edilebilir...

**Kural:** Her bölümde en az ilk paragraf bold lead-in formatında olmalıdır. Tüm paragrafların bold lead-in olması zorunlu değildir; analitik yorum içeren paragraflar için öncelikli uygulanır.

---

## 7. İçerik Zenginleştirme (Post-Assembly Enrichment) Kuralları

Rapor assembly (T5 Faz G) sonrası kelime hedefine ulaşılamamışsa veya belirli bölümlerin analitik derinliği yetersizse, T1 research.md'den zenginleştirme yapılır. Bu sürecin kalitesi aşağıdaki kurallara bağlıdır:

### 7A. Tutarlılık Kontrolü
Her ek paragraf, mevcut paragraflarla çelişki ve tekrar açısından kontrol edilmelidir. Aynı fikri farklı kelimelerle tekrarlayan paragraflar duplicate kabul edilir ve kaldırılmalıdır.

### 7B. İçgörü Seviyesi Eşleştirme
Ek paragrafların İçgörü Merdiveni seviyesi, mevcut paragraflarla aynı veya daha yüksek olmalıdır. Seviye 1-2 (veri/gözlem) ek paragraf YASAKTIR; minimum Seviye 3 (İçgörü) olmalıdır.

### 7C. Stil Uyumu
Mevcut paragraflar hangi yazım yapısını kullanıyorsa (Deductive/Inductive/Contrast), ek paragraflar da aynı bölümün stiline uyum sağlamalıdır. Bir bölümde iki farklı yazım tonu göze çarpmamalıdır.

### 7D. Duplikasyon Tarama
Assembly tamamlandıktan sonra tekrar frekansı taranmalıdır:

**Kural:** Aynı veri noktasının TAM AÇIKLAMASI (2+ cümle, aynı bağlam ve sonuç) raporda MAX 2 kez geçebilir. Terim olarak bahsetme sınırsız.

**Tarama yöntemi:** DOCX açılır, Faz 0 Tekrar Haritası'ndaki 5 kilit fact için paragraf metni regex ile taranır, 3+ tam açıklama olanlar tespit edilir, fazlalıklar kısa referans + yeni perspektife dönüştürülür.

**İstisna:** icgoru_kutusu (TEMEL BULGU / DİKKAT) içindeki tekrarlar tolere edilir; bölüm girişi executive summary niteliğinde.

**Perspektif kontrolü:** Aynı fact farklı bölümde geçiyorsa, o bölüme özgü en az 1 yeni açı sunmalıdır (farklı metrik, farklı karşılaştırma, farklı zaman dilimi). Aynı cümle yapısı farklı bölümde geçmek YASAKTIR.

---

## 8. Sık Yapılan Yazım Hataları

| Hata | Çözüm |
|------|-------|
| **Pasif cümle** → "Büyüme beklenmektedir" | Aktif → "Büyümenin %X olacağını tahmin ediyoruz" |
| **Belirsiz özne** → "Analistler düşünüyor ki..." | Spesifik → "Consensus EV/FAVÖK 9.1x fiyatlıyor; biz 11.2x görüyoruz" |
| **Zayıf geçiş** → "Öte yandan..." | Fikir köprüsü → "Bu büyüme rakamları tek başına anlamsız; asıl soru hangi karlılıkla geliyor." |
| **Hedging** → "Bazı riskler mevcut olabilir" | Dürüst → "Bu tezin çökmesi için iki şey gerekiyor: [1] veya [2]" |
| **Ünlü alıntı ama köprüsüz** | Alıntıyı teze bağla, sonraki cümle doğrudan köprü |
| **Grafik açıklamasız** | Her grafik bir insight başlığı taşır, gövde metni grafiğin ne söylediğini yorumlar |

---

## 9. Kalite Kontrol — Son Okuma

T5 tamamlamadan önce şu soruları cevapla:

1. **Consensus farkı açık mı?** → "Piyasa %X beklentisinde, biz %Y görüyoruz" ifadesi var mı?
2. **Bear case yeterince güçlü yazılmış mı?** → Sadece 1 paragraf değil, spesifik sayılarla
3. **Her başlık içgörü taşıyor mu?** → "Rekabet Analizi" değil, sonuç ifadesi
4. **Tüm sayılar kaynaklı mı?** → `[DOĞRULANMADI]` etiketi yok
5. **Argüman merdiveni Seviye 3+ mı?** → Salt veri aktarımı yok, her bölümde "ne anlama geliyor?" var
6. **Kill criteria spesifik mi?** → Ölçülebilir, izlenebilir, kaçınılmaz değil

---

| Tarih | Değişiklik |
|-------|-----------|
| 2026-03-18 | v1.0 — Yazım kalitesi standartı. İçgörü merdiveni, argüman inşa yapısı, consensus farkı çerçevesi, bull/bear denge kuralı, kontraryen düşünce. |
| 2026-03-24 | v1.1 — §6 Yasak karakterler (em dash, arrow rapor metninde yasak) + Bold lead-in standardı. §7 İçerik zenginleştirme kuralları (tutarlılık, duplikasyon kontrolü, seviye eşleştirme). Bölüm numaraları güncellendi. |
