/* ============================================
   US Markets Live Dashboard - Application Logic
   Real-time data, charts, volatility & alerts
   ============================================ */

// ============================================
// CONFIGURATION
// ============================================
const CONFIG = {
    assets: {
        sp500:  { symbol: '^GSPC',    name: 'S&P 500',       basePrice: 5250,   dailyVol: 0.012, decimals: 2 },
        nasdaq: { symbol: '^IXIC',    name: 'Nasdaq',        basePrice: 16400,  dailyVol: 0.015, decimals: 2 },
        dow:    { symbol: '^DJI',     name: 'Dow Jones',     basePrice: 39200,  dailyVol: 0.010, decimals: 2 },
        oil:    { symbol: 'CL=F',     name: 'Crude Oil WTI', basePrice: 78.50,  dailyVol: 0.025, decimals: 2 },
        dxy:    { symbol: 'DX-Y.NYB', name: 'US Dollar Idx', basePrice: 104.20, dailyVol: 0.005, decimals: 3 },
        gold:   { symbol: 'GC=F',     name: 'Gold',          basePrice: 2340,   dailyVol: 0.012, decimals: 2 },
    },
    refreshInterval: 10000,       // 10s for simulation
    liveRefreshInterval: 30000,   // 30s for live data
    alertThreshold: 2.0,          // default 2%
    chartHistoryPoints: 120,      // data points in charts
    corsProxy: 'https://api.allorigins.win/raw?url=',
};

// ============================================
// STATE
// ============================================
const state = {
    isLive: false,
    alertSoundEnabled: true,
    alertThreshold: CONFIG.alertThreshold,
    selectedAsset: 'sp500',
    selectedTimeframe: '1D',
    currentFilter: 'all',
    data: {},       // { asset: { price, open, high, low, change, changePct, history: [{time, price}] } }
    alerts: [],
    sparkCharts: {},
    mainChart: null,
    refreshTimer: null,
    previousPrices: {},
};

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initializeData();
    setupEventListeners();
    startClock();
    updateMarketStatus();
    renderNews();
    startDataLoop();
});

function initializeData() {
    const now = Date.now();
    for (const [key, cfg] of Object.entries(CONFIG.assets)) {
        // Generate initial history (past ~2 hours of 1-min data)
        const history = [];
        let price = cfg.basePrice * (1 + (Math.random() - 0.5) * 0.02);
        const open = price;
        let high = price;
        let low = price;

        for (let i = CONFIG.chartHistoryPoints; i >= 0; i--) {
            const t = now - i * 60000;
            const change = price * cfg.dailyVol * (Math.random() - 0.5) * 0.15;
            price += change;
            if (price < cfg.basePrice * 0.8) price = cfg.basePrice * 0.8;
            high = Math.max(high, price);
            low = Math.min(low, price);
            history.push({ time: t, price: +price.toFixed(cfg.decimals) });
        }

        const currentPrice = history[history.length - 1].price;
        const changeVal = currentPrice - open;
        const changePct = (changeVal / open) * 100;

        state.data[key] = {
            price: currentPrice,
            open,
            high,
            low,
            change: changeVal,
            changePct,
            history,
            prevClose: open,
        };
        state.previousPrices[key] = currentPrice;
    }
}

