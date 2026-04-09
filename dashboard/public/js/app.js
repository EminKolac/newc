// ============================================================
// Geopolitical Market Dashboard — Frontend Application
// ============================================================

const SYMBOLS = {
  '^GSPC':    { name: 'S&P 500',         category: 'index' },
  '^IXIC':    { name: 'Nasdaq Composite', category: 'index' },
  '^DJI':     { name: 'Dow Jones',        category: 'index' },
  'CL=F':     { name: 'Crude Oil (WTI)',  category: 'commodity' },
  'DX-Y.NYB': { name: 'US Dollar Index',  category: 'currency' },
  'GC=F':     { name: 'Gold',             category: 'commodity' },
};

let activeSymbol = '^GSPC';
let activeRange = '5d';
let mainChart = null;
let previousPrices = {};
let audioCtx = null;

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
  buildInstrumentCards();
  initChart();
  initTabs();
  startClock();
  connectSSE();
  fetchInitialData();
  fetchNews();
  setInterval(fetchNews, 120000); // refresh news every 2 min
});

// ===== Build instrument cards =====
function buildInstrumentCards() {
  const grid = document.getElementById('instrumentsGrid');
  grid.innerHTML = '';
  for (const [symbol, info] of Object.entries(SYMBOLS)) {
    const card = document.createElement('div');
    card.className = `instrument-card flat ${symbol === activeSymbol ? 'active' : ''}`;
    card.dataset.symbol = symbol;
    card.innerHTML = `
      <div class="card-header">
        <span class="card-name">${info.name}</span>
        <span class="card-category ${info.category}">${info.category}</span>
      </div>
      <div class="card-price" id="price-${css(symbol)}">--</div>
      <div class="card-change flat" id="change-${css(symbol)}">
        <span class="change-abs">--</span>
        <span class="change-pct">(--)</span>
      </div>
      <div class="card-volume" id="vol-${css(symbol)}">Vol: --</div>
    `;
    card.addEventListener('click', () => selectSymbol(symbol));
    grid.appendChild(card);
  }
}

function css(symbol) {
  return symbol.replace(/[^a-zA-Z0-9]/g, '_');
}

// ===== Select symbol for chart =====
function selectSymbol(symbol) {
  activeSymbol = symbol;
  document.querySelectorAll('.instrument-card').forEach((c) => c.classList.remove('active'));
  document.querySelector(`.instrument-card[data-symbol="${symbol}"]`)?.classList.add('active');
  document.querySelectorAll('.chart-tab').forEach((t) => {
    t.classList.toggle('active', t.dataset.symbol === symbol);
  });
  loadChart(symbol, activeRange);
}

// ===== Tab controls =====
function initTabs() {
  document.querySelectorAll('.chart-tab').forEach((tab) => {
    tab.addEventListener('click', () => selectSymbol(tab.dataset.symbol));
  });
  document.querySelectorAll('.range-tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      activeRange = tab.dataset.range;
      document.querySelectorAll('.range-tab').forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');
      loadChart(activeSymbol, activeRange);
    });
  });
}

// ===== Clock =====
function startClock() {
  function tick() {
    const now = new Date();
    document.getElementById('clock').textContent = now.toLocaleTimeString('en-US', {
      hour12: false, timeZone: 'America/New_York',
    }) + ' ET';
  }
  tick();
  setInterval(tick, 1000);
}

// ===== SSE Real-time Connection =====
function connectSSE() {
  const statusDot = document.querySelector('.status-dot');
  const statusText = document.querySelector('.status-text');

  const es = new EventSource('/api/stream');

  es.onopen = () => {
    statusDot.className = 'status-dot connected';
    statusText.textContent = 'Live';
  };

  es.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.type === 'quotes') updateQuotes(msg.data);
    if (msg.type === 'alert') addAlert(msg.data);
  };

  es.onerror = () => {
    statusDot.className = 'status-dot error';
    statusText.textContent = 'Reconnecting...';
  };
}

// ===== Fetch initial data =====
async function fetchInitialData() {
  try {
    const [quotesRes, alertsRes] = await Promise.all([
      fetch('/api/quotes'),
      fetch('/api/alerts'),
    ]);
    const quotes = await quotesRes.json();
    const alerts = await alertsRes.json();
    updateQuotes(quotes);
    alerts.forEach(addAlert);
    loadChart(activeSymbol, activeRange);
  } catch (err) {
    console.error('Initial data fetch failed:', err);
  }
}

