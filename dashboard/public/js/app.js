/* =============================================
   Geopolitical Market Dashboard - Application
   =============================================
   Tracks: S&P 500, Nasdaq, Dow, Oil, USD Index, Gold
   Alerts: 2%+ moves tied to US-Iran / Strait of Hormuz
   ============================================= */

(function () {
  'use strict';

  // ── Configuration ──────────────────────────────
  const SYMBOLS = [
    { id: '^GSPC',    name: 'S&P 500',        color: '#448aff', type: 'index' },
    { id: '^IXIC',    name: 'Nasdaq',          color: '#b388ff', type: 'index' },
    { id: '^DJI',     name: 'Dow Jones',       color: '#00e5ff', type: 'index' },
    { id: 'CL=F',     name: 'Crude Oil (WTI)', color: '#ff9100', type: 'commodity' },
    { id: 'DX-Y.NYB', name: 'US Dollar Index', color: '#00e676', type: 'fx' },
    { id: 'GC=F',     name: 'Gold',            color: '#ffd740', type: 'commodity' }
  ];

  // ── State ──────────────────────────────────────
  let activeSymbol = '^GSPC';
  let activeRange = '1d';
  let activeInterval = '5m';
  let refreshTimer = null;
  let alertThreshold = 2;
  let alertHistory = [];
  let previousQuotes = {};
  let sparkCharts = {};
  let mainChart = null;
  let chartDataCache = {};

  // ── DOM References ─────────────────────────────
  const $marketStatus = document.getElementById('marketStatus');
  const $lastUpdate = document.getElementById('lastUpdate');
  const $alertBanner = document.getElementById('alertBanner');
  const $alertText = document.getElementById('alertText');
  const $alertLog = document.getElementById('alertLog');
  const $volTable = document.getElementById('volTable');
  const $newsList = document.getElementById('newsList');
  const $refreshSelect = document.getElementById('refreshInterval');
  const $thresholdSelect = document.getElementById('alertThreshold');

  // ── Utilities ──────────────────────────────────
  function formatPrice(val, symbol) {
    if (val == null) return '--';
    const isIndex = ['^GSPC', '^IXIC', '^DJI'].includes(symbol);
    if (isIndex) return val.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return val.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function formatChange(change, pct) {
    if (change == null || pct == null) return { text: '--', cls: '' };
    const sign = change >= 0 ? '+' : '';
    const text = `${sign}${change.toFixed(2)} (${sign}${pct.toFixed(2)}%)`;
    const cls = change >= 0 ? 'positive' : 'negative';
    return { text, cls };
  }

  function formatVolume(vol) {
    if (vol == null) return '--';
    if (vol >= 1e9) return (vol / 1e9).toFixed(1) + 'B';
    if (vol >= 1e6) return (vol / 1e6).toFixed(1) + 'M';
    if (vol >= 1e3) return (vol / 1e3).toFixed(1) + 'K';
    return vol.toString();
  }

  function timeAgo(dateStr) {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return `${mins}m ago`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs}h ago`;
    return `${Math.floor(hrs / 24)}d ago`;
  }

  function nowTimeStr() {
    return new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }

  // ── API Calls ──────────────────────────────────
  async function fetchQuotes() {
    const res = await fetch('/api/quotes');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  async function fetchChart(symbol, range, interval) {
    const res = await fetch(`/api/chart/${encodeURIComponent(symbol)}?range=${range}&interval=${interval}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  async function fetchVolatility(symbol) {
    const res = await fetch(`/api/volatility/${encodeURIComponent(symbol)}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  async function fetchNews() {
    const res = await fetch('/api/news');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  // ── Card Updates ───────────────────────────────
  function updateCards(quotes) {
    for (const q of quotes) {
      const card = document.querySelector(`.card[data-symbol="${q.symbol}"]`);
      if (!card) continue;

      card.querySelector('.card-price').textContent = formatPrice(q.price, q.symbol);
      const chg = formatChange(q.change, q.changePercent);
      const changeEl = card.querySelector('.card-change');
      changeEl.textContent = chg.text;
      changeEl.className = `card-change ${chg.cls}`;

      // Highlight active card
      card.classList.toggle('active', q.symbol === activeSymbol);

      // Check alerts
      checkAlert(q);
    }

    // Update market status
    const firstQuote = quotes[0];
    const dot = $marketStatus.querySelector('.status-dot');
    const text = $marketStatus.querySelector('.status-text');
    if (firstQuote) {
      const state = firstQuote.marketState;
      if (state === 'REGULAR') {
        dot.className = 'status-dot live';
        text.textContent = 'Market Open';
      } else if (state === 'PRE') {
        dot.className = 'status-dot live';
        text.textContent = 'Pre-Market';
      } else if (state === 'POST' || state === 'POSTPOST') {
        dot.className = 'status-dot closed';
        text.textContent = 'After Hours';
      } else {
        dot.className = 'status-dot closed';
        text.textContent = 'Market Closed';
      }
    }

    $lastUpdate.textContent = `Updated ${nowTimeStr()}`;
  }

  // ── Sparkline Charts ───────────────────────────
  async function updateSparklines() {
    for (const sym of SYMBOLS) {
      try {
        const data = await fetchChart(sym.id, '1d', '5m');
        if (!data.points || data.points.length < 2) continue;

        const card = document.querySelector(`.card[data-symbol="${sym.id}"]`);
        if (!card) continue;
        const canvas = card.querySelector('.card-spark');
        const ctx = canvas.getContext('2d');

        // Destroy existing
        if (sparkCharts[sym.id]) sparkCharts[sym.id].destroy();

        const closes = data.points.map(p => p.close);
        const isUp = closes[closes.length - 1] >= closes[0];
        const lineColor = isUp ? '#00e676' : '#ff1744';

        sparkCharts[sym.id] = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.points.map(p => p.time),
            datasets: [{
              data: closes,
              borderColor: lineColor,
              borderWidth: 1.5,
              fill: true,
              backgroundColor: isUp ? '#00e67615' : '#ff174415',
              pointRadius: 0,
              tension: 0.3
            }]
          },
          options: {
            responsive: false,
            animation: false,
            plugins: { legend: { display: false }, tooltip: { enabled: false } },
            scales: { x: { display: false }, y: { display: false } },
            elements: { line: { borderJoinStyle: 'round' } }
          }
        });

        // Cache chart data for the active symbol
        chartDataCache[sym.id] = data;
      } catch { /* skip failed sparklines */ }
    }
  }

  // ── Main Chart ─────────────────────────────────
  async function updateMainChart(forceRefresh) {
    const cacheKey = `${activeSymbol}_${activeRange}_${activeInterval}`;
    let data;

    if (!forceRefresh && chartDataCache[cacheKey]) {
      data = chartDataCache[cacheKey];
    } else {
      try {
        data = await fetchChart(activeSymbol, activeRange, activeInterval);
        chartDataCache[cacheKey] = data;
      } catch (err) {
        console.error('Chart fetch failed:', err);
        return;
      }
    }

    if (!data.points || data.points.length === 0) return;

    const sym = SYMBOLS.find(s => s.id === activeSymbol);
    const closes = data.points.map(p => p.close);
    const times = data.points.map(p => new Date(p.time));
    const isUp = closes[closes.length - 1] >= (data.previousClose || closes[0]);
    const lineColor = isUp ? '#00e676' : '#ff1744';

    // Previous close reference line
    const prevClose = data.previousClose;
    const refLine = prevClose ? Array(closes.length).fill(prevClose) : null;

    const ctx = document.getElementById('mainChart').getContext('2d');

    if (mainChart) mainChart.destroy();

    const datasets = [{
      label: sym ? sym.name : activeSymbol,
      data: closes,
      borderColor: sym ? sym.color : lineColor,
      borderWidth: 2,
      fill: true,
      backgroundColor: (sym ? sym.color : lineColor) + '15',
      pointRadius: 0,
      pointHoverRadius: 4,
      pointHoverBackgroundColor: '#fff',
      tension: 0.2
    }];

    if (refLine) {
      datasets.push({
        label: 'Prev Close',
        data: refLine,
        borderColor: '#5a617850',
        borderWidth: 1,
        borderDash: [5, 5],
        fill: false,
        pointRadius: 0,
        pointHoverRadius: 0
      });
    }

    mainChart = new Chart(ctx, {
      type: 'line',
      data: { labels: times, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 300 },
        interaction: {
          mode: 'index',
          intersect: false
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#1a1f35ee',
            titleColor: '#e8eaf0',
            bodyColor: '#8b92a8',
            borderColor: '#2a3050',
            borderWidth: 1,
            padding: 10,
            displayColors: false,
            callbacks: {
              title: function (items) {
                const d = new Date(items[0].label);
                return d.toLocaleString('en-US', {
                  month: 'short', day: 'numeric',
                  hour: '2-digit', minute: '2-digit'
                });
              },
              label: function (item) {
                if (item.datasetIndex === 0) {
                  return `${sym ? sym.name : activeSymbol}: ${formatPrice(item.raw, activeSymbol)}`;
                }
                return `Prev Close: ${formatPrice(item.raw, activeSymbol)}`;
              }
            }
          }
        },
        scales: {
          x: {
            type: 'time',
            grid: { color: '#2a305040' },
            ticks: {
              color: '#5a6178',
              font: { size: 10, family: "'SF Mono', monospace" },
              maxTicksLimit: 10
            },
            border: { color: '#2a3050' }
          },
          y: {
            grid: { color: '#2a305040' },
            ticks: {
              color: '#5a6178',
              font: { size: 10, family: "'SF Mono', monospace" },
              callback: function (val) { return formatPrice(val, activeSymbol); }
            },
            border: { color: '#2a3050' }
          }
        }
      }
    });

    // Update chart info bar
    const last = data.points[data.points.length - 1];
    document.getElementById('infoOpen').textContent = formatPrice(last.open, activeSymbol);
    document.getElementById('infoHigh').textContent = formatPrice(last.high, activeSymbol);
    document.getElementById('infoLow').textContent = formatPrice(last.low, activeSymbol);
    document.getElementById('infoClose').textContent = formatPrice(last.close, activeSymbol);
    document.getElementById('infoVol').textContent = formatVolume(last.volume);
  }

  // ── Volatility Table ───────────────────────────
  async function updateVolatility() {
    const tbody = $volTable.querySelector('tbody');
    const rows = [];

    for (const sym of SYMBOLS) {
      try {
        const vol = await fetchVolatility(sym.id);
        const annVol = parseFloat(vol.annualizedVolatility);
        let volClass = 'vol-low';
        if (annVol > 30) volClass = 'vol-high';
        else if (annVol > 15) volClass = 'vol-medium';

        rows.push(`
          <tr>
            <td style="color:${sym.color}; font-weight:600;">${sym.name}</td>
            <td class="${volClass}">${vol.dailyVolatility}%</td>
            <td class="${volClass}">${vol.annualizedVolatility}%</td>
            <td>${vol.maxDrawdown}%</td>
            <td>${vol.averageTrueRange}</td>
          </tr>
        `);
      } catch {
        rows.push(`
          <tr>
            <td style="color:${sym.color}">${sym.name}</td>
            <td colspan="4" style="color:#5a6178;">N/A</td>
          </tr>
        `);
      }
    }

    tbody.innerHTML = rows.join('');
  }

  // ── Alert System ───────────────────────────────
  function checkAlert(quote) {
    const pct = Math.abs(quote.changePercent || 0);
    if (pct < alertThreshold) return;

    // Avoid duplicate alerts for the same symbol within 5 minutes
    const recentKey = `${quote.symbol}_${Math.floor(Date.now() / 300000)}`;
    if (alertHistory.includes(recentKey)) return;
    alertHistory.push(recentKey);
    if (alertHistory.length > 100) alertHistory = alertHistory.slice(-50);

    const isUp = quote.change >= 0;
    const direction = isUp ? 'UP' : 'DOWN';
    const msg = `${quote.name || quote.symbol} ${direction} ${Math.abs(quote.changePercent).toFixed(2)}% ($${formatPrice(quote.price, quote.symbol)})`;

    // Show banner
    $alertBanner.style.display = 'flex';
    $alertText.textContent = `ALERT: ${msg} - Monitor for geopolitical impact (US-Iran / Strait of Hormuz)`;

    // Add to log
    const logItem = document.createElement('div');
    logItem.className = `alert-item ${isUp ? 'alert-up' : 'alert-down'}`;
    logItem.innerHTML = `
      <span class="alert-time">${nowTimeStr()}</span>
      <span class="alert-msg">${msg}</span>
    `;

    const empty = $alertLog.querySelector('.alert-empty');
    if (empty) empty.remove();

    $alertLog.insertBefore(logItem, $alertLog.firstChild);

    // Flash the card
    const card = document.querySelector(`.card[data-symbol="${quote.symbol}"]`);
    if (card) {
      card.classList.remove('alert-flash');
      void card.offsetWidth; // reflow
      card.classList.add('alert-flash');
    }

    // Keep log trimmed
    while ($alertLog.children.length > 30) {
      $alertLog.removeChild($alertLog.lastChild);
    }
  }

  // ── News Feed ──────────────────────────────────
  async function updateNews() {
    try {
      const data = await fetchNews();
      if (!data.news || data.news.length === 0) {
        $newsList.innerHTML = '<div class="news-loading">No relevant headlines found.</div>';
        return;
      }

      const items = data.news.map(item => {
        let tagClass = 'news-tag';
        let tagLabel = 'GEOPOLITICAL';
        const titleLower = item.title.toLowerCase();
        if (titleLower.includes('iran')) { tagClass += ' tag-iran'; tagLabel = 'IRAN'; }
        else if (titleLower.includes('hormuz')) { tagClass += ' tag-hormuz'; tagLabel = 'HORMUZ'; }
        else if (titleLower.includes('oil') || titleLower.includes('crude')) { tagClass += ' tag-oil'; tagLabel = 'OIL'; }

        return `
          <div class="news-item">
            <a href="${item.link}" target="_blank" rel="noopener">${item.title}</a>
            <div class="news-meta">
              <span>${item.source ? item.source + ' - ' : ''}${item.pubDate ? timeAgo(item.pubDate) : ''}</span>
              <span class="${tagClass}">${tagLabel}</span>
            </div>
          </div>
        `;
      });

      $newsList.innerHTML = items.join('');
    } catch (err) {
      console.error('News fetch error:', err);
      $newsList.innerHTML = '<div class="news-loading">Failed to load news. Retrying...</div>';
    }
  }

  // ── Master Refresh ─────────────────────────────
  async function refreshAll() {
    const dot = $marketStatus.querySelector('.status-dot');
    dot.className = 'status-dot'; // reset while loading

    try {
      // Quotes first (fastest, most critical)
      const quotesData = await fetchQuotes();
      if (quotesData.quotes) {
        updateCards(quotesData.quotes);
        dot.className = 'status-dot live';
      }
    } catch (err) {
      console.error('Quotes refresh failed:', err);
      const dot2 = $marketStatus.querySelector('.status-dot');
      dot2.className = 'status-dot error';
      $marketStatus.querySelector('.status-text').textContent = 'Connection Error';
    }

    // Chart, sparklines, volatility, and news in parallel
    try {
      await Promise.allSettled([
        updateMainChart(true),
        updateSparklines(),
        updateVolatility(),
        updateNews()
      ]);
    } catch (err) {
      console.error('Refresh error:', err);
    }
  }

  // ── Event Handlers ─────────────────────────────

  // Card click -> select instrument
  document.getElementById('cardsGrid').addEventListener('click', (e) => {
    const card = e.target.closest('.card');
    if (!card) return;
    const symbol = card.dataset.symbol;
    if (symbol) {
      activeSymbol = symbol;
      // Update active states
      document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      document.querySelectorAll('.chart-tab').forEach(t => {
        t.classList.toggle('active', t.dataset.symbol === symbol);
      });
      updateMainChart(true);
    }
  });

  // Chart tab click
  document.getElementById('chartTabs').addEventListener('click', (e) => {
    if (!e.target.classList.contains('chart-tab')) return;
    const symbol = e.target.dataset.symbol;
    activeSymbol = symbol;
    document.querySelectorAll('.chart-tab').forEach(t => t.classList.remove('active'));
    e.target.classList.add('active');
    document.querySelectorAll('.card').forEach(c => {
      c.classList.toggle('active', c.dataset.symbol === symbol);
    });
    updateMainChart(true);
  });

  // Range tab click
  document.getElementById('rangeTabs').addEventListener('click', (e) => {
    if (!e.target.classList.contains('range-tab')) return;
    activeRange = e.target.dataset.range;
    activeInterval = e.target.dataset.interval;
    document.querySelectorAll('.range-tab').forEach(t => t.classList.remove('active'));
    e.target.classList.add('active');
    updateMainChart(true);
  });

  // Refresh interval select
  $refreshSelect.addEventListener('change', () => {
    const val = parseInt($refreshSelect.value, 10);
    document.getElementById('footerRefresh').textContent = val > 0 ? `${val}s` : 'manual';
    setupRefreshTimer(val);
  });

  // Alert threshold select
  $thresholdSelect.addEventListener('change', () => {
    alertThreshold = parseFloat($thresholdSelect.value);
    document.getElementById('footerThreshold').textContent = `${alertThreshold}%`;
  });

  // Manual refresh button
  document.getElementById('refreshBtn').addEventListener('click', () => {
    refreshAll();
  });

  // Dismiss alert banner
  document.getElementById('alertDismiss').addEventListener('click', () => {
    $alertBanner.style.display = 'none';
  });

  // ── Refresh Timer ──────────────────────────────
  function setupRefreshTimer(seconds) {
    if (refreshTimer) clearInterval(refreshTimer);
    if (seconds > 0) {
      refreshTimer = setInterval(refreshAll, seconds * 1000);
    }
  }

  // ── Initialize ─────────────────────────────────
  async function init() {
    console.log('Dashboard initializing...');
    await refreshAll();
    setupRefreshTimer(30);
    console.log('Dashboard ready. Auto-refresh: 30s');
  }

  // Start
  init();

})();