// ============================================
// EVENT LISTENERS
// ============================================
function setupEventListeners() {
    // Simulation toggle
    document.getElementById('simulation-toggle').addEventListener('change', (e) => {
        state.isLive = e.target.checked;
        document.querySelector('.toggle-text').textContent = state.isLive ? 'Live Data' : 'Simulated';
        restartDataLoop();
    });

    // Alert sound toggle
    document.getElementById('alert-sound-toggle').addEventListener('click', () => {
        state.alertSoundEnabled = !state.alertSoundEnabled;
        document.getElementById('alert-sound-toggle').classList.toggle('muted', !state.alertSoundEnabled);
    });

    // Alert threshold
    document.getElementById('alert-threshold').addEventListener('change', (e) => {
        state.alertThreshold = parseFloat(e.target.value) || 2.0;
    });

    // Chart asset tabs
    document.querySelectorAll('.chart-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.chart-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            state.selectedAsset = tab.dataset.asset;
            updateMainChart();
        });
    });

    // Chart timeframe buttons
    document.querySelectorAll('.tf-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.selectedTimeframe = btn.dataset.tf;
            updateMainChart();
        });
    });

    // Market card clicks
    document.querySelectorAll('.market-card').forEach(card => {
        card.addEventListener('click', () => {
            const asset = card.id.replace('card-', '');
            document.querySelectorAll('.chart-tab').forEach(t => t.classList.remove('active'));
            const tab = document.querySelector(`.chart-tab[data-asset="${asset}"]`);
            if (tab) tab.classList.add('active');
            state.selectedAsset = asset;
            updateMainChart();
        });
    });

    // News filters
    document.querySelectorAll('.news-filter').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.news-filter').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            state.currentFilter = btn.dataset.filter;
            renderNews();
        });
    });

    // Alert banner close
    document.getElementById('alert-banner-close').addEventListener('click', () => {
        document.getElementById('alert-banner').classList.add('hidden');
    });

    // Modal close
    document.getElementById('modal-close').addEventListener('click', () => {
        document.getElementById('alert-modal').classList.add('hidden');
    });

    document.getElementById('alert-modal').addEventListener('click', (e) => {
        if (e.target === e.currentTarget) {
            e.currentTarget.classList.add('hidden');
        }
    });
}

// ============================================
// DATA LOOP
// ============================================
function startDataLoop() {
    updateAll();
    const interval = state.isLive ? CONFIG.liveRefreshInterval : CONFIG.refreshInterval;
    state.refreshTimer = setInterval(updateAll, interval);
}

function restartDataLoop() {
    if (state.refreshTimer) clearInterval(state.refreshTimer);
    startDataLoop();
}

function updateAll() {
    if (state.isLive) {
        fetchLiveData().then(() => {
            refreshUI();
        }).catch(() => {
            // Fallback to simulation if live fetch fails
            simulateTick();
            refreshUI();
        });
    } else {
        simulateTick();
        refreshUI();
    }
}

// ============================================
// SIMULATION ENGINE
// ============================================
function simulateTick() {
    const now = Date.now();

    // Occasionally inject a geopolitical shock (1% chance per tick)
    const geoShock = Math.random() < 0.01;
    let shockDirection = 0;
    let shockMagnitude = 0;
    if (geoShock) {
        shockDirection = Math.random() > 0.5 ? 1 : -1;
        shockMagnitude = 0.02 + Math.random() * 0.03; // 2-5% shock
    }

    for (const [key, cfg] of Object.entries(CONFIG.assets)) {
        const d = state.data[key];
        state.previousPrices[key] = d.price;

        // Random walk with mean reversion
        let drift = (cfg.basePrice - d.price) * 0.001; // mean reversion
        let noise = d.price * cfg.dailyVol * (Math.random() - 0.5) * 0.12;
        let shock = 0;

        if (geoShock) {
            // Oil and gold react opposite to indices during geopolitical events
            if (key === 'oil') {
                shock = d.price * shockMagnitude * -shockDirection * (0.8 + Math.random() * 0.4);
            } else if (key === 'gold') {
                shock = d.price * shockMagnitude * -shockDirection * (0.5 + Math.random() * 0.3);
            } else if (key === 'dxy') {
                shock = d.price * shockMagnitude * shockDirection * (0.3 + Math.random() * 0.2);
            } else {
                // Indices
                shock = d.price * shockMagnitude * shockDirection * (0.6 + Math.random() * 0.4);
            }
        }

        const newPrice = +(d.price + drift + noise + shock).toFixed(cfg.decimals);
        d.price = Math.max(newPrice, cfg.basePrice * 0.5); // floor
        d.high = Math.max(d.high, d.price);
        d.low = Math.min(d.low, d.price);
        d.change = d.price - d.open;
        d.changePct = (d.change / d.open) * 100;

        // Add to history
        d.history.push({ time: now, price: d.price });
        if (d.history.length > 500) d.history.shift();
    }
}

