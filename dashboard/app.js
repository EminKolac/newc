// ══════════════════════════════════════════════════════════════════════════════
// Geopolitical Market Dashboard — App Logic
// Tracks: S&P 500, Nasdaq, Dow, Crude Oil (WTI), Gold, US Dollar Index
// Features: Real-time charts, volatility metrics, correlation matrix,
//           2%+ move alerts, geopolitical news feed
// ══════════════════════════════════════════════════════════════════════════════

(function () {
  'use strict';

  // ── Instrument Definitions ──
  const INSTRUMENTS = {
    sp500:  { name: 'S&P 500',   base: 5250,   vol: 0.0008, color: '#3b82f6', decimals: 2 },
    nasdaq: { name: 'Nasdaq',    base: 16400,  vol: 0.0012, color: '#a855f7', decimals: 2 },
    dow:    { name: 'Dow Jones', base: 39200,  vol: 0.0006, color: '#22c55e', decimals: 2 },
    oil:    { name: 'Crude Oil', base: 78.50,  vol: 0.0025, color: '#f97316', decimals: 2 },
    gold:   { name: 'Gold',     base: 2340,    vol: 0.0015, color: '#eab308', decimals: 2 },
    dxy:    { name: 'DXY',      base: 104.20,  vol: 0.0004, color: '#06b6d4', decimals: 3 },
  };

  const KEYS = Object.keys(INSTRUMENTS);
  const MAX_POINTS = 120; // 2 minutes of data at 1s interval
  const UPDATE_INTERVAL = 1000;

  // ── State ──
  const state = {
    prices: {},       // current prices
    opens: {},        // session open prices
    history: {},      // price history arrays
    charts: {},       // Chart.js instances
    alerts: [],       // alert log entries
    alertsEnabled: true,
    alertThreshold: 2.0,
    newsFilter: 'all',
    newsItems: [],
    geopoliticalTension: 0.5, // 0-1 scale
    vix: 18,
  };

  // ── Initialize price data ──
  KEYS.forEach(key => {
    const inst = INSTRUMENTS[key];
    // Add some initial randomization
    const openOffset = (Math.random() - 0.5) * inst.base * 0.01;
    state.opens[key] = inst.base + openOffset;
    state.prices[key] = state.opens[key];
    state.history[key] = [];
    // Pre-fill some history
    let p = state.opens[key];
    for (let i = 0; i < 60; i++) {
      p += p * (Math.random() - 0.5) * inst.vol * 2;
      state.history[key].push(p);
    }
    state.prices[key] = p;
  });

  // ── Chart Setup ──
  function createChart(key) {
    const ctx = document.getElementById(`chart-${key}`).getContext('2d');
    const inst = INSTRUMENTS[key];
    const gradient = ctx.createLinearGradient(0, 0, 0, 160);
    gradient.addColorStop(0, inst.color + '40');
    gradient.addColorStop(1, inst.color + '00');

    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: state.history[key].map((_, i) => i),
        datasets: [{
          data: [...state.history[key]],
          borderColor: inst.color,
          backgroundColor: gradient,
          borderWidth: 1.5,
          fill: true,
          pointRadius: 0,
          tension: 0.3,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 0 },
        interaction: { intersect: false, mode: 'index' },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#1e293b',
            titleColor: '#e2e8f0',
            bodyColor: '#e2e8f0',
            borderColor: inst.color,
            borderWidth: 1,
            displayColors: false,
            callbacks: {
              label: ctx => `${inst.name}: ${ctx.parsed.y.toFixed(inst.decimals)}`,
            },
          },
          annotation: {
            annotations: {
              openLine: {
                type: 'line',
                yMin: state.opens[key],
                yMax: state.opens[key],
                borderColor: '#64748b',
                borderWidth: 1,
                borderDash: [4, 4],
                label: {
                  display: true,
                  content: 'Open',
                  position: 'start',
                  backgroundColor: 'transparent',
                  color: '#64748b',
                  font: { size: 9 },
                },
              },
            },
          },
        },
        scales: {
          x: { display: false },
          y: {
            position: 'right',
            grid: { color: '#1e293b40' },
            ticks: {
              color: '#64748b',
              font: { size: 10, family: 'monospace' },
              callback: v => v.toFixed(inst.decimals > 2 ? 3 : inst.base > 1000 ? 0 : 2),
            },
          },
        },
        layout: { padding: { top: 4, bottom: 4, left: 0, right: 0 } },
      },
    });

    // Resize canvas
    chart.canvas.parentNode.style.height = '140px';
    state.charts[key] = chart;
  }

  // ── Geopolitical News Simulation ──
  const NEWS_TEMPLATES = [
    { tags: ['iran', 'ceasefire'], headline: 'US-Iran ceasefire talks enter {adj} phase as diplomats {verb} in {location}', impact: 'oil', direction: -1 },
    { tags: ['iran', 'ceasefire'], headline: 'Iran {verb} ceasefire conditions amid {adj} international pressure', impact: 'oil', direction: 1 },
    { tags: ['hormuz'], headline: 'Naval activity {verb} near Strait of Hormuz; {pct}% of global oil transit at risk', impact: 'oil', direction: 1 },
    { tags: ['hormuz'], headline: 'Strait of Hormuz shipping lanes {verb} following {adj} security assessment', impact: 'oil', direction: -1 },
    { tags: ['oil'], headline: 'Crude oil {verb} ${amt}/barrel on {adj} Middle East supply concerns', impact: 'oil', direction: 1 },
    { tags: ['oil', 'hormuz'], headline: 'OPEC+ emergency meeting called as Hormuz tensions {verb} supply outlook', impact: 'oil', direction: 1 },
    { tags: ['iran'], headline: 'Pentagon {verb} additional carrier group to Persian Gulf region', impact: 'market', direction: -1 },
    { tags: ['iran', 'ceasefire'], headline: 'UN Security Council {verb} resolution on Iran ceasefire framework', impact: 'market', direction: -1 },
    { tags: ['oil', 'hormuz'], headline: 'Insurance premiums for Hormuz transit {verb} to {adj} levels', impact: 'oil', direction: 1 },
    { tags: ['iran'], headline: 'Iran nuclear program {verb}: IAEA report cites {adj} enrichment activity', impact: 'market', direction: -1 },
    { tags: ['ceasefire'], headline: 'Ceasefire monitoring group reports {adj} compliance from both parties', impact: 'market', direction: 1 },
    { tags: ['oil'], headline: 'Strategic Petroleum Reserve release {verb} as oil prices {verb2} geopolitical premium', impact: 'oil', direction: -1 },
    { tags: ['hormuz'], headline: 'Commercial vessel {verb} in Strait of Hormuz; Iran denies involvement', impact: 'oil', direction: 1 },
    { tags: ['iran', 'ceasefire'], headline: 'US envoy: ceasefire agreement "{adj}" — sanctions relief package under review', impact: 'market', direction: 1 },
    { tags: ['market'], headline: 'Defense sector {verb} as geopolitical risk premium {verb2} across indices', impact: 'market', direction: -1 },
    { tags: ['oil', 'iran'], headline: 'Iran oil exports {verb} amid {adj} enforcement of sanctions regime', impact: 'oil', direction: 1 },
  ];

  const FILL_WORDS = {
    adj: ['critical', 'decisive', 'unprecedented', 'heightened', 'significant', 'fragile', 'substantial', 'elevated', 'renewed', 'cautious', 'promising', 'record', 'uncertain'],
    verb: ['escalate', 'stabilize', 'intensify', 'resume', 'expand', 'signal', 'confirm', 'deploy', 'announce', 'surge', 'retreat', 'convene', 'assess', 'reopen', 'seized', 'harassed'],
    verb2: ['reflects', 'absorbs', 'amplifies', 'discounts', 'incorporates', 'signals'],
    location: ['Geneva', 'Vienna', 'Doha', 'Muscat', 'Washington', 'Riyadh'],
    pct: ['20', '25', '30', '35'],
    amt: ['2.40', '3.10', '1.85', '4.20', '2.75'],
  };

  function generateNewsItem() {
    const template = NEWS_TEMPLATES[Math.floor(Math.random() * NEWS_TEMPLATES.length)];
    let headline = template.headline;
    headline = headline.replace(/\{(\w+)\}/g, (_, key) => {
      const options = FILL_WORDS[key];
      return options ? options[Math.floor(Math.random() * options.length)] : '';
    });

    const impactLabels = {
      oil: 'Oil price impact',
      market: 'Broad market impact',
    };

    return {
      tags: template.tags,
      headline: headline.charAt(0).toUpperCase() + headline.slice(1),
      time: new Date(),
      impact: impactLabels[template.impact] || 'Market impact',
      direction: template.direction,
      severity: Math.random() > 0.7 ? 'high' : 'moderate',
    };
  }

  // ── Price Simulation Engine ──
  // Uses geometric Brownian motion with mean-reversion and geopolitical shocks
  function simulatePriceUpdate() {
    // Occasionally shift geopolitical tension
    if (Math.random() < 0.02) {
      state.geopoliticalTension = Math.max(0, Math.min(1,
        state.geopoliticalTension + (Math.random() - 0.45) * 0.3
      ));
    }

    const tension = state.geopoliticalTension;

    KEYS.forEach(key => {
      const inst = INSTRUMENTS[key];
      const price = state.prices[key];

      // Base volatility adjusted by geopolitical tension
      let effectiveVol = inst.vol;
      if (key === 'oil') effectiveVol *= (1 + tension * 2);
      if (key === 'gold') effectiveVol *= (1 + tension * 1.5);
      if (key === 'dxy') effectiveVol *= (1 + tension * 0.5);
      if (['sp500', 'nasdaq', 'dow'].includes(key)) effectiveVol *= (1 + tension * 0.8);

      // Geometric Brownian motion with slight mean reversion
      const meanReversion = (inst.base - price) / inst.base * 0.001;
      const shock = (Math.random() - 0.5) * 2;
      const geoShock = key === 'oil' ? tension * (Math.random() - 0.3) * 0.001 :
                       key === 'gold' ? tension * (Math.random() - 0.3) * 0.0008 :
                       ['sp500', 'nasdaq', 'dow'].includes(key) ? -tension * Math.random() * 0.0003 : 0;

      const change = price * (effectiveVol * shock + meanReversion + geoShock);
      state.prices[key] = Math.max(price * 0.9, Math.min(price * 1.1, price + change));

      // Update history
      state.history[key].push(state.prices[key]);
      if (state.history[key].length > MAX_POINTS) {
        state.history[key].shift();
      }
    });

    // Update simulated VIX
    const avgVol = KEYS.filter(k => ['sp500', 'nasdaq', 'dow'].includes(k))
      .map(k => calcIntradayVol(k))
      .reduce((a, b) => a + b, 0) / 3;
    state.vix = Math.max(10, Math.min(80,
      12 + avgVol * 300 + tension * 25 + (Math.random() - 0.5) * 2
    ));
  }

  // ── Volatility Calculations ──
  function calcReturns(prices) {
    const returns = [];
    for (let i = 1; i < prices.length; i++) {
      returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
    }
    return returns;
  }

  function calcStdDev(arr) {
    if (arr.length < 2) return 0;
    const mean = arr.reduce((a, b) => a + b, 0) / arr.length;
    const variance = arr.reduce((sum, val) => sum + (val - mean) ** 2, 0) / (arr.length - 1);
    return Math.sqrt(variance);
  }

  function calcIntradayVol(key) {
    const returns = calcReturns(state.history[key]);
    return calcStdDev(returns);
  }

  function calc1hVol(key) {
    const recent = state.history[key].slice(-60);
    const returns = calcReturns(recent);
    return calcStdDev(returns);
  }

  function calcPctChange(key) {
    return ((state.prices[key] - state.opens[key]) / state.opens[key]) * 100;
  }

  function calcDayRange(key) {
    const h = state.history[key];
    return { min: Math.min(...h), max: Math.max(...h) };
  }

  // ── Correlation ──
  function calcCorrelation(arr1, arr2) {
    const n = Math.min(arr1.length, arr2.length);
    if (n < 5) return 0;
    const a = arr1.slice(-n), b = arr2.slice(-n);
    const r1 = calcReturns(a), r2 = calcReturns(b);
    const len = Math.min(r1.length, r2.length);
    if (len < 3) return 0;

    const mean1 = r1.reduce((s, v) => s + v, 0) / len;
    const mean2 = r2.reduce((s, v) => s + v, 0) / len;

    let cov = 0, std1 = 0, std2 = 0;
    for (let i = 0; i < len; i++) {
      const d1 = r1[i] - mean1, d2 = r2[i] - mean2;
      cov += d1 * d2;
      std1 += d1 * d1;
      std2 += d2 * d2;
    }

    const denom = Math.sqrt(std1 * std2);
    return denom === 0 ? 0 : cov / denom;
  }

  // ── Alert System ──
  function checkAlerts() {
    const threshold = state.alertThreshold;

    KEYS.forEach(key => {
      const pctChange = Math.abs(calcPctChange(key));
      const inst = INSTRUMENTS[key];

      if (pctChange >= threshold) {
        // Check if we already fired for this level (avoid spam)
        const level = Math.floor(pctChange / threshold);
        const existingAlert = state.alerts.find(a =>
          a.key === key && a.level === level && (Date.now() - a.timestamp < 60000)
        );

        if (!existingAlert) {
          const direction = calcPctChange(key) > 0 ? 'UP' : 'DOWN';
          const alert = {
            key,
            level,
            timestamp: Date.now(),
            time: new Date(),
            message: `${inst.name} ${direction} ${pctChange.toFixed(2)}% from open`,
            severity: pctChange >= threshold * 2 ? 'critical' : 'warning',
            pctChange: pctChange,
          };
          state.alerts.unshift(alert);
          if (state.alerts.length > 50) state.alerts.pop();

          showAlertBanner(alert);
          flashCard(key);
          renderAlerts();
        }
      }
    });
  }

  function showAlertBanner(alert) {
    const banner = document.getElementById('alert-banner');
    const text = document.getElementById('alert-banner-text');
    text.textContent = `⚠ ALERT: ${alert.message}`;
    banner.classList.remove('hidden');

    // Auto-dismiss after 8s
    clearTimeout(state.bannerTimeout);
    state.bannerTimeout = setTimeout(() => banner.classList.add('hidden'), 8000);
  }

  function flashCard(key) {
    const card = document.getElementById(`card-${key}`);
    card.classList.remove('alert-flash');
    void card.offsetWidth; // trigger reflow
    card.classList.add('alert-flash');
  }

  // ── UI Rendering ──
  function updateClock() {
    const now = new Date();
    document.getElementById('clock').textContent =
      now.toLocaleTimeString('en-US', { hour12: false }) + ' ' +
      now.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

    // Simple market hours check (NYSE: 9:30-16:00 ET)
    const et = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
    const h = et.getHours(), m = et.getMinutes();
    const day = et.getDay();
    const isOpen = day >= 1 && day <= 5 && ((h === 9 && m >= 30) || (h > 9 && h < 16));
    const badge = document.getElementById('market-status');
    badge.textContent = isOpen ? 'MARKETS OPEN' : 'MARKETS CLOSED';
    badge.className = `badge ${isOpen ? 'badge-open' : 'badge-closed'}`;
  }

  function updateTicker() {
    const strip = document.getElementById('ticker-strip');
    strip.innerHTML = KEYS.map(key => {
      const inst = INSTRUMENTS[key];
      const price = state.prices[key];
      const pct = calcPctChange(key);
      const dir = pct >= 0 ? 'up' : 'down';
      const arrow = pct >= 0 ? '▲' : '▼';
      return `
        <div class="ticker-item">
          <span class="ticker-name">${inst.name}</span>
          <span class="ticker-price">${price.toFixed(inst.decimals)}</span>
          <span class="ticker-change ${dir}-bg">${arrow} ${Math.abs(pct).toFixed(2)}%</span>
        </div>
      `;
    }).join('');
  }

  function updateCharts() {
    KEYS.forEach(key => {
      const chart = state.charts[key];
      const inst = INSTRUMENTS[key];
      const data = chart.data;
      data.labels = state.history[key].map((_, i) => i);
      data.datasets[0].data = [...state.history[key]];

      // Update open line
      chart.options.plugins.annotation.annotations.openLine.yMin = state.opens[key];
      chart.options.plugins.annotation.annotations.openLine.yMax = state.opens[key];

      chart.update('none');

      // Update price display
      const price = state.prices[key];
      const pct = calcPctChange(key);
      const dir = pct >= 0 ? 'up' : 'down';

      document.getElementById(`price-${key}`).textContent = price.toFixed(inst.decimals);
      const changeEl = document.getElementById(`change-${key}`);
      changeEl.textContent = `${pct >= 0 ? '+' : ''}${pct.toFixed(2)}%`;
      changeEl.className = `change ${dir}-bg`;
    });
  }

  function updateVolatilityMetrics() {
    KEYS.forEach(key => {
      const inst = INSTRUMENTS[key];
      const intradayVol = calcIntradayVol(key) * 100;
      const range = calcDayRange(key);

      const volEl = document.getElementById(`vol-${key}`);
      if (volEl) volEl.textContent = intradayVol.toFixed(3) + '%';

      const rangeEl = document.getElementById(`range-${key}`);
      if (rangeEl) rangeEl.textContent =
        `${range.min.toFixed(inst.decimals)} – ${range.max.toFixed(inst.decimals)}`;

      // Special metrics per instrument
      if (key === 'sp500' || key === 'nasdaq' || key === 'dow') {
        const betaEl = document.getElementById(`beta-${key}`);
        if (betaEl) {
          const corr = calcCorrelation(state.history[key], state.history.sp500);
          betaEl.textContent = key === 'sp500' ? '1.00' : corr.toFixed(2);
        }
      }

      if (key === 'oil') {
        const geoEl = document.getElementById('geo-oil');
        if (geoEl) {
          const tension = state.geopoliticalTension;
          const label = tension > 0.7 ? 'ELEVATED' : tension > 0.4 ? 'MODERATE' : 'LOW';
          geoEl.textContent = label;
          geoEl.style.color = tension > 0.7 ? '#ef4444' : tension > 0.4 ? '#eab308' : '#22c55e';
        }
      }

      if (key === 'gold') {
        const havenEl = document.getElementById('haven-gold');
        if (havenEl) {
          const tension = state.geopoliticalTension;
          const flow = tension > 0.6 ? 'STRONG' : tension > 0.3 ? 'MODERATE' : 'WEAK';
          havenEl.textContent = flow;
          havenEl.style.color = tension > 0.6 ? '#22c55e' : tension > 0.3 ? '#eab308' : '#64748b';
        }
      }

      if (key === 'dxy') {
        const trendEl = document.getElementById('trend-dxy');
        if (trendEl) {
          const recent = state.history.dxy.slice(-20);
          const start = recent[0], end = recent[recent.length - 1];
          const trend = end > start ? 'STRENGTHENING' : 'WEAKENING';
          trendEl.textContent = trend;
          trendEl.style.color = end > start ? '#22c55e' : '#ef4444';
        }
      }
    });
  }

  function updateVIX() {
    const vix = state.vix;
    const el = document.getElementById('vix-value');
    el.textContent = vix.toFixed(1);
    el.style.color = vix > 35 ? '#ef4444' : vix > 25 ? '#f97316' : vix > 18 ? '#eab308' : '#22c55e';

    const gauge = document.getElementById('vix-gauge-fill');
    const pct = Math.min(100, (vix / 60) * 100);
    gauge.style.width = pct + '%';
    gauge.style.background = vix > 35 ? '#ef4444' : vix > 25 ? '#f97316' : vix > 18 ? '#eab308' : '#22c55e';
  }

  function updateVolTable() {
    const body = document.getElementById('vol-table-body');
    body.innerHTML = KEYS.map(key => {
      const inst = INSTRUMENTS[key];
      const hourVol = calc1hVol(key) * 100;
      const dayVol = calcIntradayVol(key) * 100;
      const statusClass = dayVol > 0.15 ? 'vol-extreme' : dayVol > 0.08 ? 'vol-high' :
                          dayVol > 0.04 ? 'vol-moderate' : 'vol-low';
      const statusLabel = dayVol > 0.15 ? 'EXTREME' : dayVol > 0.08 ? 'HIGH' :
                          dayVol > 0.04 ? 'MOD' : 'LOW';
      return `
        <div class="vol-row">
          <span>${inst.name}</span>
          <span>${hourVol.toFixed(3)}%</span>
          <span>${dayVol.toFixed(3)}%</span>
          <span class="vol-status ${statusClass}">${statusLabel}</span>
        </div>
      `;
    }).join('');
  }

  function updateCorrelationMatrix() {
    const container = document.getElementById('correlation-matrix');
    const labels = ['', ...KEYS.map(k => INSTRUMENTS[k].name.split(' ')[0])];

    let html = labels.map(l => `<div class="corr-cell corr-header">${l}</div>`).join('');

    KEYS.forEach(k1 => {
      html += `<div class="corr-cell corr-header">${INSTRUMENTS[k1].name.split(' ')[0]}</div>`;
      KEYS.forEach(k2 => {
        const corr = k1 === k2 ? 1 : calcCorrelation(state.history[k1], state.history[k2]);
        const absCorr = Math.abs(corr);
        const r = corr < 0 ? Math.round(180 + absCorr * 75) : Math.round(34);
        const g = corr < 0 ? Math.round(50) : Math.round(140 + absCorr * 57);
        const b = corr < 0 ? Math.round(50) : Math.round(34);
        const alpha = 0.15 + absCorr * 0.6;
        html += `<div class="corr-cell" style="background:rgba(${r},${g},${b},${alpha})">${corr.toFixed(2)}</div>`;
      });
    });

    container.innerHTML = html;
  }

  function renderAlerts() {
    const log = document.getElementById('alert-log');
    const countEl = document.getElementById('alert-count');
    countEl.textContent = state.alerts.length;

    log.innerHTML = state.alerts.slice(0, 20).map(alert => {
      const time = alert.time.toLocaleTimeString('en-US', { hour12: false });
      const sevClass = alert.severity === 'critical' ? 'down-bg' : 'up-bg';
      const sevLabel = alert.severity === 'critical' ? 'CRITICAL' : 'WARNING';
      return `
        <div class="alert-item">
          <span class="alert-time">${time}</span>
          <span class="alert-msg">${alert.message}</span>
          <span class="alert-severity ${sevClass}">${sevLabel}</span>
        </div>
      `;
    }).join('');
  }

  function renderNews() {
    const feed = document.getElementById('news-feed');
    const filtered = state.newsFilter === 'all'
      ? state.newsItems
      : state.newsItems.filter(n => n.tags.some(t => t.includes(state.newsFilter)));

    feed.innerHTML = filtered.slice(0, 15).map(item => {
      const time = item.time.toLocaleTimeString('en-US', { hour12: false });
      const tagHtml = item.tags.map(t => {
        const cls = t === 'iran' ? 'news-tag-iran' :
                    t === 'hormuz' ? 'news-tag-hormuz' :
                    t === 'oil' ? 'news-tag-oil' :
                    t === 'ceasefire' ? 'news-tag-ceasefire' : 'news-tag-market';
        return `<span class="news-tag ${cls}">${t}</span>`;
      }).join(' ');

      const impactDir = item.direction > 0 ? '▲ Bearish for equities' : '▼ Supportive for equities';
      const oilDir = item.direction > 0 ? '▲ Oil upward pressure' : '▼ Oil downward pressure';

      return `
        <div class="news-item">
          <div class="news-item-header">
            <div>${tagHtml}</div>
            <span class="news-time">${time}</span>
          </div>
          <div class="news-headline">${item.headline}</div>
          <div class="news-impact">${item.impact} · ${item.tags.includes('oil') ? oilDir : impactDir}</div>
        </div>
      `;
    }).join('');
  }

  // ── News Generation Timer ──
  function maybeGenerateNews() {
    if (Math.random() < 0.08) { // ~8% chance per second → ~1 per 12s
      const item = generateNewsItem();
      state.newsItems.unshift(item);
      if (state.newsItems.length > 50) state.newsItems.pop();

      // Geopolitical shock: news events can influence tension
      if (item.direction > 0) {
        state.geopoliticalTension = Math.min(1, state.geopoliticalTension + 0.05);
      } else {
        state.geopoliticalTension = Math.max(0, state.geopoliticalTension - 0.03);
      }

      renderNews();
    }
  }

  // ── Main Update Loop ──
  function tick() {
    simulatePriceUpdate();
    updateClock();
    updateTicker();
    updateCharts();
    updateVolatilityMetrics();
    updateVIX();
    updateVolTable();
    checkAlerts();
    maybeGenerateNews();

    // Correlation matrix updates less frequently (expensive)
    if (Date.now() % 5000 < UPDATE_INTERVAL) {
      updateCorrelationMatrix();
    }
  }

  // ── Event Handlers ──
  function setupEventHandlers() {
    // Theme toggle
    document.getElementById('btn-theme').addEventListener('click', () => {
      document.body.classList.toggle('light-theme');
    });

    // Alert sound toggle
    document.getElementById('btn-toggle-alerts').addEventListener('click', () => {
      state.alertsEnabled = !state.alertsEnabled;
      const btn = document.getElementById('btn-toggle-alerts');
      btn.textContent = state.alertsEnabled ? '🔔' : '🔕';
    });

    // Alert threshold
    document.getElementById('alert-threshold').addEventListener('change', (e) => {
      state.alertThreshold = parseFloat(e.target.value) || 2.0;
    });

    // Clear alerts
    document.getElementById('btn-clear-alerts').addEventListener('click', () => {
      state.alerts = [];
      renderAlerts();
    });

    // Dismiss banner
    document.getElementById('alert-dismiss').addEventListener('click', () => {
      document.getElementById('alert-banner').classList.add('hidden');
    });

    // News filters
    document.querySelectorAll('.news-filter').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.news-filter').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        state.newsFilter = btn.dataset.filter;
        renderNews();
      });
    });
  }

  // ── Bootstrap ──
  function init() {
    // Create all charts
    KEYS.forEach(createChart);

    // Seed initial news
    for (let i = 0; i < 5; i++) {
      const item = generateNewsItem();
      item.time = new Date(Date.now() - Math.random() * 600000);
      state.newsItems.push(item);
    }
    state.newsItems.sort((a, b) => b.time - a.time);

    // Setup handlers
    setupEventHandlers();

    // Initial render
    updateClock();
    updateTicker();
    updateVolatilityMetrics();
    updateVIX();
    updateVolTable();
    updateCorrelationMatrix();
    renderAlerts();
    renderNews();

    // Start update loop
    setInterval(tick, UPDATE_INTERVAL);
  }

  // Wait for DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
