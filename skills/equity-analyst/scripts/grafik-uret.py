#!/usr/bin/env python3
"""
Grafik Üretici — Equity analiz grafikleri üretim aracı.

BBB renk paleti, Türkçe etiketler, 300 DPI (DOCX) / 150 DPI (web) standart.
Chart kataloğu ve detaylı rehber: references/c2-tam-kapsama/task4-grafik-uretim.md

Kullanım:
    # Modül olarak import
    from scripts import grafik_uret as gu
    gu.gelir_marj_grafigi(years, revenue, margin, 'THYAO', 'charts/THYAO_G02.png')

    # Komut satırından demo grafikler
    python grafik-uret.py --demo --ticker TBORG --cikti-klasor /tmp/demo_charts

    # Tek grafik türü
    python grafik-uret.py --tur football-field --veri veri.json --cikti grafik.png
"""

import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

try:
    import matplotlib
    matplotlib.use('Agg')  # Headless mod
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
except ImportError:
    print("matplotlib gerekli. Kur: pip install matplotlib", file=sys.stderr)
    sys.exit(1)

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

# ═══════════════════════════════════════════════════════════
# BBB STİL TANIMLARI
# ═══════════════════════════════════════════════════════════

plt.style.use('seaborn-v0_8-whitegrid')

# ── Sıcak Premium: Global matplotlib ayarları ──
SAYFA_BG = '#FFFFFF'   # v4.13: Beyaz arka plan — DOCX sayfa arka planı beyaz, grafikler de beyaz olmalı
plt.rcParams.update({
    'figure.facecolor': SAYFA_BG,
    'axes.facecolor': SAYFA_BG,
    'savefig.facecolor': SAYFA_BG,
    'grid.color': '#E0E0E0',         # v4.13: Nötr gri grid çizgileri (beyaz üzerinde görünür)
    'grid.alpha': 0.5,
    'axes.edgecolor': '#CCCCCC',     # v4.13: Nötr gri eksen çizgileri (beyaz uyumlu)
    'font.family': 'sans-serif',     # Arial — DOCX font ile senkron
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
})

BBB_RENKLER = {
    'birincil': '#f7931a',
    'ikincil': '#4d4d4d',
    'acik': '#BDD7EE',
    'pozitif': '#548235',
    'negatif': '#C00000',
    'uyari': '#FFC000',
    'notr': '#808080',
    'arka_plan': SAYFA_BG,           # v4.13: Beyaz — DOCX beyaz sayfa ile uyumlu
    'metin': '#333333',
}

BBB_PALET = ['#f7931a', '#4d4d4d', '#0d579b', '#329239', '#C00000', '#FFC000', '#7030A0', '#BDD7EE']

# Alias — yeni fonksiyonlar tutarlı isimler kullanır
RENKLER = {
    'birincil': BBB_RENKLER['birincil'],
    'ikincil': BBB_RENKLER['ikincil'],
    'acik': BBB_RENKLER['acik'],
    'acik_mavi': BBB_RENKLER['acik'],
    'olumlu': BBB_RENKLER['pozitif'],
    'olumsuz': BBB_RENKLER['negatif'],
    'uyari': BBB_RENKLER['uyari'],
    'metin': BBB_RENKLER['metin'],
}
RENKLER_TEXT = BBB_RENKLER['metin']

# Varsayılan boyutlar
VARSAYILAN_DPI = 300
DPI = 300
VARSAYILAN_GENISLIK = 10
VARSAYILAN_YUKSEKLIK = 6

# İsimli figsize sabitleri — kaynak her zaman büyük, ölçekleme DOCX engine'de yapılır
FIGSIZE_TAM   = (10, 6)    # 3000×1800px @ 300 DPI — tam sayfa genişliği
FIGSIZE_YARIM = (10, 6)    # Aynı kalite — DOCX'te 7.5cm'e ölçeklenir
FIGSIZE_GRID  = (8, 5)     # 2400×1500px — grid hücresi grafikler
FIGSIZE_KUCUK = (6, 4)     # 1800×1200px — küçük destekleyici grafikler
FIG_WIDTH = 10
FIG_HEIGHT = 6

# Font boyutları (+2pt — okunabilirlik iyileştirmesi)
BASLIK_BOYUT = 16
EKSEN_BOYUT = 12
ETIKET_BOYUT = 11
KAYNAK_BOYUT = 13
TITLE_SIZE = BASLIK_BOYUT
AXIS_SIZE = EKSEN_BOYUT
LABEL_SIZE = ETIKET_BOYUT
SOURCE_SIZE = KAYNAK_BOYUT


def _tamsayi_eksen(ax, eksen='x'):
    """X veya Y ekseninde sadece tam sayı tick'ler göster (2024.5 gibi ondalık tick'leri engeller)."""
    loc = mticker.MaxNLocator(integer=True)
    if eksen == 'x':
        ax.xaxis.set_major_locator(loc)
    else:
        ax.yaxis.set_major_locator(loc)