// ============================================
// LIVE DATA FETCHING
// ============================================
async function fetchLiveData() {
    const symbols = Object.values(CONFIG.assets).map(a => a.symbol);
    const url = `https://query1.finance.yahoo.com/v7/finance/quote?symbols=${symbols.join(',')}`;
    const proxyUrl = CONFIG.corsProxy + encodeURIComponent(url);

    const response = await fetch(proxyUrl);
    if (!response.ok) throw new Error('Fetch failed');
    const json = await response.json();

    if (!json.quoteResponse || !json.quoteResponse.result) throw new Error('Invalid data');

    const now = Date.now();
    const results = json.quoteResponse.result;

    for (const [key, cfg] of Object.entries(CONFIG.assets)) {
        const quote = results.find(r => r.symbol === cfg.symbol);
        if (!quote) continue;

        const d = state.data[key];
        state.previousPrices[key] = d.price;

        d.price = quote.regularMarketPrice || d.price;
        d.open = quote.regularMarketOpen || d.open;
        d.high = quote.regularMarketDayHigh || d.high;
        d.low = quote.regularMarketDayLow || d.low;
        d.change = quote.regularMarketChange || d.change;
        d.changePct = quote.regularMarketChangePercent || d.changePct;
        d.prevClose = quote.regularMarketPreviousClose || d.prevClose;

        d.history.push({ time: now, price: d.price });
        if (d.history.length > 500) d.history.shift();
    }
}

// ============================================
// UI REFRESH
// ============================================
function refreshUI() {
    updateMarketCards();
    updateSparklines();
    updateMainChart();
    updateVolatility();
    checkAlerts();
    updateLastUpdate();
}

function updateMarketCards() {
    for (const [key, cfg] of Object.entries(CONFIG.assets)) {
        const d = state.data[key];
        const card = document.getElementById(`card-${key}`);
        const isPositive = d.changePct >= 0;
        const prevPrice = state.previousPrices[key];

        // Update card class
        card.classList.remove('positive', 'negative');
        card.classList.add(isPositive ? 'positive' : 'negative');

        // Flash effect on price change
        if (prevPrice !== d.price) {
            const flashClass = d.price > prevPrice ? 'flash-green' : 'flash-red';
            card.classList.remove('flash-green', 'flash-red');
            void card.offsetWidth; // force reflow
            card.classList.add(flashClass);
            setTimeout(() => card.classList.remove(flashClass), 600);
        }

        // Update values
        document.getElementById(`price-${key}`).textContent = formatPrice(d.price, key);
        document.getElementById(`change-${key}`).textContent =
            (d.change >= 0 ? '+' : '') + d.change.toFixed(cfg.decimals);
        document.getElementById(`pct-${key}`).textContent =
            `(${d.changePct >= 0 ? '+' : ''}${d.changePct.toFixed(2)}%)`;
        document.getElementById(`high-${key}`).textContent = d.high.toFixed(cfg.decimals);
        document.getElementById(`low-${key}`).textContent = d.low.toFixed(cfg.decimals);
    }
}

function formatPrice(price, key) {
    if (key === 'oil' || key === 'dxy') return price.toFixed(2);
    if (price >= 10000) return price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return price.toFixed(2);
}

// ============================================
// SPARKLINE CHARTS
// ============================================
function updateSparklines() {
    for (const key of Object.keys(CONFIG.assets)) {
        const d = state.data[key];
        const canvas = document.getElementById(`spark-${key}`);
        const ctx = canvas.getContext('2d');
        const isPositive = d.changePct >= 0;

        // Destroy existing chart
        if (state.sparkCharts[key]) {
            state.sparkCharts[key].destroy();
        }

        const recent = d.history.slice(-60);
        const color = isPositive ? '#00c853' : '#ff1744';

        state.sparkCharts[key] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: recent.map(p => p.time),
                datasets: [{
                    data: recent.map(p => p.price),
                    borderColor: color,
                    borderWidth: 1.5,
                    fill: {
                        target: 'origin',
                        above: isPositive ? 'rgba(0,200,83,0.08)' : 'rgba(255,23,68,0.08)',
                    },
                    pointRadius: 0,
                    tension: 0.3,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, tooltip: { enabled: false } },
                scales: {
                    x: { display: false },
                    y: { display: false },
                },
                animation: { duration: 0 },
            }
        });
    }
}