// ===== Update quote cards =====
function updateQuotes(quotes) {
  let anyOpen = false;
  for (const [symbol, q] of Object.entries(quotes)) {
    const id = css(symbol);
    const priceEl = document.getElementById(`price-${id}`);
    const changeEl = document.getElementById(`change-${id}`);
    const volEl = document.getElementById(`vol-${id}`);
    const card = document.querySelector(`.instrument-card[data-symbol="${symbol}"]`);
    if (!priceEl || !q) continue;

    // Determine direction
    const dir = q.changePct > 0.01 ? 'up' : q.changePct < -0.01 ? 'down' : 'flat';

    // Flash on price change
    const prev = previousPrices[symbol];
    if (prev && prev !== q.price) {
      priceEl.classList.remove('flash-up', 'flash-down');
      void priceEl.offsetWidth; // reflow
      priceEl.classList.add(q.price > prev ? 'flash-up' : 'flash-down');
    }
    previousPrices[symbol] = q.price;

    // Update values
    priceEl.textContent = formatPrice(q.price, symbol);
    changeEl.className = `card-change ${dir}`;
    const arrow = dir === 'up' ? '▲' : dir === 'down' ? '▼' : '●';
    changeEl.innerHTML = `
      <span>${arrow} ${q.change >= 0 ? '+' : ''}${formatPrice(q.change, symbol)}</span>
      <span>(${q.changePct >= 0 ? '+' : ''}${q.changePct.toFixed(2)}%)</span>
    `;
    volEl.textContent = `Vol: ${formatVolume(q.volume)}`;

    // Card border color
    card.classList.remove('up', 'down', 'flat');
    card.classList.add(dir);

    // Market state
    if (q.marketState === 'REGULAR') anyOpen = true;
  }

  const stateEl = document.getElementById('marketState');
  if (anyOpen) {
    stateEl.textContent = 'Market Open';
    stateEl.className = 'market-state open';
  } else {
    stateEl.textContent = 'Market Closed';
    stateEl.className = 'market-state closed';
  }
}