def _temiz_eksen(ax):
    """Üst ve sağ çizgileri kaldır, temiz görünüm."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def _kaynak_notu(fig, metin: str = 'Kaynak: KAP, BBB tahminleri'):
    """Grafiğin altına kaynak notu ekle. Negatif y ile figür dışına yerleşir, bbox_inches='tight' ile korunur."""
    fig.text(0.12, -0.02, metin, fontsize=KAYNAK_BOYUT - 2, style='italic', color='gray')


def _kaydet(fig, yol: str, dpi: int = VARSAYILAN_DPI):
    """Grafiği kaydet ve kapat. tight_layout ile kaynak notu alanı korunur."""
    Path(yol).parent.mkdir(parents=True, exist_ok=True)
    try:
        fig.tight_layout(rect=[0, 0.04, 1, 1])  # Alt %4 — kaynak notu figür dışında (-0.02)
    except Exception:
        pass
    fig.savefig(yol, dpi=dpi, bbox_inches='tight', facecolor='white')  # v4.13: explicit beyaz
    plt.close(fig)
    # RGBA → RGB dönüşümü (Word uyumluluğu)
    try:
        from PIL import Image
        img = Image.open(yol)
        if img.mode == 'RGBA':
            rgb = Image.new('RGB', img.size, (255, 255, 255))
            rgb.paste(img, mask=img.split()[3])
            rgb.save(yol, dpi=(dpi, dpi))
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════
# G02: GELİR & KÂRLILIK TRENDİ (Bar + Line Combo)
# ═══════════════════════════════════════════════════════════

def gelir_marj_grafigi(
    yillar: List,
    gelir: List[float],
    marj: List[float],
    ticker: str,
    kayit_yolu: str,
    marj_etiketi: str = 'FAVÖK Marjı',
    tahmin_baslangic: Optional[int] = None,
    kaynak: str = 'Kaynak: KAP, BBB tahminleri',
    dpi: int = VARSAYILAN_DPI,
):
    """G02 — Gelir barları + marj çizgisi overlay.

    Args:
        yillar: Yıl listesi [2020, 2021, ..., 2027]
        gelir: Gelir değerleri (mn TL)
        marj: Marj yüzdeleri (ondalık: 0.25 = %25)
        ticker: Hisse kodu
        kayit_yolu: PNG kayıt yolu
        marj_etiketi: Y ekseni etiketi (varsayılan: FAVÖK Marjı)
        tahmin_baslangic: Tahmin başlangıç yılı (dikey çizgi)
        kaynak: Kaynak notu metni
        dpi: Çözünürlük
    """
    fig, ax1 = plt.subplots(figsize=(VARSAYILAN_GENISLIK, VARSAYILAN_YUKSEKLIK))

    # Bar renkleri (tahmin yılları daha açık)
    if tahmin_baslangic:
        renkler = [BBB_RENKLER['acik'] if y >= tahmin_baslangic else BBB_RENKLER['ikincil'] for y in yillar]
    else:
        renkler = [BBB_RENKLER['ikincil']] * len(yillar)

    ax1.bar(yillar, gelir, color=renkler, alpha=0.85, edgecolor='white', label='Gelir')
    _tamsayi_eksen(ax1)
    ax1.set_ylabel('Gelir (mn TL)', fontsize=EKSEN_BOYUT, color=BBB_RENKLER['metin'])

    # Marj çizgisi
    ax2 = ax1.twinx()
    marj_pct = [m * 100 if m < 1 else m for m in marj]
    ax2.plot(yillar, marj_pct, color=BBB_RENKLER['negatif'], marker='o', linewidth=2.5,
             label=marj_etiketi, zorder=5)
    ax2.set_ylabel(f'{marj_etiketi} (%)', fontsize=EKSEN_BOYUT)

    # Tahmin ayırıcı
    if tahmin_baslangic:
        ax1.axvline(x=tahmin_baslangic - 0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax1.text(tahmin_baslangic - 0.3, max(gelir) * 0.95, 'Tahmin →', fontsize=9, color='gray')

    plt.title(f'{ticker} — Gelir & {marj_etiketi}', fontsize=BASLIK_BOYUT,
              fontweight='bold', color=BBB_RENKLER['birincil'], pad=15)
    fig.legend(loc='upper left', bbox_to_anchor=(0.12, 0.88), frameon=False)
    _temiz_eksen(ax1)
    _kaynak_notu(fig, kaynak)
    plt.tight_layout()
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G03: GELİR SEGMENT KIRILIMI (Stacked Area) ⭐
# ═══════════════════════════════════════════════════════════

def gelir_segment_grafigi(
    yillar: List,
    segmentler: Dict[str, List[float]],
    ticker: str,
    kayit_yolu: str,
    tahmin_baslangic: Optional[int] = None,
    kaynak: str = 'Kaynak: KAP, Şirket IR, BBB tahminleri',
    dpi: int = VARSAYILAN_DPI,
):
    """G03 — Gelir segmentasyonu stacked area chart.

    Args:
        segmentler: {'Segment A': [v1, v2, ...], 'Segment B': [...]}
    """
    fig, ax = plt.subplots(figsize=(VARSAYILAN_GENISLIK, VARSAYILAN_YUKSEKLIK))

    etiketler = list(segmentler.keys())
    degerler = list(segmentler.values())

    ax.stackplot(yillar, *degerler, labels=etiketler,
                 colors=BBB_PALET[:len(etiketler)], alpha=0.8)

    _tamsayi_eksen(ax)
    ax.set_ylabel('Gelir (mn TL)', fontsize=EKSEN_BOYUT)
    ax.set_title(f'{ticker} — Gelir Segment Kırılımı', fontsize=BASLIK_BOYUT,
                 fontweight='bold', color=BBB_RENKLER['birincil'], pad=15)
    ax.legend(loc='upper left', frameon=False)
    _temiz_eksen(ax)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    if tahmin_baslangic:
        ax.axvline(x=tahmin_baslangic - 0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)

    _kaynak_notu(fig, kaynak)
    plt.tight_layout()
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G31: PEER KARŞILAŞTIRMA (Horizontal Bar)
# ═══════════════════════════════════════════════════════════

def peer_karsilastirma_grafigi(
    sirketler: List[str],
    degerler: List[float],
    metrik_adi: str,
    hedef_ticker: str,
    kayit_yolu: str,
    birim: str = 'x',
    kaynak: str = 'Kaynak: BBB Finans, Yahoo Finance, KAP',
    dpi: int = VARSAYILAN_DPI,
):
    """G31 — Yatay bar, target şirket koyu renk ile vurgulanır."""
    fig, ax = plt.subplots(figsize=(VARSAYILAN_GENISLIK, max(4, len(sirketler) * 0.9)))

    renkler = [BBB_RENKLER['birincil'] if s == hedef_ticker else BBB_RENKLER['acik'] for s in sirketler]
    bars = ax.barh(sirketler, degerler, color=renkler, edgecolor='white', height=0.6)

    for bar, val in zip(bars, degerler):
        ax.text(bar.get_width() + max(degerler) * 0.02, bar.get_y() + bar.get_height() / 2,
                f'{val:.1f}{birim}', va='center', fontsize=ETIKET_BOYUT, fontweight='bold')

    # Medyan çizgisi
    medyan = np.median(degerler)
    ax.axvline(x=medyan, color=BBB_RENKLER['uyari'], linestyle='--', linewidth=1.5,
               label=f'Medyan: {medyan:.1f}{birim}')

    ax.set_title(f'{metrik_adi} — Peer Karşılaştırma', fontsize=BASLIK_BOYUT,
                 fontweight='bold', color=BBB_RENKLER['birincil'])
    ax.legend(loc='lower right', frameon=False)
    _temiz_eksen(ax)
    _kaynak_notu(fig, kaynak)
    plt.tight_layout()
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G32: DEĞERLEME FOOTBALL FIELD ⭐ (Horizontal Range Bars)
# ═══════════════════════════════════════════════════════════

def football_field_grafigi(
    yontemler: List[str],
    dusuk: List[float],
    yuksek: List[float],
    mevcut_fiyat: float,
    hedef_fiyat: float,
    kayit_yolu: str,
    para_birimi: str = 'TL',
    kaynak: str = 'Kaynak: BBB tahminleri',
    dpi: int = VARSAYILAN_DPI,
):
    """G32 — Değerleme aralıkları football field."""
    fig, ax = plt.subplots(figsize=(VARSAYILAN_GENISLIK, max(4, len(yontemler) * 1.2)))
    # Mavi tonları — rapor geneli ile tutarlı palet
    renkler_yontem = ['#f7931a', '#4d4d4d', '#0d579b', '#329239', '#FFC000']

    tum_degerler = dusuk + yuksek
    min_val = min(tum_degerler)
    max_val = max(tum_degerler)
    aralik = max_val - min_val

    for i, (yontem, d, y) in enumerate(zip(yontemler, dusuk, yuksek)):
        ax.barh(i, y - d, left=d, height=0.5,
                color=renkler_yontem[i % len(renkler_yontem)], alpha=0.8, edgecolor='white')
        orta = (d + y) / 2
        ax.plot(orta, i, 'D', color='white', markersize=8, zorder=5, label='Orta Nokta' if i == 0 else '')

        # Etiketler — çakışma önleme için yeterli offset
        ax.text(d - aralik * 0.06, i, f'{d:.0f}', va='center', ha='right', fontsize=10, fontweight='bold')
        ax.text(y + aralik * 0.02, i, f'{y:.0f}', va='center', ha='left', fontsize=10, fontweight='bold')

    ax.axvline(x=mevcut_fiyat, color=BBB_RENKLER['negatif'], linestyle='--', linewidth=2,
               label=f'Mevcut: {mevcut_fiyat:.0f} {para_birimi}')
    ax.axvline(x=hedef_fiyat, color=BBB_RENKLER['birincil'], linestyle='-', linewidth=2,
               label=f'Hedef: {hedef_fiyat:.0f} {para_birimi}')

    # X ekseni aralığını genişlet (etiket çakışmasını önle)
    ax.set_xlim(min_val - aralik * 0.15, max_val + aralik * 0.12)

    ax.set_yticks(range(len(yontemler)))
    ax.set_yticklabels(yontemler, fontsize=EKSEN_BOYUT)
    ax.set_xlabel(f'Hisse Fiyatı ({para_birimi})', fontsize=EKSEN_BOYUT)
    ax.set_title('Değerleme Aralığı Analizi', fontsize=BASLIK_BOYUT,
                 fontweight='bold', color=BBB_RENKLER['birincil'])
    ax.legend(loc='upper right', frameon=False)
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    _kaynak_notu(fig, kaynak)
    plt.tight_layout()
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G28: DCF SENSITIVITY HEATMAP ⭐
# ═══════════════════════════════════════════════════════════

def dcf_sensitivity_grafigi(
    wacc_degerleri: List[float],
    buyume_degerleri: List[float],
    fiyat_matrisi: List[List[float]],
    kayit_yolu: str,
    para_birimi: str = 'TL',
    kaynak: str = 'Kaynak: BBB DCF modeli',
    dpi: int = VARSAYILAN_DPI,
):
    """G28 — WACC vs Terminal Büyüme sensitivity heatmap."""
    if not HAS_SEABORN or not HAS_PANDAS:
        print("seaborn ve pandas gerekli. Kur: pip install seaborn pandas", file=sys.stderr)
        return

    matris = np.array(fiyat_matrisi)
    df = pd.DataFrame(
        matris,
        index=[f'%{w:.1f}' for w in wacc_degerleri],
        columns=[f'%{g:.1f}' for g in buyume_degerleri]
    )

    fig, ax = plt.subplots(figsize=(9, 7))
    # annot_kws ile font boyutu, hücre rengine göre otomatik metin rengi seaborn'dan gelir
    sns.heatmap(df, annot=True, fmt='.0f', cmap='RdYlGn',
                cbar_kws={'label': f'Adil Değer Tahmini ({para_birimi})'}, linewidths=0.5,
                linecolor='white', ax=ax,
                annot_kws={'fontweight': 'bold', 'fontsize': 11},
                vmin=np.min(matris) * 0.8, vmax=np.max(matris) * 1.1)

    ax.set_xlabel('Terminal Büyüme Oranı', fontsize=EKSEN_BOYUT, fontweight='bold')
    ax.set_ylabel('WACC', fontsize=EKSEN_BOYUT, fontweight='bold')
    ax.set_title(f'DCF Hassasiyet Analizi — Adil Değer Tahmini ({para_birimi}/hisse)', fontsize=BASLIK_BOYUT,
                 fontweight='bold', color=BBB_RENKLER['birincil'], pad=15)
    plt.yticks(rotation=0)
    _kaynak_notu(fig, kaynak)
    plt.tight_layout()
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G17: PAZAR PAYI (Donut Chart)
# ═══════════════════════════════════════════════════════════

def pazar_payi_grafigi(
    sirketler: List[str],
    paylar: List[float],
    hedef_ticker: str,
    kayit_yolu: str,
    baslik: str = 'Pazar Payı Dağılımı',
    kaynak: str = 'Kaynak: Sektör verileri',
    dpi: int = VARSAYILAN_DPI,
):
    """G17 — Pazar payı donut chart, target şirket vurgulu."""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Hedef dışı dilimler için turuncusuz palet (hedef zaten turuncu olacak)
    _palet_diger = [c for c in BBB_PALET if c != BBB_RENKLER['birincil']]
    diger_idx = 0
    renkler = []
    for s in sirketler:
        if s == hedef_ticker:
            renkler.append(BBB_RENKLER['birincil'])
        else:
            renkler.append(_palet_diger[diger_idx % len(_palet_diger)])
            diger_idx += 1
    patlama = [0.05 if s == hedef_ticker else 0 for s in sirketler]

    wedges, texts, autotexts = ax.pie(
        paylar, labels=sirketler, colors=renkler, explode=patlama,
        autopct='%1.1f%%', startangle=90, pctdistance=0.85
    )

    # Donut deliği — sayfa arka planıyla uyumlu (beyaz değil bej)
    merkez = plt.Circle((0, 0), 0.60, fc=SAYFA_BG)
    ax.add_artist(merkez)

    ax.set_title(baslik, fontsize=BASLIK_BOYUT, fontweight='bold',
                 color=BBB_RENKLER['birincil'], pad=15)
    fig.text(0.5, -0.02, kaynak, fontsize=KAYNAK_BOYUT,
             style='italic', color='gray', ha='center')
    plt.tight_layout()
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G30: COMPS SCATTER (Büyüme vs Çarpan)
# ═══════════════════════════════════════════════════════════

def comps_scatter_grafigi(
    sirketler: List[str],
    buyume_oranlari: List[float],
    carpanlar: List[float],
    hedef_ticker: str,
    carpan_adi: str,
    kayit_yolu: str,
    kaynak: str = 'Kaynak: BBB Finans, Yahoo Finance',
    dpi: int = VARSAYILAN_DPI,
):
    """G30 — Peer scatter: büyüme vs değerleme çarpanı."""
    fig, ax = plt.subplots(figsize=(VARSAYILAN_GENISLIK, VARSAYILAN_YUKSEKLIK))

    for s, b, c in zip(sirketler, buyume_oranlari, carpanlar):
        renk = BBB_RENKLER['birincil'] if s == hedef_ticker else BBB_RENKLER['acik']
        boyut = 200 if s == hedef_ticker else 120
        ax.scatter(b, c, s=boyut, c=renk, edgecolors='white', linewidth=1.5, zorder=5)
        ax.annotate(s, (b, c), textcoords="offset points", xytext=(8, 5), fontsize=9)

    # Trend çizgisi
    z = np.polyfit(buyume_oranlari, carpanlar, 1)
    p = np.poly1d(z)
    x_cizgi = np.linspace(min(buyume_oranlari) * 0.9, max(buyume_oranlari) * 1.1, 100)
    ax.plot(x_cizgi, p(x_cizgi), '--', color='gray', alpha=0.5, label='Trend')

    ax.set_xlabel('Gelir Büyümesi (%)', fontsize=EKSEN_BOYUT)
    ax.set_ylabel(carpan_adi, fontsize=EKSEN_BOYUT)
    ax.set_title(f'Büyüme vs {carpan_adi} — Peer Karşılaştırma', fontsize=BASLIK_BOYUT,
                 fontweight='bold', color=BBB_RENKLER['birincil'])
    _temiz_eksen(ax)
    ax.legend(frameon=False)
    _kaynak_notu(fig, kaynak)
    plt.tight_layout()
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════

def demo_uret(ticker: str = 'DEMO', cikti_klasor: str = '/tmp/demo_charts'):
    """Tüm grafik türlerinden demo örnekler üret."""
    os.makedirs(cikti_klasor, exist_ok=True)
    print(f"Demo grafikler üretiliyor → {cikti_klasor}/")

    yillar = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027]
    gelir = [1200, 1450, 1800, 2300, 2800, 3200, 3700, 4200]
    marj = [0.18, 0.19, 0.21, 0.22, 0.24, 0.25, 0.26, 0.27]

    gelir_marj_grafigi(yillar, gelir, marj, ticker,
                       f'{cikti_klasor}/{ticker}_G02_gelir_marj.png',
                       tahmin_baslangic=2026)
    print("  ✓ G02 — Gelir & Marj")

    segmentler = {
        'Yurtiçi': [800, 900, 1000, 1200, 1400, 1500, 1600, 1700],
        'Avrupa': [300, 400, 550, 750, 900, 1100, 1300, 1500],
        'Diğer': [100, 150, 250, 350, 500, 600, 800, 1000],
    }
    gelir_segment_grafigi(yillar, segmentler, ticker,
                          f'{cikti_klasor}/{ticker}_G03_segment.png',
                          tahmin_baslangic=2026)
    print("  ✓ G03 — Segment Kırılımı")

    sirketler = ['THYAO', 'PGSUS', 'IAG', 'LHA', 'AF-KLM', 'TKC']
    ev_ebitda = [5.2, 4.8, 6.1, 5.5, 4.9, 7.2]
    peer_karsilastirma_grafigi(sirketler, ev_ebitda, 'EV/FAVÖK', 'THYAO',
                               f'{cikti_klasor}/{ticker}_G31_peer.png')
    print("  ✓ G31 — Peer Karşılaştırma")

    yontemler = ['DCF (FCFF)', 'Peer Comps (EV/FAVÖK)', 'Peer Comps (F/K)']
    dusuk = [180, 150, 160]
    yuksek = [280, 230, 250]
    football_field_grafigi(yontemler, dusuk, yuksek, 155, 220,
                           f'{cikti_klasor}/{ticker}_G32_football.png')
    print("  ✓ G32 — Football Field")

    wacc_vals = [12, 14, 16, 18, 20]
    growth_vals = [3, 4, 5, 6, 7]
    matris = [
        [320, 350, 390, 440, 510],
        [260, 280, 310, 340, 390],
        [220, 235, 255, 280, 310],
        [190, 200, 215, 235, 260],
        [165, 175, 185, 200, 220],
    ]
    dcf_sensitivity_grafigi(wacc_vals, growth_vals, matris,
                            f'{cikti_klasor}/{ticker}_G28_sensitivity.png')
    print("  ✓ G28 — DCF Sensitivity")

    paylar_sirketler = ['TBORG', 'AEFES', 'Diğer']
    paylar = [49.7, 50.0, 0.3]
    pazar_payi_grafigi(paylar_sirketler, paylar, 'TBORG',
                       f'{cikti_klasor}/{ticker}_G17_pazar_payi.png')
    print("  ✓ G17 — Pazar Payı")

    comp_sirketler = ['TBORG', 'AEFES', 'Heineken', 'Carlsberg', 'AB InBev']
    buyumeler = [8, 3, 5, 6, 2]
    carpanlar_vals = [12, 14, 18, 16, 15]
    comps_scatter_grafigi(comp_sirketler, buyumeler, carpanlar_vals, 'TBORG', 'EV/FAVÖK',
                          f'{cikti_klasor}/{ticker}_G30_comps.png')
    print("  ✓ G30 — Comps Scatter")

    # G29 — Waterfall
    kalemler = ['PV(FCFF)', 'PV(TV)', '- Borç', '- Azınlık', '+ Nakit', '= Özkaynak']
    degerler = [1200, 3500, -800, -150, 600, 4350]
    dcf_waterfall_grafigi(kalemler, degerler,
                          f'{cikti_klasor}/{ticker}_G29_waterfall.png')
    print("  ✓ G29 — DCF Waterfall")

    # G12 — FCF Bar
    fcf_yillar = [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027]
    fcf_degerler = [120, -50, 200, 350, 280, 400, 500, 600]
    fcf_bar_grafigi(fcf_yillar, fcf_degerler, ticker,
                    f'{cikti_klasor}/{ticker}_G12_fcf.png',
                    tahmin_baslangic=2025)
    print("  ✓ G12 — Serbest Nakit Akışı")

    # G34 — Tarihsel Çarpan Bandı
    band_yillar = [2020, 2021, 2022, 2023, 2024, 2025]
    band_dusuk = [6.5, 7.0, 5.5, 6.0, 7.5, 8.0]
    band_yuksek = [10.5, 12.0, 9.5, 11.0, 12.5, 13.0]
    band_medyan = [8.5, 9.5, 7.5, 8.5, 10.0, 10.5]
    tarihsel_carpan_bandi(band_yillar, band_dusuk, band_yuksek, band_medyan,
                          'EV/FAVÖK', mevcut_deger=9.2,
                          kayit_yolu=f'{cikti_klasor}/{ticker}_G34_carpan_bandi.png')
    print("  ✓ G34 — Tarihsel Çarpan Bandı")

    # G14 — Senaryo Karşılaştırma
    senaryo_metrikleri = ['Gelir (mn TL)', 'FAVÖK (mn TL)', 'Net Kâr (mn TL)', 'Adil Değer Tahmini (TL)']
    bear_vals = [8500, 1400, 600, 150]
    base_vals = [10000, 1800, 900, 220]
    bull_vals = [12000, 2400, 1300, 310]
    senaryo_karsilastirma_grafigi(senaryo_metrikleri, bear_vals, base_vals, bull_vals,
                                  ticker, f'{cikti_klasor}/{ticker}_G14_senaryo.png')
    print("  ✓ G14 — Senaryo Karşılaştırma")

    # E06 — Beat/Miss Waterfall
    bm_kalemler = ['Beklenti', 'Gelir\nSürprizi', 'Marj\nEtkisi', 'Vergi\nEtkisi', 'Diğer', 'Gerçekleşme']
    bm_degerler = [850, 120, -40, 15, -25, 920]
    beat_miss_waterfall_grafigi(bm_kalemler, bm_degerler, 'FAVÖK',
                                f'{cikti_klasor}/{ticker}_E06_beat_miss.png')
    print("  ✓ E06 — Beat/Miss Waterfall")

    # G03-ALT — Stacked Area
    sa_yillar = [2020, 2021, 2022, 2023, 2024, 2025]
    seg_a = [5000, 5500, 6200, 7000, 7800, 8500]
    seg_b = [3000, 3400, 3800, 4200, 4800, 5500]
    seg_c = [2000, 2200, 2500, 2900, 3400, 4000]
    gelir_stacked_area(sa_yillar, [seg_a, seg_b, seg_c], ['Bira', 'Malt', 'Diğer'],
                       ticker, f'{cikti_klasor}/{ticker}_G03alt_stacked_area.png', tahmin_baslangic=2025)
    print("  ✓ G03-ALT — Stacked Area")

    # G04 — Stacked Bar (Coğrafi)
    bolge_a = [8000, 8800, 9500, 10500, 12000, 14000]
    bolge_b = [1500, 1800, 2200, 2800, 3500, 4200]
    gelir_stacked_bar(sa_yillar, [bolge_a, bolge_b], ['Türkiye', 'İhracat'],
                      ticker, f'{cikti_klasor}/{ticker}_G04_stacked_bar.png')
    print("  ✓ G04 — Stacked Bar")

    # G01 — Hisse Fiyat
    tarihler_str = list(range(1, 25))
    fiyatlar_demo = [100 + i * 2 + np.random.randn() * 5 for i in range(24)]
    bench_demo = [100 + i * 1.5 + np.random.randn() * 3 for i in range(24)]
    hisse_fiyat_grafigi(tarihler_str, fiyatlar_demo, bench_demo, ticker, 'BIST-100',
                        f'{cikti_klasor}/{ticker}_G01_hisse_fiyat.png')
    print("  ✓ G01 — Hisse Fiyat")

    # G10/G11 — Marj Evrimi
    marjlar = {'Brüt Marj': [52, 53, 54, 55.3, 56], 'FAVÖK Marjı': [16, 17, 18, 19.1, 20],
               'Net Marj': [12, 14, 15, 11, 13]}
    marj_evrimi_grafigi([2021, 2022, 2023, 2024, 2025], marjlar, ticker,
                        f'{cikti_klasor}/{ticker}_G10_marj_evrimi.png')
    print("  ✓ G10/G11 — Marj Evrimi")

    # G15 — TAM/SAM
    tam_y = [2022, 2023, 2024, 2025, 2026, 2027, 2028]
    pazar_buyuklugu_grafigi(tam_y, [50, 55, 60, 66, 73, 80, 88],
                             sam=[30, 33, 36, 40, 44, 48, 53],
                             som=[5, 5.5, 6, 7, 8, 9, 10],
                             birim='milyar TL',
                             kayit_yolu=f'{cikti_klasor}/{ticker}_G15_tam.png')
    print("  ✓ G15 — TAM/SAM/SOM")

    # G16 — Rekabet Pozisyonlama
    rekabet_pozisyonlama_grafigi(
        [ticker, 'AEFES', 'AB InBev', 'Heineken', 'Carlsberg'],
        [50, 50, 28, 22, 18],  # Pazar payı
        [55.3, 35, 60, 58, 52],  # Brüt marj
        'Pazar Payı (%)', 'Brüt Marj (%)', hedef_idx=0,
        kayit_yolu=f'{cikti_klasor}/{ticker}_G16_rekabet.png')
    print("  ✓ G16 — Rekabet Pozisyonlama")

    # G13 — Dashboard
    operasyonel_dashboard([2021, 2022, 2023, 2024, 2025],
                          {'Gelir Büyümesi (%)': [15, 22, 18, 27, 4],
                           'FAVÖK Marjı (%)': [16, 17, 18, 19, 19],
                           'ROIC (%)': [20, 22, 24, 26, 25],
                           'Net Borç/FAVÖK (x)': [0.5, 0.3, -0.1, -0.3, 0.2]},
                          ticker, f'{cikti_klasor}/{ticker}_G13_dashboard.png')
    print("  ✓ G13 — Dashboard")

    # G33 — Adil Değer Tahmini Senaryoları
    hedef_fiyat_senaryolari(
        [{'isim': 'Kötümser', 'fiyat': 150, 'olasilik': 25},
         {'isim': 'Baz', 'fiyat': 221, 'olasilik': 50},
         {'isim': 'İyimser', 'fiyat': 310, 'olasilik': 25}],
        155, ticker, f'{cikti_klasor}/{ticker}_G33_hedef_fiyat.png')
    print("  ✓ G33 — Adil Değer Tahmini Senaryoları")

    # Chart index
    chart_index_olustur(cikti_klasor, ticker)

    print(f"\n✅ 20 demo grafik üretildi → {cikti_klasor}/")


# ═══════════════════════════════════════════════════════════
# G29: DCF WATERFALL (EV → Equity Bridge)
# ═══════════════════════════════════════════════════════════

def dcf_waterfall_grafigi(kalemler, degerler, kayit_yolu, dpi=DPI):
    """DCF waterfall: PV(FCFF) + PV(TV) - Borç - Azınlık + Nakit = Özsermaye Değeri

    kalemler: ['PV(FCFF)', 'PV(TV)', '- Borç', '- Azınlık', '+ Nakit', '= Özsermaye']
    degerler: [1200, 3500, -800, -150, 600, 4350]  (son eleman = toplam)
    """
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    
    n = len(kalemler)
    kumulatif = 0
    bottoms = []
    heights = []
    renkler = []
    
    for i, val in enumerate(degerler):
        if i == n - 1:
            # Son bar = toplam (sıfırdan başlar)
            bottoms.append(0)
            heights.append(val)
            renkler.append(RENKLER['birincil'])
        else:
            if val >= 0:
                bottoms.append(kumulatif)
                heights.append(val)
                renkler.append(RENKLER['olumlu'] if i < 2 else RENKLER['ikincil'])
            else:
                bottoms.append(kumulatif + val)
                heights.append(abs(val))
                renkler.append(RENKLER['olumsuz'])
            kumulatif += val
    
    bars = ax.bar(range(n), heights, bottom=bottoms, color=renkler,
                  edgecolor=SAYFA_BG, width=0.6, alpha=0.85)
    
    # Değer etiketleri
    for i, (bar, val) in enumerate(zip(bars, degerler)):
        y_pos = bottoms[i] + heights[i] / 2
        isaret = '+' if val > 0 and i > 0 and i < n - 1 else ''
        if i == n - 1:
            isaret = ''
        ax.text(i, y_pos, f'{isaret}{val:,.0f}', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white' if abs(val) > 200 else RENKLER_TEXT)
    
    # Bağlantı çizgileri
    for i in range(n - 2):
        ust = bottoms[i] + heights[i]
        ax.plot([i + 0.3, i + 0.7], [ust, ust], color='gray', linewidth=0.8, linestyle='--')
    
    ax.set_xticks(range(n))
    ax.set_xticklabels(kalemler, fontsize=AXIS_SIZE)
    ax.set_ylabel('Değer (mn TL)', fontsize=AXIS_SIZE)
    ax.set_title('DCF Equity Bridge — EV\'den Özsermaye Değerine', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    _kaynak_notu(fig, 'Kaynak: BBB DCF modeli')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G12: SERBEST NAKİT AKIŞI (FCF) BAR
# ═══════════════════════════════════════════════════════════

def fcf_bar_grafigi(yillar, fcf_degerleri, ticker, kayit_yolu, dpi=DPI, tahmin_baslangic=None):
    """FCF bar chart — pozitif yeşil, negatif kırmızı."""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    
    renkler_bar = []
    for i, (yil, val) in enumerate(zip(yillar, fcf_degerleri)):
        if val >= 0:
            if tahmin_baslangic and yil >= tahmin_baslangic:
                renkler_bar.append(RENKLER['ikincil'])
            else:
                renkler_bar.append(RENKLER['olumlu'])
        else:
            renkler_bar.append(RENKLER['olumsuz'])
    
    bars = ax.bar(yillar, fcf_degerleri, color=renkler_bar, edgecolor='white', alpha=0.85)
    _tamsayi_eksen(ax)

    # Değer etiketleri
    for bar, val in zip(bars, fcf_degerleri):
        yoff = 5 if val >= 0 else -15
        ax.text(bar.get_x() + bar.get_width()/2, val + yoff,
                f'{val:,.0f}', ha='center', va='bottom' if val >= 0 else 'top',
                fontsize=LABEL_SIZE, fontweight='bold', color=RENKLER_TEXT)
    
    # Tahmin ayırıcı
    if tahmin_baslangic:
        ax.axvline(x=tahmin_baslangic - 0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax.text(tahmin_baslangic - 0.3, max(fcf_degerleri) * 0.95, 'Tahmin →',
                fontsize=9, color='gray')
    
    ax.axhline(y=0, color='gray', linewidth=0.8)
    ax.set_ylabel('Serbest Nakit Akışı (mn TL)', fontsize=AXIS_SIZE)
    ax.set_title(f'{ticker} — Serbest Nakit Akışı (FCF)', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    _kaynak_notu(fig, 'Kaynak: KAP, BBB tahminleri')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G34: TARİHSEL ÇARPAN BANDI (Area/Band)
# ═══════════════════════════════════════════════════════════

def tarihsel_carpan_bandi(yillar, dusuk, yuksek, medyan, carpan_adi,
                          mevcut_deger=None, kayit_yolu=None, dpi=DPI):
    """Tarihsel çarpan bandı — min/max alan, medyan çizgisi, mevcut nokta."""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    
    ax.fill_between(yillar, dusuk, yuksek, alpha=0.2, color=RENKLER['birincil'], label='Min-Max Aralığı')
    ax.plot(yillar, medyan, color=RENKLER['birincil'], linewidth=2.5, marker='o',
            markersize=6, label='Medyan', zorder=4)
    ax.plot(yillar, dusuk, color=RENKLER['acik_mavi'], linewidth=1, linestyle='--', alpha=0.7)
    ax.plot(yillar, yuksek, color=RENKLER['acik_mavi'], linewidth=1, linestyle='--', alpha=0.7)
    _tamsayi_eksen(ax)
    
    if mevcut_deger is not None:
        ax.axhline(y=mevcut_deger, color=RENKLER['olumsuz'], linestyle='--', linewidth=1.5,
                   label=f'Mevcut: {mevcut_deger:.1f}x', zorder=5)
    
    ax.set_ylabel(f'{carpan_adi}', fontsize=AXIS_SIZE)
    ax.set_title(f'Tarihsel {carpan_adi} Bandı', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.legend(loc='upper left', frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    _kaynak_notu(fig, 'Kaynak: BBB Finans, Bloomberg')
    if kayit_yolu:
        _kaydet(fig, kayit_yolu, dpi)
    else:
        plt.close()


# ═══════════════════════════════════════════════════════════
# G14: SENARYO KARŞILAŞTIRMA (Grouped Bar)
# ═══════════════════════════════════════════════════════════

def senaryo_karsilastirma_grafigi(metrikler, bear, base, bull, ticker, kayit_yolu, dpi=DPI):
    """Bear/Base/Bull senaryo karşılaştırma — grouped horizontal bar."""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, max(4, len(metrikler) * 1.4)))
    
    y_pos = np.arange(len(metrikler))
    bar_height = 0.25
    
    ax.barh(y_pos - bar_height, bear, bar_height, label='Kötümser', color=RENKLER['olumsuz'], alpha=0.75)
    ax.barh(y_pos, base, bar_height, label='Baz', color=RENKLER['birincil'], alpha=0.85)
    ax.barh(y_pos + bar_height, bull, bar_height, label='İyimser', color=RENKLER['olumlu'], alpha=0.75)
    
    # Değer etiketleri
    for i, (b, ba, bu) in enumerate(zip(bear, base, bull)):
        for val, yoff in [(b, -bar_height), (ba, 0), (bu, bar_height)]:
            ax.text(val + max(bull) * 0.01, i + yoff, f'{val:,.0f}',
                    va='center', fontsize=9, color=RENKLER_TEXT)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(metrikler, fontsize=AXIS_SIZE)
    ax.set_title(f'{ticker} — Senaryo Karşılaştırma (Kötümser / Baz / İyimser)', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.legend(loc='lower right', frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    _kaynak_notu(fig, 'Kaynak: BBB tahminleri')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# E06: BEAT/MISS WATERFALL (Earnings Update)
# ═══════════════════════════════════════════════════════════

def beat_miss_waterfall_grafigi(kalemler, degerler, metrik_adi, kayit_yolu, dpi=DPI):
    """Earnings beat/miss waterfall: Beklenti + bileşenler = Gerçekleşme.
    
    kalemler: ['Beklenti', 'Gelir Sürprizi', 'Marj Etkisi', 'Vergi', 'Diğer', 'Gerçekleşme']
    degerler: [850, 120, -40, 15, -25, 920]
    İlk ve son elemanlar total bar (sıfırdan başlar).
    """
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    
    n = len(kalemler)
    kumulatif = degerler[0]  # Beklenti
    bottoms = [0]  # İlk bar sıfırdan
    heights = [degerler[0]]
    renkler = [RENKLER['ikincil']]  # Beklenti nötr mavi
    
    for i in range(1, n - 1):
        val = degerler[i]
        if val >= 0:
            bottoms.append(kumulatif)
            heights.append(val)
            renkler.append(RENKLER['olumlu'])
        else:
            bottoms.append(kumulatif + val)
            heights.append(abs(val))
            renkler.append(RENKLER['olumsuz'])
        kumulatif += val
    
    # Son bar = gerçekleşme (sıfırdan)
    bottoms.append(0)
    heights.append(degerler[-1])
    renkler.append(RENKLER['birincil'])
    
    bars = ax.bar(range(n), heights, bottom=bottoms, color=renkler,
                  edgecolor='white', width=0.6, alpha=0.85)
    
    # Etiketler
    for i, (bar, val) in enumerate(zip(bars, degerler)):
        y_pos = bottoms[i] + heights[i] / 2
        if i == 0 or i == n - 1:
            label = f'{val:,.0f}'
        else:
            label = f'{"+"+str(val) if val > 0 else str(val)}'
        ax.text(i, y_pos, label, ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
    
    # Bağlantı çizgileri
    for i in range(n - 2):
        ust = bottoms[i] + heights[i] if degerler[i] >= 0 or i == 0 else bottoms[i]
        ax.plot([i + 0.3, i + 0.7], [bottoms[i] + heights[i], bottoms[i] + heights[i]],
                color='gray', linewidth=0.8, linestyle='--')
    
    ax.set_xticks(range(n))
    ax.set_xticklabels(kalemler, fontsize=AXIS_SIZE)
    ax.set_ylabel(f'{metrik_adi} (mn TL)', fontsize=AXIS_SIZE)
    ax.set_title(f'{metrik_adi} — Beklenti vs Gerçekleşme Köprüsü', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    _kaynak_notu(fig, 'Kaynak: KAP, BBB tahminleri')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G03-ALT: GELİR STACKED AREA (Ürün Segmentasyonu)
# ═══════════════════════════════════════════════════════════

def gelir_stacked_area(yillar, segmentler, segment_isimleri, ticker, kayit_yolu,
                       dpi=DPI, tahmin_baslangic=None):
    """Stacked area — gelir segmentasyonu. segmentler: listelerden oluşan liste."""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    ax.stackplot(yillar, *segmentler, labels=segment_isimleri,
                 colors=BBB_PALET[:len(segmentler)], alpha=0.8)
    _tamsayi_eksen(ax)
    if tahmin_baslangic:
        ax.axvline(x=tahmin_baslangic - 0.5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
        ax.text(tahmin_baslangic, ax.get_ylim()[1] * 0.95, 'Tahmin →', fontsize=9, color='gray')
    ax.set_ylabel('Gelir (mn TL)', fontsize=AXIS_SIZE)
    ax.set_title(f'{ticker} — Gelir Segmentasyonu', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.legend(loc='upper left', frameon=False, fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    _kaynak_notu(fig, 'Kaynak: KAP, BBB tahminleri')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G04: COĞRAFİ GELİR STACKED BAR
# ═══════════════════════════════════════════════════════════

def gelir_stacked_bar(yillar, bolge_verileri, bolge_isimleri, ticker, kayit_yolu, dpi=DPI):
    """Stacked bar — coğrafi gelir kırılımı."""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    x = np.arange(len(yillar))
    bottoms = np.zeros(len(yillar))
    for i, (veriler, isim) in enumerate(zip(bolge_verileri, bolge_isimleri)):
        ax.bar(x, veriler, bottom=bottoms, label=isim,
               color=BBB_PALET[i % len(BBB_PALET)], alpha=0.85, edgecolor='white')
        bottoms += np.array(veriler)
    # Toplam ve ikinci bölge payı etiketleri
    if len(bolge_verileri) >= 2:
        for j in range(len(yillar)):
            toplam = sum(b[j] for b in bolge_verileri)
            if toplam == 0:
                continue
            ikinci_pay = bolge_verileri[1][j] / toplam * 100
            if ikinci_pay >= 0.1:  # Sadece anlamlı payları göster
                ax.text(j, toplam + toplam * 0.01,
                        f'{bolge_isimleri[1].split("(")[0].strip()}: %{ikinci_pay:.1f}',
                        ha='center', fontsize=8, color='gray', style='italic')
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in yillar], fontsize=AXIS_SIZE)
    ax.set_ylabel('Gelir (mn TL)', fontsize=AXIS_SIZE)
    ax.set_title(f'{ticker} — Coğrafi Gelir Kırılımı', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.legend(loc='upper left', frameon=False, fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    _kaynak_notu(fig, 'Kaynak: KAP, BBB tahminleri')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G01: HİSSE FİYAT PERFORMANSI
# ═══════════════════════════════════════════════════════════

def hisse_fiyat_grafigi(tarihler, fiyatlar, benchmark_fiyatlar=None, ticker='',
                        benchmark_adi='BIST-100', kayit_yolu=None, dpi=DPI):
    """Hisse fiyat performansı vs benchmark (100 bazlı normalize)."""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    baz = fiyatlar[0]
    norm = [f / baz * 100 for f in fiyatlar]
    ax.plot(tarihler, norm, color=RENKLER['birincil'], linewidth=2.5, label=ticker, zorder=4)
    if benchmark_fiyatlar:
        baz_b = benchmark_fiyatlar[0]
        norm_b = [f / baz_b * 100 for f in benchmark_fiyatlar]
        ax.plot(tarihler, norm_b, color=RENKLER['olumsuz'], linewidth=1.5,
                linestyle='--', label=benchmark_adi, alpha=0.7)
    _tamsayi_eksen(ax)
    ax.set_ylabel('Endekslenmiş (100 bazlı)', fontsize=AXIS_SIZE)
    ax.set_title(f'{ticker} vs {benchmark_adi} — Fiyat Performansı', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.legend(loc='upper left', frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.3, linestyle='--')
    _kaynak_notu(fig, 'Kaynak: BBB Finans')
    if kayit_yolu:
        _kaydet(fig, kayit_yolu, dpi)
    else:
        plt.close()


# ═══════════════════════════════════════════════════════════
# G10/G11: MARJ EVRİMİ (Çoklu Çizgi)
# ═══════════════════════════════════════════════════════════

def marj_evrimi_grafigi(yillar, marjlar_dict, ticker, kayit_yolu, dpi=DPI):
    """Çoklu marj çizgi grafiği. marjlar_dict: {'Brüt Marj': [55,56,...], 'FAVÖK Marjı': [17,18,...]}"""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    renk_listesi = [RENKLER['birincil'], RENKLER['olumlu'], RENKLER['olumsuz'],
                    BBB_RENKLER['uyari'], '#7030A0']
    for i, (isim, degerler) in enumerate(marjlar_dict.items()):
        r = renk_listesi[i % len(renk_listesi)]
        ax.plot(yillar, degerler, marker='o', markersize=6, linewidth=2.5, label=isim, color=r, zorder=4)
        ax.text(yillar[-1] + 0.15, degerler[-1], f'%{degerler[-1]:.1f}',
                fontsize=LABEL_SIZE, color=r, fontweight='bold', va='center')
    _tamsayi_eksen(ax)
    ax.set_ylabel('Marj (%)', fontsize=AXIS_SIZE)
    ax.set_title(f'{ticker} — Kârlılık Evrimi', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.legend(loc='lower right', frameon=False, fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.3, linestyle='--')
    _kaynak_notu(fig, 'Kaynak: KAP, BBB Finans')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G15: TAM/SAM PAZAR BÜYÜKLÜĞÜ
# ═══════════════════════════════════════════════════════════

def pazar_buyuklugu_grafigi(yillar, tam, sam=None, som=None, birim='milyar USD',
                             kayit_yolu=None, dpi=DPI):
    """TAM/SAM/SOM pazar büyüklüğü alansal grafik."""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    datasets = [(tam, 'TAM (Toplam Erişilebilir Pazar)', RENKLER['acik_mavi'])]
    if sam:
        datasets.append((sam, 'SAM (Ulaşılabilir Pazar)', RENKLER['ikincil']))
    if som:
        datasets.append((som, 'SOM (Elde Edilebilir Pazar)', RENKLER['birincil']))
    for veriler, isim, renk in reversed(datasets):
        ax.fill_between(yillar, veriler, alpha=0.3, color=renk)
        ax.plot(yillar, veriler, linewidth=2, label=isim, color=renk)
    _tamsayi_eksen(ax)
    ax.set_ylabel(f'Pazar ({birim})', fontsize=AXIS_SIZE)
    ax.set_title('Pazar Büyüklüğü (TAM / SAM / SOM)', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.legend(loc='upper left', frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.3, linestyle='--')
    _kaynak_notu(fig, 'Kaynak: Sektör raporları, BBB')
    if kayit_yolu:
        _kaydet(fig, kayit_yolu, dpi)
    else:
        plt.close()


# ═══════════════════════════════════════════════════════════
# G16: REKABETÇİ POZİSYONLAMA (2×2 Scatter)
# ═══════════════════════════════════════════════════════════

def rekabet_pozisyonlama_grafigi(sirketler, x_deg, y_deg, x_label, y_label,
                                  hedef_idx=0, kayit_yolu=None, dpi=DPI, ticker=None):
    """2×2 pozisyonlama scatter. hedef_idx: vurgulanacak şirket indeksi."""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
    for i, (s, x, y) in enumerate(zip(sirketler, x_deg, y_deg)):
        if i == hedef_idx:
            ax.scatter(x, y, s=200, color=RENKLER['birincil'], zorder=5, edgecolors='white', linewidth=2)
            ax.annotate(f'{s} ★', (x, y), xytext=(8, 8), textcoords='offset points',
                        fontsize=11, fontweight='bold', color=RENKLER['birincil'])
        else:
            ax.scatter(x, y, s=120, color=RENKLER['ikincil'], alpha=0.7, zorder=4)
            ax.annotate(s, (x, y), xytext=(6, 6), textcoords='offset points', fontsize=9, color=RENKLER_TEXT)
    med_x, med_y = np.median(x_deg), np.median(y_deg)
    ax.axvline(x=med_x, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.axhline(y=med_y, color='gray', linestyle='--', linewidth=0.8, alpha=0.5)
    ax.set_xlabel(x_label, fontsize=AXIS_SIZE)
    ax.set_ylabel(y_label, fontsize=AXIS_SIZE)
    baslik_prefix = f'{ticker} — ' if ticker else ''
    ax.set_title(f'{baslik_prefix}Rekabet Pozisyonlama Matrisi', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(alpha=0.2, linestyle='--')
    _kaynak_notu(fig, 'Kaynak: KAP, Yahoo Finance, BBB')
    if kayit_yolu:
        _kaydet(fig, kayit_yolu, dpi)
    else:
        plt.close()


# ═══════════════════════════════════════════════════════════
# G13: OPERASYONel METRİK DASHBOARD (2×2 Panel)
# ═══════════════════════════════════════════════════════════

def operasyonel_dashboard(yillar, metrikler, ticker, kayit_yolu, dpi=DPI):
    """4-panel dashboard. metrikler: dict, en fazla 4 anahtar."""
    fig, axes = plt.subplots(2, 2, figsize=(FIG_WIDTH, FIG_HEIGHT + 1))
    fig.suptitle(f'{ticker} — Operasyonel Göstergeler', fontsize=TITLE_SIZE,
                 fontweight='bold', color=BBB_RENKLER['birincil'], y=0.98)
    renk_listesi = [RENKLER['birincil'], RENKLER['olumlu'], RENKLER['olumsuz'], BBB_RENKLER['uyari']]
    for idx, (isim, degerler) in enumerate(metrikler.items()):
        if idx >= 4:
            break
        ax = axes[idx // 2][idx % 2]
        r = renk_listesi[idx]
        ax.plot(yillar, degerler, marker='o', markersize=5, linewidth=2, color=r)
        ax.fill_between(yillar, degerler, alpha=0.1, color=r)
        _tamsayi_eksen(ax)
        ax.set_title(isim, fontsize=10, fontweight='bold', color=BBB_RENKLER['metin'])
        ax.grid(alpha=0.3, linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.text(yillar[-1], degerler[-1], f'{degerler[-1]:.1f}', fontsize=9, fontweight='bold', color=r)
    _kaynak_notu(fig, 'Kaynak: KAP, BBB Finans')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# G33: HEDEF FİYAT SENARYOLARI
# ═══════════════════════════════════════════════════════════

def hedef_fiyat_senaryolari(senaryolar, mevcut_fiyat, ticker, kayit_yolu, dpi=DPI):
    """Horizontal bar — Bear/Base/Bull hedef fiyat senaryoları.
    senaryolar: [{'isim': 'Bear', 'fiyat': 150, 'olasilik': 25}, ...]"""
    fig, ax = plt.subplots(figsize=(FIG_WIDTH, 4))
    renkler_s = [RENKLER['olumsuz'], RENKLER['birincil'], RENKLER['olumlu']]
    isimler = [s['isim'] for s in senaryolar]
    fiyatlar = [s['fiyat'] for s in senaryolar]
    olasiliklar = [s.get('olasilik', '') for s in senaryolar]
    y_pos = np.arange(len(senaryolar))
    bars = ax.barh(y_pos, fiyatlar, color=renkler_s[:len(senaryolar)], alpha=0.8, height=0.5)
    for i, (bar, f, o) in enumerate(zip(bars, fiyatlar, olasiliklar)):
        label = f'{f:.0f} TL'
        if o:
            label += f' (%{o})'
        ax.text(f + max(fiyatlar) * 0.02, i, label, va='center', fontsize=11, fontweight='bold', color=RENKLER_TEXT)
    ax.axvline(x=mevcut_fiyat, color='gray', linestyle='--', linewidth=2, label=f'Mevcut: {mevcut_fiyat} TL')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(isimler, fontsize=AXIS_SIZE)
    ax.set_xlabel('Adil Değer Tahmini (TL)', fontsize=AXIS_SIZE)
    ax.set_title(f'{ticker} — Adil Değer Tahmini Senaryoları', fontsize=TITLE_SIZE,
                 fontweight='bold', color=RENKLER['birincil'], pad=15)
    ax.legend(loc='lower right', frameon=False, fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    _kaynak_notu(fig, 'Kaynak: BBB DCF modeli')
    _kaydet(fig, kayit_yolu, dpi)


# ═══════════════════════════════════════════════════════════
# CHART INDEX OLUŞTURUCU
# ═══════════════════════════════════════════════════════════

def chart_dogrula(klasor, ticker=None):
    """T4 chart paketini dogrula. Zorunlu chart'lar, dosya sayisi, boyut kontrolu."""
    import glob
    
    if ticker:
        pngs = sorted(glob.glob(os.path.join(klasor, f'{ticker}_*.png')))
    else:
        pngs = sorted(glob.glob(os.path.join(klasor, '*.png')))
    
    png_isimleri = [os.path.basename(f) for f in pngs]
    
    print("=" * 60)
    print("GRAFIK DOGRULAMA")
    print("=" * 60)
    
    # 1. Zorunlu chart'lar
    zorunlu_kodlar = ['G03', 'G04', 'G28', 'G32']
    zorunlu_aciklamalar = {
        'G03': 'Gelir segmentasyonu (stacked area)',
        'G04': 'Cografi gelir kirilimi (stacked bar)',
        'G28': 'DCF sensitivity (heatmap)',
        'G32': 'Degerleme football field',
    }
    print("\n1. ZORUNLU GRAFIKLER (4):")
    tum_zorunlu = True
    for kod in zorunlu_kodlar:
        found = any(kod in f for f in png_isimleri)
        status = '✓' if found else '✗ EKSIK'
        if not found:
            tum_zorunlu = False
        print(f"   {status}: {kod} — {zorunlu_aciklamalar[kod]}")
    
    # 2. Toplam sayi
    print(f"\n2. TOPLAM GRAFIK: {len(pngs)}")
    print(f"   Hedef: 25-35")
    if len(pngs) >= 25:
        print(f"   Durum: ✓ GECTI ({len(pngs)} >= 25)")
    elif len(pngs) >= 20:
        print(f"   Durum: ⚠ UYARI ({len(pngs)} < 25, {25 - len(pngs)} eksik)")
    else:
        print(f"   Durum: ✗ BASARISIZ ({len(pngs)} < 20)")
    
    # 3. Dosya boyutlari
    print("\n3. DOSYA BOYUT KONTROLU (ilk 5):")
    kucuk = []
    for f in pngs[:5]:
        boyut_kb = os.path.getsize(f) / 1024
        if boyut_kb < 50:
            kucuk.append(os.path.basename(f))
        print(f"   {os.path.basename(f)}: {boyut_kb:.0f} KB {'⚠ KUCUK' if boyut_kb < 50 else ''}")
    
    if kucuk:
        print(f"   ⚠ UYARI: {len(kucuk)} dosya dusuk cozunurluk olabilir (< 50 KB)")
    else:
        print(f"   ✓ Orneklenen dosyalarin hepsi yeterli boyutta")
    
    # 4. chart_index.txt
    index_yolu = os.path.join(klasor, 'chart_index.txt')
    index_var = os.path.exists(index_yolu)
    print(f"\n4. CHART INDEX: {'✓ Mevcut' if index_var else '✗ EKSIK — chart_index_olustur() calistir'}")
    
    # 5. Mevcut chart kodlari
    print(f"\n5. MEVCUT CHART KODLARI:")
    mevcut_kodlar = set()
    for f in png_isimleri:
        for part in f.split('_'):
            if part.startswith('G') and part[1:].isdigit():
                mevcut_kodlar.add(part)
            elif part.startswith('EK') and part[2:].isdigit():
                mevcut_kodlar.add(part)
            elif part.startswith('E') and part[1:].isdigit() and len(part) <= 3:
                mevcut_kodlar.add(part)
    print(f"   {sorted(mevcut_kodlar)}")
    
    # Sonuc
    print("\n" + "=" * 60)
    gecti = tum_zorunlu and len(pngs) >= 25
    if gecti:
        print("✓ DOGRULAMA GECTI — T5 icin hazir")
    else:
        sorunlar = []
        if not tum_zorunlu:
            sorunlar.append("zorunlu chart eksik")
        if len(pngs) < 25:
            sorunlar.append(f"toplam {len(pngs)} < 25")
        print(f"✗ DOGRULAMA BASARISIZ — {', '.join(sorunlar)}")
    print("=" * 60)
    
    return gecti