// ============================================
// MAIN CHART
// ============================================
function updateMainChart() {
    const key = state.selectedAsset;
    const d = state.data[key];
    const cfg = CONFIG.assets[key];
    const canvas = document.getElementById('main-chart');
    const ctx = canvas.getContext('2d');

    if (state.mainChart) {
        state.mainChart.destroy();
    }

    // Select data range based on timeframe
    let history = d.history;
    const now = Date.now();
    switch (state.selectedTimeframe) {
        case '1D': history = d.history.filter(p => p.time > now - 24 * 3600000); break;
        case '5D': history = d.history; break; // use all available
        case '1M': history = d.history; break;
        case '3M': history = d.history; break;
    }

    if (history.length === 0) history = d.history;

    const isPositive = d.changePct >= 0;
    const mainColor = isPositive ? '#00c853' : '#ff1744';
    const fillColor = isPositive ? 'rgba(0,200,83,0.1)' : 'rgba(255,23,68,0.1)';

    // Previous close line
    const prevCloseData = history.map(() => d.open);

    state.mainChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: history.map(p => new Date(p.time)),
            datasets: [
                {
                    label: cfg.name,
                    data: history.map(p => p.price),
                    borderColor: mainColor,
                    borderWidth: 2,
                    fill: {
                        target: 1,
                        above: isPositive ? 'rgba(0,200,83,0.06)' : 'rgba(255,23,68,0.06)',
                        below: isPositive ? 'rgba(0,200,83,0.06)' : 'rgba(255,23,68,0.06)',
                    },
                    pointRadius: 0,
                    pointHitRadius: 10,
                    tension: 0.2,
                    order: 1,
                },
                {
                    label: 'Previous Close',
                    data: prevCloseData,
                    borderColor: 'rgba(255,255,255,0.15)',
                    borderWidth: 1,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false,
                    order: 2,
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1a1f2e',
                    borderColor: '#2a3042',
                    borderWidth: 1,
                    titleColor: '#e8eaed',
                    bodyColor: '#9ca3af',
                    titleFont: { family: "'SF Mono', monospace", size: 12 },
                    bodyFont: { family: "'SF Mono', monospace", size: 11 },
                    padding: 10,
                    displayColors: false,
                    callbacks: {
                        title: (items) => {
                            const date = new Date(items[0].parsed.x || items[0].label);
                            return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
                        },
                        label: (item) => {
                            if (item.datasetIndex === 1) return `Open: ${item.parsed.y.toFixed(cfg.decimals)}`;
                            return `${cfg.name}: ${item.parsed.y.toFixed(cfg.decimals)}`;
                        }
                    }
                },
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'minute',
                        displayFormats: { minute: 'HH:mm' },
                    },
                    grid: { color: 'rgba(255,255,255,0.03)', drawBorder: false },
                    ticks: { color: '#6b7280', font: { size: 10, family: "'SF Mono', monospace" }, maxTicksLimit: 10 },
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.03)', drawBorder: false },
                    ticks: {
                        color: '#6b7280',
                        font: { size: 10, family: "'SF Mono', monospace" },
                        callback: (v) => v.toFixed(cfg.decimals),
                    },
                },
            },
            animation: { duration: 300 },
        }
    });
}

// ============================================
// VOLATILITY CALCULATIONS
// ============================================
function updateVolatility() {
    const vols = {};
    let totalVol = 0;
    let maxDD = 0;

    for (const key of Object.keys(CONFIG.assets)) {
        const d = state.data[key];
        const returns = [];
        for (let i = 1; i < d.history.length; i++) {
            const ret = (d.history[i].price - d.history[i - 1].price) / d.history[i - 1].price;
            returns.push(ret);
        }

        // Standard deviation of returns
        const mean = returns.reduce((a, b) => a + b, 0) / (returns.length || 1);
        const variance = returns.reduce((a, b) => a + (b - mean) ** 2, 0) / (returns.length || 1);
        const stdDev = Math.sqrt(variance);

        // Annualize (assuming 1-min data, ~390 min/day, ~252 days/year)
        const annualized = stdDev * Math.sqrt(390 * 252) * 100;
        vols[key] = annualized;
        totalVol += annualized;

        // Max drawdown
        let peak = d.history[0]?.price || d.price;
        for (const point of d.history) {
            if (point.price > peak) peak = point.price;
            const dd = (peak - point.price) / peak * 100;
            if (dd > maxDD) maxDD = dd;
        }

        // Update UI
        const volEl = document.getElementById(`vol-${key}`);
        const barEl = document.getElementById(`vol-bar-${key}`);
        if (volEl) volEl.textContent = annualized.toFixed(1) + '%';
        if (barEl) barEl.style.width = Math.min(annualized / 60 * 100, 100) + '%';
    }

    // Summary metrics
    const avgVol = totalVol / Object.keys(CONFIG.assets).length;
    document.getElementById('avg-vol').textContent = avgVol.toFixed(1) + '%';
    document.getElementById('max-drawdown').textContent = maxDD.toFixed(2) + '%';

    // Correlation between oil and gold
    const oilReturns = getReturns('oil');
    const goldReturns = getReturns('gold');
    const corr = calculateCorrelation(oilReturns, goldReturns);
    document.getElementById('correlation').textContent = corr.toFixed(3);
}

