/* ============================================================
   Geopolitical Market Dashboard — Core Application
   Real-time simulation with Chart.js, volatility metrics,
   alerts for >2% moves, and US-Iran / Strait of Hormuz feed.
   ============================================================ */

(function () {
  'use strict';

  // ── Asset Definitions ──────────────────────────────────────
  const ASSETS = {
    sp500:  { symbol: 'S&P 500',  base: 5280.00, color: '#3b82f6', volatility: 0.012, drift: 0.0001 },
    nasdaq: { symbol: 'NASDAQ',   base: 16750.00, color: '#8b5cf6', volatility: 0.015, drift: 0.00012 },
    dow:    { symbol: 'DOW 30',   base: 39800.00, color: '#06b6d4', volatility: 0.010, drift: 0.00008 },
    oil:    { symbol: 'WTI Crude',base: 78.50,    color: '#f97316', volatility: 0.020, drift: -0.0001 },
    gold:   { symbol: 'Gold',     base: 2340.00,  color: '#eab308', volatility: 0.008, drift: 0.00005 },
    dxy:    { symbol: 'DXY',      base: 104.20,   color: '#22c55e', volatility: 0.005, drift: 0.00002 },
  };

  const ALERT_THRESHOLD = 0.02; // 2%
  const UPDATE_INTERVAL = 1500; // ms between ticks
  const MAX_POINTS = 200;       // max data points per chart
  const VOL_WINDOW = 20;        // rolling volatility window

  // ── State ──────────────────────────────────────────────────
  const state = {
    prices: {},      // { assetKey: [{ time, price, open }] }
    opens: {},       // session open prices
    alerts: [],      // alert log entries
    newsItems: [],   // news feed items
    charts: {},      // Chart.js instances
    alertShown: {},  // track which alerts have been shown per asset
    tickCount: 0,
  };

  // ── Initialize Prices ──────────────────────────────────────
  function initPrices() {
    const now = Date.now();
    for (const [key, asset] of Object.entries(ASSETS)) {
      const openPrice = asset.base * (1 + (Math.random() - 0.5) * 0.01);
      state.opens[key] = openPrice;
      state.prices[key] = [];
      // Pre-fill some history
      let price = openPrice;
      for (let i = 60; i >= 0; i--) {
        price = simulateTick(price, asset);
        state.prices[key].push({
          time: new Date(now - i * UPDATE_INTERVAL),
          price: price,
          open: openPrice,
        });
      }
      state.opens[key] = openPrice;
    }
  }

  // ── Price Simulation (Geometric Brownian Motion) ───────────
  function simulateTick(currentPrice, asset) {
    const dt = UPDATE_INTERVAL / 60000;
    const drift = asset.drift * dt;
    const diffusion = asset.volatility * Math.sqrt(dt) * randn();
    // Add occasional jumps for geopolitical shock simulation
    let jump = 0;
    if (Math.random() < 0.003) {
      jump = (Math.random() - 0.5) * asset.volatility * 3;
    }
    return currentPrice * Math.exp(drift + diffusion + jump);
  }

  function randn() {
    let u = 0, v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
  }

  // ── Volatility Calculation ─────────────────────────────────
  function calcVolatility(prices, window) {
    if (prices.length < window + 1) return 0;
    const returns = [];
    const recent = prices.slice(-window - 1);
    for (let i = 1; i < recent.length; i++) {
      returns.push(Math.log(recent[i].price / recent[i - 1].price));
    }
    const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
    const variance = returns.reduce((a, b) => a + (b - mean) ** 2, 0) / (returns.length - 1);
    // Annualize: sqrt(252 trading days * 390 minutes / interval)
    const periodsPerDay = (390 * 60000) / UPDATE_INTERVAL;
    return Math.sqrt(variance * periodsPerDay * 252) * 100;
  }

  function calcRollingVolatilities(key) {
    const prices = state.prices[key];
    const vols = [];
    for (let i = VOL_WINDOW + 1; i <= prices.length; i++) {
      const slice = prices.slice(0, i);
      vols.push({
        time: prices[i - 1].time,
        vol: calcVolatility(slice, VOL_WINDOW),
      });
    }
    return vols;
  }

  // ── Percentage Change ──────────────────────────────────────
  function pctChange(key) {
    const prices = state.prices[key];
    if (!prices.length) return 0;
    const current = prices[prices.length - 1].price;
    const open = state.opens[key];
    return (current - open) / open;
  }

  function currentPrice(key) {
    const prices = state.prices[key];
    return prices.length ? prices[prices.length - 1].price : ASSETS[key].base;
  }

  function dayHigh(key) {
    return Math.max(...state.prices[key].map(p => p.price));
  }

  function dayLow(key) {
    return Math.min(...state.prices[key].map(p => p.price));
  }

  // ── Format Helpers ─────────────────────────────────────────
  function fmt(n, decimals) {
    if (decimals === undefined) {
      decimals = n > 1000 ? 2 : n > 100 ? 2 : 2;
    }
    return n.toLocaleString('en-US', {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    });
  }

  function fmtPct(n) {
    const sign = n >= 0 ? '+' : '';
    return sign + (n * 100).toFixed(2) + '%';
  }

  function fmtTime(d) {
    return d.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }

  // ── Clock ──────────────────────────────────────────────────
  function updateClock() {
    const now = new Date();
    document.getElementById('clock').textContent =
      now.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' }) +
      '  ' + fmtTime(now) + ' ET';

    // Market status (simplified: Mon-Fri 9:30-16:00 ET)
    const h = now.getHours(), m = now.getMinutes(), day = now.getDay();
    const marketOpen = day >= 1 && day <= 5 && (h > 9 || (h === 9 && m >= 30)) && h < 16;
    const el = document.getElementById('market-status');
    if (marketOpen) {
      el.classList.remove('closed');
      el.querySelector('.status-text').textContent = 'MARKET OPEN';
    } else {
      el.classList.add('closed');
      el.querySelector('.status-text').textContent = 'SIMULATED';
    }
  }

  // ── Metric Cards ───────────────────────────────────────────
  function renderMetricCards() {
    const container = document.getElementById('metrics-row');
    container.innerHTML = '';

    for (const [key, asset] of Object.entries(ASSETS)) {
      const price = currentPrice(key);
      const pct = pctChange(key);
      const change = price - state.opens[key];
      const vol = calcVolatility(state.prices[key], VOL_WINDOW);
      const isAlert = Math.abs(pct) >= ALERT_THRESHOLD;

      const card = document.createElement('div');
      card.className = 'metric-card' + (isAlert ? ' alert-active' : '');
      card.innerHTML = `
        <div class="accent-bar" style="background:${asset.color}"></div>
        <div class="label">${asset.symbol}</div>
        <div class="price" style="color:${asset.color}">${fmt(price)}</div>
        <div class="change-row">
          <span class="change ${pct >= 0 ? 'up' : 'down'}">${pct >= 0 ? '+' : ''}${fmt(change)}</span>
          <span class="pct ${pct >= 0 ? 'up' : 'down'}">${fmtPct(pct)}</span>
        </div>
        <span class="vol-badge">VOL ${vol.toFixed(1)}%</span>
      `;
      container.appendChild(card);
    }
  }

  // ── Ticker Strip ───────────────────────────────────────────
  function updateTicker() {
    const container = document.getElementById('ticker-content');
    let html = '';
    for (const [key, asset] of Object.entries(ASSETS)) {
      const price = currentPrice(key);
      const pct = pctChange(key);
      const dir = pct >= 0 ? 'up' : 'down';
      const arrow = pct >= 0 ? '\u25B2' : '\u25BC';
      html += `
        <span class="ticker-item">
          <span class="ticker-symbol">${asset.symbol}</span>
          <span class="ticker-price">${fmt(price)}</span>
          <span class="ticker-change ${dir}">${arrow} ${fmtPct(pct)}</span>
        </span>
      `;
    }
    // Duplicate for seamless scroll
    container.innerHTML = html + html;
  }

  // ── Charts ─────────────────────────────────────────────────
  function createCharts() {
    const baseOpts = {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 300 },
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: {
          labels: { color: '#94a3b8', font: { size: 11, family: 'monospace' }, boxWidth: 12 },
        },
        tooltip: {
          backgroundColor: '#1a1f2e',
          titleColor: '#e2e8f0',
          bodyColor: '#94a3b8',
          borderColor: '#2a3042',
          borderWidth: 1,
          titleFont: { family: 'monospace' },
          bodyFont: { family: 'monospace' },
        },
      },
      scales: {
        x: {
          ticks: { color: '#64748b', maxTicksLimit: 8, font: { size: 10, family: 'monospace' } },
          grid: { color: 'rgba(42,48,66,0.5)' },
        },
        y: {
          ticks: { color: '#64748b', font: { size: 10, family: 'monospace' } },
          grid: { color: 'rgba(42,48,66,0.5)' },
        },
      },
    };

    // Indices chart
    state.charts.indices = new Chart(document.getElementById('chart-indices'), {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          makeDataset('S&P 500', '#3b82f6'),
          makeDataset('NASDAQ', '#8b5cf6'),
          makeDataset('DOW 30', '#06b6d4'),
        ],
      },
      options: {
        ...baseOpts,
        scales: {
          ...baseOpts.scales,
          y: { ...baseOpts.scales.y, position: 'right' },
          y1: {
            display: true,
            position: 'left',
            ticks: { color: '#64748b', font: { size: 10, family: 'monospace' } },
            grid: { drawOnChartArea: false },
          },
        },
      },
    });

    // Commodities chart
    state.charts.commodities = new Chart(document.getElementById('chart-commodities'), {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          makeDataset('WTI Crude', '#f97316'),
          makeDataset('Gold', '#eab308'),
        ],
      },
      options: {
        ...baseOpts,
        scales: {
          ...baseOpts.scales,
          y: { ...baseOpts.scales.y, position: 'left' },
          y1: {
            display: true,
            position: 'right',
            ticks: { color: '#64748b', font: { size: 10, family: 'monospace' } },
            grid: { drawOnChartArea: false },
          },
        },
      },
    });

    // DXY chart
    state.charts.dxy = new Chart(document.getElementById('chart-dxy'), {
      type: 'line',
      data: {
        labels: [],
        datasets: [makeDataset('DXY', '#22c55e')],
      },
      options: {
        ...baseOpts,
        plugins: {
          ...baseOpts.plugins,
          annotation: {
            annotations: {
              openLine: {
                type: 'line',
                yMin: state.opens.dxy,
                yMax: state.opens.dxy,
                borderColor: 'rgba(100,116,139,0.5)',
                borderWidth: 1,
                borderDash: [6, 4],
                label: {
                  display: true,
                  content: 'Open',
                  position: 'start',
                  color: '#64748b',
                  font: { size: 10, family: 'monospace' },
                },
              },
            },
          },
        },
      },
    });

    // Volatility chart
    state.charts.volatility = new Chart(document.getElementById('chart-volatility'), {
      type: 'line',
      data: {
        labels: [],
        datasets: [
          { ...makeDataset('Oil Vol', '#f97316'), fill: true, backgroundColor: 'rgba(249,115,22,0.08)' },
          { ...makeDataset('Gold Vol', '#eab308'), fill: true, backgroundColor: 'rgba(234,179,8,0.08)' },
          { ...makeDataset('S&P Vol', '#3b82f6'), fill: true, backgroundColor: 'rgba(59,130,246,0.08)' },
          { ...makeDataset('DXY Vol', '#22c55e'), fill: true, backgroundColor: 'rgba(34,197,94,0.08)' },
        ],
      },
      options: {
        ...baseOpts,
        scales: {
          ...baseOpts.scales,
          y: {
            ...baseOpts.scales.y,
            title: {
              display: true,
              text: 'Annualized Vol %',
              color: '#64748b',
              font: { size: 10, family: 'monospace' },
            },
          },
        },
      },
    });
  }

  function makeDataset(label, color) {
    return {
      label: label,
      data: [],
      borderColor: color,
      backgroundColor: color + '15',
      borderWidth: 1.5,
      pointRadius: 0,
      pointHitRadius: 10,
      tension: 0.3,
      fill: false,
    };
  }

  function updateCharts() {
    const sp = state.prices.sp500;
    const labels = sp.map(p => fmtTime(p.time));

    // Indices — normalize to percentage change for overlay
    const c = state.charts.indices;
    c.data.labels = labels;
    c.data.datasets[0].data = state.prices.sp500.map(p => p.price);
    c.data.datasets[1].data = state.prices.nasdaq.map(p => p.price);
    c.data.datasets[2].data = state.prices.dow.map(p => p.price);
    // Assign DOW to y1 axis since its scale differs greatly
    c.data.datasets[0].yAxisID = 'y1';
    c.data.datasets[1].yAxisID = 'y';
    c.data.datasets[2].yAxisID = 'y1';
    c.update('none');

    // Commodities
    const cc = state.charts.commodities;
    cc.data.labels = labels;
    cc.data.datasets[0].data = state.prices.oil.map(p => p.price);
    cc.data.datasets[0].yAxisID = 'y';
    cc.data.datasets[1].data = state.prices.gold.map(p => p.price);
    cc.data.datasets[1].yAxisID = 'y1';
    cc.update('none');

    // DXY
    const cd = state.charts.dxy;
    cd.data.labels = labels;
    cd.data.datasets[0].data = state.prices.dxy.map(p => p.price);
    cd.update('none');

    // Volatility
    const cv = state.charts.volatility;
    const volOil = calcRollingVolatilities('oil');
    const volGold = calcRollingVolatilities('gold');
    const volSp = calcRollingVolatilities('sp500');
    const volDxy = calcRollingVolatilities('dxy');
    const volLabels = volOil.map(v => fmtTime(v.time));
    cv.data.labels = volLabels;
    cv.data.datasets[0].data = volOil.map(v => v.vol);
    cv.data.datasets[1].data = volGold.map(v => v.vol);
    cv.data.datasets[2].data = volSp.map(v => v.vol);
    cv.data.datasets[3].data = volDxy.map(v => v.vol);
    cv.update('none');
  }

  // ── Correlation / Snapshot Table ───────────────────────────
  function updateSnapshotTable() {
    const tbody = document.getElementById('corr-tbody');
    tbody.innerHTML = '';

    for (const [key, asset] of Object.entries(ASSETS)) {
      const price = currentPrice(key);
      const pct = pctChange(key);
      const vol = calcVolatility(state.prices[key], VOL_WINDOW);
      const high = dayHigh(key);
      const low = dayLow(key);

      let signal, signalClass;
      if (Math.abs(pct) >= ALERT_THRESHOLD) {
        signal = pct > 0 ? 'SURGE' : 'PLUNGE';
        signalClass = 'volatile';
      } else if (pct > 0.005) {
        signal = 'BULLISH';
        signalClass = 'bullish';
      } else if (pct < -0.005) {
        signal = 'BEARISH';
        signalClass = 'bearish';
      } else {
        signal = 'NEUTRAL';
        signalClass = 'neutral';
      }

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td style="color:${asset.color};font-weight:600">${asset.symbol}</td>
        <td>${fmt(price)}</td>
        <td style="color:${pct >= 0 ? 'var(--green)' : 'var(--red)'}">${fmtPct(pct)}</td>
        <td>${vol.toFixed(1)}%</td>
        <td style="font-size:0.72rem;color:var(--text-muted)">${fmt(low)} — ${fmt(high)}</td>
        <td><span class="signal-badge ${signalClass}">${signal}</span></td>
      `;
      tbody.appendChild(tr);
    }
  }

  // ── Alert System ───────────────────────────────────────────
  function checkAlerts() {
    for (const [key, asset] of Object.entries(ASSETS)) {
      const pct = pctChange(key);
      const absPct = Math.abs(pct);

      if (absPct >= ALERT_THRESHOLD && !state.alertShown[key]) {
        state.alertShown[key] = true;
        const direction = pct > 0 ? 'UP' : 'DOWN';
        const msg = `${asset.symbol} moved ${direction} ${(absPct * 100).toFixed(2)}% — potential geopolitical catalyst (US-Iran / Hormuz developments)`;

        // Banner
        showBannerAlert(msg);

        // Log
        addAlertLog('critical', msg);

        // If oil moves sharply, add a correlated analysis alert
        if (key === 'oil') {
          setTimeout(() => {
            addAlertLog('warning', `Oil ${direction.toLowerCase()} ${(absPct * 100).toFixed(1)}% — monitoring Strait of Hormuz shipping lane impact on energy markets`);
          }, 2000);
        }

        if (key === 'gold') {
          setTimeout(() => {
            addAlertLog('info', `Gold safe-haven flow detected — ${direction.toLowerCase()} ${(absPct * 100).toFixed(1)}% amid geopolitical uncertainty`);
          }, 3000);
        }
      }

      // Reset alert if price normalizes
      if (absPct < ALERT_THRESHOLD * 0.7 && state.alertShown[key]) {
        state.alertShown[key] = false;
      }
    }
  }

  function showBannerAlert(msg) {
    const banner = document.getElementById('alert-banner');
    document.getElementById('alert-content').textContent = msg;
    banner.classList.remove('hidden');
  }

  function addAlertLog(type, msg) {
    const now = new Date();
    state.alerts.unshift({ type, msg, time: now });
    if (state.alerts.length > 50) state.alerts.pop();
    renderAlertLog();
  }

  function renderAlertLog() {
    const ul = document.getElementById('alert-log');
    ul.innerHTML = '';
    for (const a of state.alerts.slice(0, 20)) {
      const li = document.createElement('li');
      li.innerHTML = `
        <span class="alert-type ${a.type}">${a.type.toUpperCase()}</span>
        <span><span class="news-time">${fmtTime(a.time)}</span>${a.msg}</span>
      `;
      ul.appendChild(li);
    }
  }

  // ── Geopolitical News Feed ─────────────────────────────────
  const NEWS_TEMPLATES = [
    { tag: 'breaking', text: 'US State Department confirms new round of talks with Iranian delegation on nuclear deal framework' },
    { tag: 'breaking', text: 'Iranian Foreign Ministry issues statement on ceasefire terms — markets react to de-escalation signals' },
    { tag: 'update',   text: 'US Navy 5th Fleet reports increased maritime patrol activity near Strait of Hormuz' },
    { tag: 'update',   text: 'IRGC naval forces conduct exercises near Hormuz chokepoint — Pentagon monitoring' },
    { tag: 'market',   text: 'Oil tanker insurance premiums rise 15% for Strait of Hormuz transit routes' },
    { tag: 'analysis', text: 'Goldman Sachs: Oil could spike $15/bbl if Strait of Hormuz disrupted — risk premium rising' },
    { tag: 'breaking', text: 'Reuters: US and Iran agree to temporary ceasefire along proxy conflict zones' },
    { tag: 'update',   text: 'CENTCOM commander briefs Congress on Persian Gulf force posture changes' },
    { tag: 'market',   text: 'LNG spot prices in Asia surge on Hormuz strait transit uncertainty' },
    { tag: 'analysis', text: 'JPMorgan note: Gold safe-haven premium at 3-month high on Middle East risk' },
    { tag: 'breaking', text: 'UN Security Council emergency session on Strait of Hormuz shipping disruptions' },
    { tag: 'update',   text: 'Saudi Arabia reaffirms commitment to OPEC+ output targets amid regional tensions' },
    { tag: 'market',   text: 'Brent-WTI spread widens as Hormuz transit risks increase freight costs' },
    { tag: 'analysis', text: 'Citi research: DXY strength correlated with safe-haven flows amid Iran tensions' },
    { tag: 'breaking', text: 'White House National Security Advisor discusses Iran policy in press briefing' },
    { tag: 'update',   text: 'Lloyd\'s of London updates war risk zones to include expanded Hormuz corridor' },
    { tag: 'market',   text: 'Defense sector ETFs outperform broad market on Middle East escalation fears' },
    { tag: 'analysis', text: 'Morgan Stanley: S&P 500 downside risk of 5-8% if Hormuz conflict escalates' },
    { tag: 'breaking', text: 'Iranian President signals willingness to resume nuclear negotiations with US' },
    { tag: 'update',   text: 'Commercial shipping firms reroute vessels away from Strait of Hormuz' },
    { tag: 'market',   text: 'VIX futures curve inverts — markets pricing near-term geopolitical shock' },
    { tag: 'analysis', text: 'BlackRock geopolitical risk indicator reaches elevated level on Iran developments' },
    { tag: 'breaking', text: 'EU foreign policy chief proposes new framework for US-Iran ceasefire enforcement' },
    { tag: 'update',   text: 'US Central Command repositions carrier strike group to Arabian Sea' },
    { tag: 'market',   text: 'Energy sector leads S&P 500 gains as oil prices rally on supply concerns' },
    { tag: 'analysis', text: 'BofA: Gold could test $2,500 if Strait of Hormuz situation deteriorates further' },
    { tag: 'breaking', text: 'Breaking: Iran JCPOA compliance report shows progress on enrichment limits' },
    { tag: 'update',   text: 'Qatar mediating backchannel discussions between Washington and Tehran' },
    { tag: 'market',   text: 'Treasury yields drop as investors seek safety amid Middle East developments' },
    { tag: 'analysis', text: 'Deutsche Bank: Recommends overweight energy, underweight consumer discretionary' },
  ];

  let newsIndex = 0;

  function addNewsItem() {
    const template = NEWS_TEMPLATES[newsIndex % NEWS_TEMPLATES.length];
    newsIndex++;

    const now = new Date();
    const item = {
      tag: template.tag,
      text: template.text,
      time: now,
    };

    state.newsItems.unshift(item);
    if (state.newsItems.length > 30) state.newsItems.pop();
    renderNewsFeed();
  }

  function renderNewsFeed() {
    const ul = document.getElementById('news-feed');
    ul.innerHTML = '';
    for (const n of state.newsItems) {
      const li = document.createElement('li');
      li.innerHTML = `
        <span class="news-time">${fmtTime(n.time)}</span>
        <span class="news-tag ${n.tag}">${n.tag}</span>
        ${n.text}
      `;
      ul.appendChild(li);
    }
  }

  // ── Main Update Loop ──────────────────────────────────────
  function tick() {
    state.tickCount++;

    // Generate new prices
    const now = new Date();
    for (const [key, asset] of Object.entries(ASSETS)) {
      const lastPrice = currentPrice(key);
      const newPrice = simulateTick(lastPrice, asset);
      state.prices[key].push({ time: now, price: newPrice, open: state.opens[key] });

      // Trim to max points
      if (state.prices[key].length > MAX_POINTS) {
        state.prices[key].shift();
      }
    }

    // Update all components
    renderMetricCards();
    updateTicker();
    updateCharts();
    updateSnapshotTable();
    checkAlerts();

    // Add news every ~15 ticks (~22 seconds)
    if (state.tickCount % 15 === 0) {
      addNewsItem();
    }
  }

  // ── Event Handlers ─────────────────────────────────────────
  function bindEvents() {
    // Dismiss alert banner
    document.getElementById('alert-dismiss').addEventListener('click', () => {
      document.getElementById('alert-banner').classList.add('hidden');
    });

    // Clear alert log
    document.getElementById('clear-alerts').addEventListener('click', () => {
      state.alerts = [];
      renderAlertLog();
    });

    // Timeframe buttons — change update speed to simulate different intervals
    document.querySelectorAll('.tf-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const group = e.target.dataset.group;
        document.querySelectorAll(`.tf-btn[data-group="${group}"]`).forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
      });
    });
  }

  // ── Initialization ─────────────────────────────────────────
  function init() {
    initPrices();
    createCharts();
    updateClock();
    renderMetricCards();
    updateTicker();
    updateCharts();
    updateSnapshotTable();
    bindEvents();

    // Seed initial news
    for (let i = 0; i < 5; i++) {
      addNewsItem();
    }

    // Add startup alerts
    addAlertLog('info', 'Dashboard initialized — monitoring US market indices, oil, gold, and DXY');
    addAlertLog('info', 'Alert threshold set at \u00B12% for geopolitical move detection');
    addAlertLog('warning', 'Geopolitical risk elevated — US-Iran ceasefire talks and Strait of Hormuz activity under watch');

    // Start loops
    setInterval(tick, UPDATE_INTERVAL);
    setInterval(updateClock, 1000);
  }

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