// ===== Chart =====
function initChart() {
  const ctx = document.getElementById('mainChart').getContext('2d');
  mainChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Price',
        data: [],
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59,130,246,0.08)',
        borderWidth: 1.5,
        pointRadius: 0,
        pointHitRadius: 10,
        fill: true,
        tension: 0.1,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { intersect: false, mode: 'index' },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#1a1f2e',
          borderColor: '#2a3040',
          borderWidth: 1,
          titleColor: '#e5e7eb',
          bodyColor: '#9ca3af',
          titleFont: { family: 'inherit', size: 12 },
          bodyFont: { family: 'inherit', size: 11 },
          padding: 10,
          callbacks: {
            label: (ctx) => `Price: ${ctx.parsed.y.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
          },
        },
      },
      scales: {
        x: {
          type: 'time',
          grid: { color: 'rgba(42,48,64,0.5)', drawBorder: false },
          ticks: { color: '#6b7280', font: { size: 10, family: 'inherit' }, maxTicksLimit: 8 },
        },
        y: {
          position: 'right',
          grid: { color: 'rgba(42,48,64,0.5)', drawBorder: false },
          ticks: {
            color: '#6b7280',
            font: { size: 10, family: 'inherit' },
            callback: (v) => v.toLocaleString(),
          },
        },
      },
    },
  });
}

async function loadChart(symbol, range) {
  try {
    const res = await fetch(`/api/history/${encodeURIComponent(symbol)}?range=${range}`);
    const data = await res.json();

    if (data.history && data.history.length) {
      const firstClose = data.history[0].close;
      const lastClose = data.history[data.history.length - 1].close;
      const isUp = lastClose >= firstClose;
      const color = isUp ? '#10b981' : '#ef4444';
      const bgColor = isUp ? 'rgba(16,185,129,0.08)' : 'rgba(239,68,68,0.08)';

      mainChart.data.labels = data.history.map((d) => new Date(d.time));
      mainChart.data.datasets[0].data = data.history.map((d) => d.close);
      mainChart.data.datasets[0].borderColor = color;
      mainChart.data.datasets[0].backgroundColor = bgColor;
      mainChart.data.datasets[0].label = SYMBOLS[symbol]?.name || symbol;
      mainChart.update('none');
    }

    // Update volatility metrics
    if (data.volatility) {
      document.getElementById('volATR').textContent = data.volatility.atr.toFixed(2);
      document.getElementById('volStdDev').textContent = data.volatility.stdDev.toFixed(4) + '%';
      document.getElementById('volAvgRange').textContent = data.volatility.avgRange.toFixed(2);
    }
    // Day range from current quote
    const quotes = await (await fetch('/api/quotes')).json();
    const q = quotes[symbol];
    if (q) {
      document.getElementById('volDayRange').textContent = q.dayRange.toFixed(2) + '%';
    }
  } catch (err) {
    console.error('Chart load failed:', err);
  }
}

// ===== Alerts =====
function addAlert(alert) {
  const list = document.getElementById('alertsList');
  // Remove empty state
  const empty = list.querySelector('.empty-state');
  if (empty) empty.remove();

  const el = document.createElement('div');
  el.className = `alert-item ${alert.direction}`;
  const time = new Date(alert.timestamp).toLocaleTimeString('en-US', {
    hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'America/New_York',
  });
  el.innerHTML = `
    <div class="alert-item-header">
      <span class="alert-item-symbol">${alert.name}</span>
      <span class="alert-item-time">${time} ET</span>
    </div>
    <div class="alert-item-msg">
      <span class="alert-item-pct ${alert.direction}">
        ${alert.direction === 'up' ? '▲' : '▼'} ${alert.changePct >= 0 ? '+' : ''}${alert.changePct.toFixed(2)}%
      </span>
      @ ${formatPrice(alert.price, alert.symbol)}
    </div>
    <div class="alert-item-msg" style="margin-top:3px;">${alert.message}</div>
  `;
  list.prepend(el);

  // Show banner
  showBanner(alert);

  // Play alert sound
  playAlertSound(alert.direction);

  // Keep max 20 alerts in DOM
  while (list.children.length > 20) list.lastChild.remove();
}

function showBanner(alert) {
  const banner = document.getElementById('alertBanner');
  const text = document.getElementById('alertBannerText');
  text.innerHTML = `<strong>${alert.name}</strong> ${alert.direction === 'up' ? '▲' : '▼'} ${alert.changePct >= 0 ? '+' : ''}${alert.changePct.toFixed(2)}% — ${alert.message}`;
  banner.style.display = 'flex';
  // Auto-dismiss after 15s
  setTimeout(dismissBanner, 15000);
}

function dismissBanner() {
  document.getElementById('alertBanner').style.display = 'none';
}
// Expose to global for onclick
window.dismissBanner = dismissBanner;

function playAlertSound(direction) {
  try {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.frequency.value = direction === 'up' ? 880 : 440;
    osc.type = 'sine';
    gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
    osc.start(audioCtx.currentTime);
    osc.stop(audioCtx.currentTime + 0.3);
  } catch (e) {
    // audio not available
  }
}

// ===== News Feed =====
async function fetchNews() {
  try {
    const res = await fetch('/api/news');
    const items = await res.json();
    const list = document.getElementById('newsList');

    if (!items.length) {
      list.innerHTML = '<div class="empty-state">No news available</div>';
      return;
    }

    list.innerHTML = '';
    items.forEach((item) => {
      const el = document.createElement('div');
      el.className = `news-item ${item.isGeopolitical ? 'geopolitical' : ''}`;
      const timeAgo = item.pubDate ? formatTimeAgo(new Date(item.pubDate)) : '';
      el.innerHTML = `
        <div>
          ${item.isGeopolitical ? '<span class="news-tag">Geopolitical</span>' : ''}
          <a href="${item.link}" target="_blank" rel="noopener">${item.title}</a>
        </div>
        <div class="news-source">${item.source || 'News'} ${timeAgo ? '· ' + timeAgo : ''}</div>
      `;
      list.appendChild(el);
    });
  } catch (err) {
    console.error('News fetch failed:', err);
  }
}

// ===== Helpers =====
function formatPrice(value, symbol) {
  if (value == null || isNaN(value)) return '--';
  const abs = Math.abs(value);
  // Indices: no decimals for large numbers, 2 for small
  if (abs >= 1000) return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  return value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 });
}

function formatVolume(vol) {
  if (!vol) return '--';
  if (vol >= 1e9) return (vol / 1e9).toFixed(1) + 'B';
  if (vol >= 1e6) return (vol / 1e6).toFixed(1) + 'M';
  if (vol >= 1e3) return (vol / 1e3).toFixed(1) + 'K';
  return vol.toString();
}

function formatTimeAgo(date) {
  const now = new Date();
  const diff = (now - date) / 1000;
  if (diff < 60) return 'just now';
  if (diff < 3600) return Math.floor(diff / 60) + 'm ago';
  if (diff < 86400) return Math.floor(diff / 3600) + 'h ago';
  return Math.floor(diff / 86400) + 'd ago';
}