function getReturns(key) {
    const d = state.data[key];
    const returns = [];
    for (let i = 1; i < d.history.length; i++) {
        returns.push((d.history[i].price - d.history[i - 1].price) / d.history[i - 1].price);
    }
    return returns;
}

function calculateCorrelation(x, y) {
    const n = Math.min(x.length, y.length);
    if (n < 2) return 0;

    const mx = x.slice(0, n).reduce((a, b) => a + b, 0) / n;
    const my = y.slice(0, n).reduce((a, b) => a + b, 0) / n;

    let num = 0, dx = 0, dy = 0;
    for (let i = 0; i < n; i++) {
        const xi = x[i] - mx;
        const yi = y[i] - my;
        num += xi * yi;
        dx += xi * xi;
        dy += yi * yi;
    }

    const denom = Math.sqrt(dx * dy);
    return denom === 0 ? 0 : num / denom;
}

// ============================================
// ALERT SYSTEM
// ============================================
function checkAlerts() {
    for (const [key, cfg] of Object.entries(CONFIG.assets)) {
        const d = state.data[key];
        const absPct = Math.abs(d.changePct);

        if (absPct >= state.alertThreshold) {
            // Check if we already alerted for this level
            const existing = state.alerts.find(
                a => a.asset === key && Math.abs(a.pct - d.changePct) < 0.5
            );
            if (existing) continue;

            const alert = {
                id: Date.now() + '-' + key,
                asset: key,
                name: cfg.name,
                price: d.price,
                change: d.change,
                pct: d.changePct,
                time: new Date(),
                direction: d.changePct >= 0 ? 'up' : 'down',
            };

            state.alerts.unshift(alert);
            renderAlerts();
            showAlertBanner(alert);
            showAlertModal(alert);

            if (state.alertSoundEnabled) {
                playAlertSound();
            }
        }
    }
}

function renderAlerts() {
    const container = document.getElementById('alerts-list');
    const count = document.getElementById('alert-count');
    count.textContent = state.alerts.length;

    if (state.alerts.length === 0) {
        container.innerHTML = '<div class="alert-empty">No alerts triggered yet. Monitoring for significant moves...</div>';
        return;
    }

    container.innerHTML = state.alerts.map(a => `
        <div class="alert-item alert-${a.direction}">
            <span class="alert-icon">${a.direction === 'up' ? '\u25B2' : '\u25BC'}</span>
            <div class="alert-content">
                <div class="alert-title">${a.name} ${a.direction === 'up' ? 'surged' : 'dropped'} ${Math.abs(a.pct).toFixed(2)}%</div>
                <div class="alert-detail">${formatPrice(a.price, a.asset)} (${a.change >= 0 ? '+' : ''}${a.change.toFixed(2)})</div>
            </div>
            <span class="alert-time">${a.time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</span>
        </div>
    `).join('');
}

function showAlertBanner(alert) {
    const banner = document.getElementById('alert-banner');
    const text = document.getElementById('alert-banner-text');
    text.textContent = `ALERT: ${alert.name} ${alert.direction === 'up' ? 'UP' : 'DOWN'} ${Math.abs(alert.pct).toFixed(2)}% \u2014 Now at ${formatPrice(alert.price, alert.asset)} \u2014 Monitor Iran-Hormuz developments`;
    banner.classList.remove('hidden');
}