def chart_index_olustur(klasor, ticker, kayit_yolu=None):
    """Klasördeki tüm chart dosyalarının indeksini oluştur."""
    import glob
    dosyalar = sorted(glob.glob(os.path.join(klasor, f'{ticker}_*.png')))
    if not kayit_yolu:
        kayit_yolu = os.path.join(klasor, 'chart_index.txt')
    with open(kayit_yolu, 'w', encoding='utf-8') as f:
        f.write(f'CHART INDEX — {ticker}\n')
        f.write('=' * 60 + '\n\n')
        f.write(f'Toplam: {len(dosyalar)} chart\n\n')
        for i, d in enumerate(dosyalar, 1):
            isim = os.path.basename(d)
            boyut = os.path.getsize(d) / 1024
            f.write(f'{i:2d}. {isim} ({boyut:.0f} KB)\n')
    print(f'✅ Chart index → {kayit_yolu} ({len(dosyalar)} dosya)')
    return dosyalar


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='BBB Grafik Üretici — Equity analiz grafikleri',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python grafik-uret.py --demo --ticker TBORG --cikti-klasor /tmp/charts
  python grafik-uret.py --tur football-field --veri veri.json --cikti grafik.png

Grafik türleri: gelir-marj, segment, peer, football-field, sensitivity, pazar-payi, comps-scatter,
                waterfall, fcf, carpan-bandi, senaryo, beat-miss
        """
    )
    parser.add_argument('--demo', action='store_true', help='Demo grafikler üret')
    parser.add_argument('--ticker', default='DEMO', help='Hisse kodu (demo için)')
    parser.add_argument('--cikti-klasor', default='/tmp/demo_charts', help='Demo çıktı klasörü')
    parser.add_argument('--tur', help='Tek grafik türü')
    parser.add_argument('--veri', help='JSON veri dosyası')
    parser.add_argument('--index', action='store_true', help='Chart index dosyası oluştur')
    parser.add_argument('--dogrula', action='store_true', help='Chart paketini dogrula (T4 QC)')
    parser.add_argument('--cikti', help='Çıktı dosya yolu')
    parser.add_argument('--dpi', type=int, default=300, help='Çözünürlük (varsayılan: 300)')

    args = parser.parse_args()

    if args.dogrula:
        chart_dogrula(args.cikti_klasor, args.ticker if args.ticker != 'DEMO' else None)
    elif args.demo:
        demo_uret(args.ticker, args.cikti_klasor)
    elif args.tur and args.veri and args.cikti:
        with open(args.veri, 'r', encoding='utf-8') as f:
            veri = json.load(f)
        # Grafik türüne göre yönlendir
        fonksiyonlar = {
            'gelir-marj': gelir_marj_grafigi,
            'segment': gelir_segment_grafigi,
            'peer': peer_karsilastirma_grafigi,
            'football-field': football_field_grafigi,
            'sensitivity': dcf_sensitivity_grafigi,
            'pazar-payi': pazar_payi_grafigi,
            'comps-scatter': comps_scatter_grafigi,
            'waterfall': dcf_waterfall_grafigi,
            'fcf': fcf_bar_grafigi,
            'carpan-bandi': tarihsel_carpan_bandi,
            'senaryo': senaryo_karsilastirma_grafigi,
            'beat-miss': beat_miss_waterfall_grafigi,
            'stacked-area': gelir_stacked_area,
            'stacked-bar': gelir_stacked_bar,
            'hisse-fiyat': hisse_fiyat_grafigi,
            'marj-evrimi': marj_evrimi_grafigi,
            'tam': pazar_buyuklugu_grafigi,
            'rekabet': rekabet_pozisyonlama_grafigi,
            'dashboard': operasyonel_dashboard,
            'hedef-fiyat': hedef_fiyat_senaryolari,
        }
        if args.tur in fonksiyonlar:
            fonksiyonlar[args.tur](**veri, kayit_yolu=args.cikti, dpi=args.dpi)
            print(f"✅ {args.tur} → {args.cikti}")
        else:
            print(f"❌ Bilinmeyen tür: {args.tur}. Desteklenen: {', '.join(fonksiyonlar.keys())}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