function showAlertModal(alert) {
    const modal = document.getElementById('alert-modal');
    const body = document.getElementById('modal-body');

    body.innerHTML = `
        <div class="modal-asset">${alert.name}</div>
        <div class="modal-move ${alert.direction}">
            ${alert.direction === 'up' ? '\u25B2' : '\u25BC'} ${Math.abs(alert.pct).toFixed(2)}%
        </div>
        <p>Current price: <strong>${formatPrice(alert.price, alert.asset)}</strong></p>
        <p>Change: <strong>${alert.change >= 0 ? '+' : ''}${alert.change.toFixed(2)}</strong></p>
        <p>Time: <strong>${alert.time.toLocaleTimeString()}</strong></p>
        <hr style="border-color: #2a3042; margin: 12px 0;">
        <p style="color: var(--orange); font-weight: 600;">
            Geopolitical Context: Monitor Strait of Hormuz shipping activity and US-Iran ceasefire negotiations. Large market moves may correlate with developments in this region.
        </p>
    `;
    modal.classList.remove('hidden');
}

function playAlertSound() {
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(880, audioCtx.currentTime);
        oscillator.frequency.setValueAtTime(660, audioCtx.currentTime + 0.1);
        oscillator.frequency.setValueAtTime(880, audioCtx.currentTime + 0.2);
        gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
        oscillator.start(audioCtx.currentTime);
        oscillator.stop(audioCtx.currentTime + 0.4);
    } catch (e) {
        // Audio not supported
    }
}

// ============================================
// NEWS FEED
// ============================================
const NEWS_DATA = [
    {
        title: 'US and Iran signal willingness to resume nuclear talks amid ceasefire pressure',
        time: randomPastTime(15),
        tags: ['ceasefire', 'sanctions'],
        severity: 'high',
        categories: ['ceasefire', 'sanctions'],
    },
    {
        title: 'Oil tanker traffic through Strait of Hormuz returns to normal levels after brief disruption',
        time: randomPastTime(32),
        tags: ['hormuz', 'oil'],
        severity: 'high',
        categories: ['hormuz', 'oil'],
    },
    {
        title: 'Pentagon confirms increased naval presence near Hormuz following Iranian military exercises',
        time: randomPastTime(48),
        tags: ['hormuz', 'military'],
        severity: 'high',
        categories: ['hormuz'],
    },
    {
        title: 'Brent crude rises 3% on reports of Iranian drone activity near shipping lanes',
        time: randomPastTime(65),
        tags: ['oil', 'hormuz'],
        severity: 'medium',
        categories: ['oil', 'hormuz'],
    },
    {
        title: 'European mediators propose new ceasefire framework for US-Iran tensions',
        time: randomPastTime(90),
        tags: ['ceasefire'],
        severity: 'medium',
        categories: ['ceasefire'],
    },
    {
        title: 'Treasury Department expands sanctions list targeting Iranian oil exports',
        time: randomPastTime(120),
        tags: ['sanctions', 'oil'],
        severity: 'medium',
        categories: ['sanctions', 'oil'],
    },
    {
        title: 'Gold hits session high as safe-haven demand rises on Middle East uncertainty',
        time: randomPastTime(140),
        tags: ['oil'],
        severity: 'medium',
        categories: ['oil'],
    },
    {
        title: 'Iranian foreign minister: "Ceasefire conditions must include sanctions relief"',
        time: randomPastTime(180),
        tags: ['ceasefire', 'sanctions'],
        severity: 'high',
        categories: ['ceasefire', 'sanctions'],
    },
    {
        title: 'Shipping insurance premiums spike for vessels transiting Strait of Hormuz',
        time: randomPastTime(210),
        tags: ['hormuz', 'oil'],
        severity: 'medium',
        categories: ['hormuz', 'oil'],
    },
    {
        title: 'OPEC+ emergency meeting called to discuss potential Hormuz supply disruptions',
        time: randomPastTime(240),
        tags: ['oil', 'hormuz'],
        severity: 'high',
        categories: ['oil', 'hormuz'],
    },
    {
        title: 'US Dollar strengthens as investors seek safety amid escalating tensions',
        time: randomPastTime(280),
        tags: ['sanctions'],
        severity: 'low',
        categories: ['sanctions'],
    },
    {
        title: 'Iran IRGC Navy conducts live-fire exercises in Persian Gulf region',
        time: randomPastTime(320),
        tags: ['hormuz', 'military'],
        severity: 'high',
        categories: ['hormuz'],
    },
    {
        title: 'Analysts: Ceasefire could trigger 10% drop in oil prices within weeks',
        time: randomPastTime(360),
        tags: ['ceasefire', 'oil'],
        severity: 'medium',
        categories: ['ceasefire', 'oil'],
    },
    {
        title: 'Qatar and Oman mediating back-channel US-Iran de-escalation talks',
        time: randomPastTime(400),
        tags: ['ceasefire'],
        severity: 'medium',
        categories: ['ceasefire'],
    },
    {
        title: 'S&P 500 futures drop as satellite imagery shows Iranian fast-boat movements near Hormuz',
        time: randomPastTime(450),
        tags: ['hormuz', 'military'],
        severity: 'high',
        categories: ['hormuz'],
    },
];

function randomPastTime(minutesAgo) {
    return new Date(Date.now() - minutesAgo * 60000);
}

function renderNews() {
    const container = document.getElementById('news-list');
    let items = NEWS_DATA;

    if (state.currentFilter !== 'all') {
        items = items.filter(n => n.categories.includes(state.currentFilter));
    }

    items.sort((a, b) => b.time - a.time);

    if (items.length === 0) {
        container.innerHTML = '<div class="news-loading">No news matching this filter.</div>';
        return;
    }

    container.innerHTML = items.map(n => `
        <div class="news-item severity-${n.severity}">
            <div class="news-header">
                <span class="news-title">${n.title}</span>
                <span class="news-time">${formatNewsTime(n.time)}</span>
            </div>
            <div class="news-tags">
                ${n.tags.map(t => `<span class="news-tag ${t}">${t}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

function formatNewsTime(date) {
    const diff = Math.round((Date.now() - date.getTime()) / 60000);
    if (diff < 1) return 'Just now';
    if (diff < 60) return `${diff}m ago`;
    if (diff < 1440) return `${Math.floor(diff / 60)}h ago`;
    return date.toLocaleDateString();
}

// ============================================
// CLOCK & MARKET STATUS
// ============================================
function startClock() {
    updateClock();
    setInterval(updateClock, 1000);
    setInterval(updateMarketStatus, 60000);
}

function updateClock() {
    const now = new Date();
    const etOptions = { timeZone: 'America/New_York', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
    const etTime = now.toLocaleTimeString('en-US', etOptions);
    const etDate = now.toLocaleDateString('en-US', { timeZone: 'America/New_York', weekday: 'short', month: 'short', day: 'numeric' });
    document.getElementById('clock').textContent = `${etDate} ${etTime} ET`;
}

function updateMarketStatus() {
    const now = new Date();
    const et = new Date(now.toLocaleString('en-US', { timeZone: 'America/New_York' }));
    const hours = et.getHours();
    const minutes = et.getMinutes();
    const day = et.getDay();
    const timeInMin = hours * 60 + minutes;

    const statusEl = document.getElementById('market-status');
    const textEl = document.getElementById('market-status-text');

    statusEl.classList.remove('open', 'closed', 'pre', 'post');

    if (day === 0 || day === 6) {
        statusEl.classList.add('closed');
        textEl.textContent = 'Market Closed (Weekend)';
    } else if (timeInMin >= 570 && timeInMin < 960) {
        // 9:30 AM - 4:00 PM ET
        statusEl.classList.add('open');
        textEl.textContent = 'Market Open';
    } else if (timeInMin >= 240 && timeInMin < 570) {
        // 4:00 AM - 9:30 AM ET
        statusEl.classList.add('pre');
        textEl.textContent = 'Pre-Market';
    } else if (timeInMin >= 960 && timeInMin < 1200) {
        // 4:00 PM - 8:00 PM ET
        statusEl.classList.add('post');
        textEl.textContent = 'After Hours';
    } else {
        statusEl.classList.add('closed');
        textEl.textContent = 'Market Closed';
    }
}

function updateLastUpdate() {
    const now = new Date();
    document.getElementById('last-update').textContent =
        'Last update: ' + now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}
