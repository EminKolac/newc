/* ========================================================================
   Geopolitical Market Dashboard — Application Logic
   ======================================================================== */

// ---------------------------------------------------------------------------
// 1. Configuration & State
// ---------------------------------------------------------------------------
const INSTRUMENTS = [
    { id: 'sp500',  label: 'S&P 500',         symbol: '^GSPC',    basePrice: 5450,   color: '#3b82f6', decimals: 2 },
    { id: 'nasdaq', label: 'Nasdaq',           symbol: '^IXIC',    basePrice: 17150,  color: '#8b5cf6', decimals: 2 },
    { id: 'dow',    label: 'Dow Jones',        symbol: '^DJI',     basePrice: 40200,  color: '#10b981', decimals: 2 },
    { id: 'oil',    label: 'WTI Crude Oil',    symbol: 'CL=F',     basePrice: 72.50,  color: '#f97316', decimals: 2 },
    { id: 'gold',   label: 'Gold',             symbol: 'GC=F',     basePrice: 2380,   color: '#f59e0b', decimals: 2 },
    { id: 'dxy',    label: 'US Dollar Index',  symbol: 'DX-Y.NYB', basePrice: 104.25, color: '#06b6d4', decimals: 3 },
];

const state = {
    settings: {
        refreshInterval: 30,
        alertThreshold: 2.0,
        chartTimeframe: '5d',
        soundAlerts: true,
        dataSource: 'demo',
    },
    charts: {},
    priceHistory: {},
    currentPrices: {},
    openPrices: {},
    previousClose: {},
    alerts: [],
    refreshTimer: null,
};

// ---------------------------------------------------------------------------
// 2. Initialization
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    buildSummaryCards();
    initCharts();
    initEventListeners();
    initNewsFromSeed();
    startDataLoop();
});

function loadSettings() {
    const saved = localStorage.getItem('dashSettings');
    if (saved) {
        Object.assign(state.settings, JSON.parse(saved));
    }
    document.getElementById('refreshInterval').value = state.settings.refreshInterval;
    document.getElementById('alertThreshold').value = state.settings.alertThreshold;
    document.getElementById('chartTimeframe').value = state.settings.chartTimeframe;
    document.getElementById('soundAlerts').checked = state.settings.soundAlerts;
    document.getElementById('dataSource').value = state.settings.dataSource;
}

function saveSettings() {
    state.settings.refreshInterval = parseInt(document.getElementById('refreshInterval').value, 10);
    state.settings.alertThreshold = parseFloat(document.getElementById('alertThreshold').value);
    state.settings.chartTimeframe = document.getElementById('chartTimeframe').value;
    state.settings.soundAlerts = document.getElementById('soundAlerts').checked;
    state.settings.dataSource = document.getElementById('dataSource').value;
    localStorage.setItem('dashSettings', JSON.stringify(state.settings));
    restartDataLoop();
}

// ---------------------------------------------------------------------------
// 3. UI Event Listeners
// ---------------------------------------------------------------------------
function initEventListeners() {
    document.getElementById('btnSettings').addEventListener('click', () => {
        document.getElementById('settingsModal').classList.remove('hidden');
    });
    document.getElementById('modalClose').addEventListener('click', () => {
        document.getElementById('settingsModal').classList.add('hidden');
    });
    document.getElementById('btnSaveSettings').addEventListener('click', () => {
        saveSettings();
        document.getElementById('settingsModal').classList.add('hidden');
    });
    document.getElementById('alertDismiss').addEventListener('click', () => {
        document.getElementById('alertBanner').classList.add('hidden');
    });
    document.getElementById('btnClearAlerts').addEventListener('click', () => {
        state.alerts = [];
        document.getElementById('alertLog').innerHTML = '';
    });
}

// ---------------------------------------------------------------------------
// 4. Summary Cards
// ---------------------------------------------------------------------------
function buildSummaryCards() {
    const container = document.getElementById('summaryCards');
    container.innerHTML = INSTRUMENTS.map(inst => `
        <div class="summary-card" id="card-${inst.id}" data-id="${inst.id}">
            <div class="card-label">${inst.label}</div>
            <div class="card-price" id="cardprice-${inst.id}">—</div>
            <div class="card-change" id="cardchange-${inst.id}">—</div>
        </div>
    `).join('');
}

function updateSummaryCard(inst, price, prevClose) {
    const change = price - prevClose;
    const changePct = (change / prevClose) * 100;
    const el = document.getElementById(`cardprice-${inst.id}`);
    const cel = document.getElementById(`cardchange-${inst.id}`);
    if (el) el.textContent = formatPrice(price, inst.decimals);
    if (cel) {
        const sign = change >= 0 ? '+' : '';
        cel.textContent = `${sign}${change.toFixed(2)} (${sign}${changePct.toFixed(2)}%)`;
        cel.className = `card-change ${change >= 0 ? 'positive' : 'negative'}`;
    }

    const card = document.getElementById(`card-${inst.id}`);
    if (Math.abs(changePct) >= state.settings.alertThreshold) {
        card.classList.add('alert-active');
    } else {
        card.classList.remove('alert-active');
    }
}

// ---------------------------------------------------------------------------
// 5. Charts (Chart.js)
// ---------------------------------------------------------------------------
function initCharts() {
    INSTRUMENTS.forEach(inst => {
        const ctx = document.getElementById(`chart-${inst.id}`).getContext('2d');
        state.charts[inst.id] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    borderColor: inst.color,
                    backgroundColor: hexToRgba(inst.color, 0.08),
                    borderWidth: 1.5,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0,
                    pointHitRadius: 8,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 400 },
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1a2235',
                        borderColor: '#2a3550',
                        borderWidth: 1,
                        titleFont: { family: 'SF Mono, Consolas, monospace', size: 11 },
                        bodyFont: { family: 'SF Mono, Consolas, monospace', size: 12 },
                        padding: 10,
                        callbacks: {
                            label: (ctx) => `${inst.label}: ${formatPrice(ctx.parsed.y, inst.decimals)}`,
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        grid: { color: 'rgba(42,53,80,0.3)', drawBorder: false },
                        ticks: { color: '#6b7280', font: { size: 10, family: 'SF Mono, Consolas, monospace' }, maxTicksLimit: 8 },
                    },
                    y: {
                        display: true,
                        position: 'right',
                        grid: { color: 'rgba(42,53,80,0.3)', drawBorder: false },
                        ticks: {
                            color: '#6b7280',
                            font: { size: 10, family: 'SF Mono, Consolas, monospace' },
                            callback: (val) => formatPrice(val, inst.decimals),
                        },
                    }
                },
            }
        });
        state.priceHistory[inst.id] = [];
    });
}

function updateChart(inst, history) {
    const chart = state.charts[inst.id];
    if (!chart) return;

    chart.data.labels = history.map(p => p.label);
    chart.data.datasets[0].data = history.map(p => p.value);

    // Color line red/green based on overall trend
    const first = history[0]?.value ?? 0;
    const last = history[history.length - 1]?.value ?? 0;
    const trending = last >= first;
    chart.data.datasets[0].borderColor = trending ? '#10b981' : '#ef4444';
    chart.data.datasets[0].backgroundColor = trending
        ? 'rgba(16,185,129,0.08)' : 'rgba(239,68,68,0.08)';

    chart.update('none');
}

function updateChartPrice(inst, price, prevClose) {
    const el = document.getElementById(`price-${inst.id}`);
    if (!el) return;
    const change = price - prevClose;
    const changePct = (change / prevClose) * 100;
    const sign = change >= 0 ? '+' : '';
    el.innerHTML = `
        ${formatPrice(price, inst.decimals)}
        <span class="change ${change >= 0 ? 'positive' : 'negative'}">
            ${sign}${changePct.toFixed(2)}%
        </span>
    `;
}

// ---------------------------------------------------------------------------
// 6. Volatility Metrics
// ---------------------------------------------------------------------------
function computeVolatility(history) {
    if (history.length < 2) {
        return { stdDev: 0, atr14: 0, intradayRange: 0, intradayRangePct: 0 };
    }

    const prices = history.map(p => p.value);
    const returns = [];
    for (let i = 1; i < prices.length; i++) {
        returns.push((prices[i] - prices[i - 1]) / prices[i - 1]);
    }

    // Standard deviation of returns
    const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
    const variance = returns.reduce((a, r) => a + (r - mean) ** 2, 0) / returns.length;
    const stdDev = Math.sqrt(variance) * 100; // as percentage

    // Intraday range (High - Low of last ~session)
    const recentPrices = prices.slice(-78); // ~1 trading day at 5-min intervals
    const high = Math.max(...recentPrices);
    const low = Math.min(...recentPrices);
    const intradayRange = high - low;
    const midpoint = (high + low) / 2;
    const intradayRangePct = midpoint > 0 ? (intradayRange / midpoint) * 100 : 0;

    // ATR approximation (using 14-period ranges)
    const periodSize = Math.max(1, Math.floor(prices.length / 14));
    let trSum = 0;
    let trCount = 0;
    for (let i = periodSize; i < prices.length; i += periodSize) {
        const slice = prices.slice(i - periodSize, i);
        const h = Math.max(...slice);
        const l = Math.min(...slice);
        trSum += h - l;
        trCount++;
    }
    const atr14 = trCount > 0 ? trSum / trCount : 0;

    return { stdDev, atr14, intradayRange, intradayRangePct };
}

function updateVolatilityDisplay(inst, vol) {
    const container = document.getElementById(`vol-${inst.id}`);
    if (!container) return;

    const rangeClass = vol.intradayRangePct > 2 ? 'high' : vol.intradayRangePct > 1 ? 'medium' : 'low';
    const volClass = vol.stdDev > 1.5 ? 'high' : vol.stdDev > 0.8 ? 'medium' : 'low';

    container.innerHTML = `
        <div class="vol-item">
            <span class="vol-label">Range</span>
            <span class="vol-value ${rangeClass}">${vol.intradayRangePct.toFixed(2)}%</span>
        </div>
        <div class="vol-item">
            <span class="vol-label">5D Vol</span>
            <span class="vol-value ${volClass}">${vol.stdDev.toFixed(3)}%</span>
        </div>
        <div class="vol-item">
            <span class="vol-label">ATR(14)</span>
            <span class="vol-value">${vol.atr14.toFixed(2)}</span>
        </div>
    `;
}

function updateVolTable() {
    const tbody = document.getElementById('volTableBody');
    tbody.innerHTML = INSTRUMENTS.map(inst => {
        const price = state.currentPrices[inst.id] ?? inst.basePrice;
        const prevClose = state.previousClose[inst.id] ?? inst.basePrice;
        const change = price - prevClose;
        const changePct = (change / prevClose) * 100;
        const history = state.priceHistory[inst.id] || [];
        const vol = computeVolatility(history);
        const sign = change >= 0 ? '+' : '';
        const cls = change >= 0 ? 'positive' : 'negative';

        let statusLabel = 'Normal';
        let statusClass = 'normal';
        if (Math.abs(changePct) >= state.settings.alertThreshold) {
            statusLabel = 'ALERT';
            statusClass = 'high';
        } else if (Math.abs(changePct) >= state.settings.alertThreshold * 0.5 || vol.stdDev > 1.0) {
            statusLabel = 'Elevated';
            statusClass = 'elevated';
        }

        return `<tr>
            <td>${inst.label}</td>
            <td>${formatPrice(price, inst.decimals)}</td>
            <td class="${cls}">${sign}${changePct.toFixed(2)}%</td>
            <td>${vol.intradayRangePct.toFixed(2)}%</td>
            <td>${vol.stdDev.toFixed(3)}%</td>
            <td>${vol.atr14.toFixed(2)}</td>
            <td><span class="status-badge ${statusClass}">${statusLabel}</span></td>
        </tr>`;
    }).join('');
}

// ---------------------------------------------------------------------------
// 7. Alert System
// ---------------------------------------------------------------------------
function checkAlerts(inst, price, prevClose) {
    const changePct = ((price - prevClose) / prevClose) * 100;
    const threshold = state.settings.alertThreshold;

    if (Math.abs(changePct) >= threshold) {
        const existing = state.alerts.find(a => a.instId === inst.id && a.type === 'threshold'
            && (Date.now() - a.timestamp < 60000));
        if (existing) return; // Don't spam

        const direction = changePct > 0 ? 'surged' : 'plunged';
        const geoContext = getGeopoliticalContext(inst.id, changePct);

        const alert = {
            id: Date.now(),
            instId: inst.id,
            type: 'threshold',
            level: Math.abs(changePct) >= threshold * 1.5 ? 'critical' : 'warning',
            message: `${inst.label} ${direction} ${Math.abs(changePct).toFixed(2)}% — now at ${formatPrice(price, inst.decimals)}. ${geoContext}`,
            timestamp: Date.now(),
        };

        state.alerts.unshift(alert);
        renderAlertLog();
        showBannerAlert(alert.message);
        flashChartPanel(inst.id);

        if (state.settings.soundAlerts) {
            playAlertSound();
        }
    }
}

function getGeopoliticalContext(instId, changePct) {
    const contexts = {
        oil: changePct > 0
            ? 'Potential Strait of Hormuz disruption risk — monitor tanker traffic and Iran naval activity.'
            : 'Possible ceasefire progress easing supply concerns — watch for official US-Iran statements.',
        gold: changePct > 0
            ? 'Safe-haven demand rising amid US-Iran tensions — geopolitical risk premium increasing.'
            : 'Risk appetite improving — possible diplomatic breakthrough signaling de-escalation.',
        sp500: changePct > 0
            ? 'Market rally may reflect ceasefire optimism — confirm with oil/gold cross-asset signals.'
            : 'Equity sell-off amid escalation fears — check defense sector and energy correlations.',
        nasdaq: changePct > 0
            ? 'Tech recovery suggesting risk-on sentiment — verify against VIX and bond yields.'
            : 'Growth stocks under pressure from geopolitical uncertainty — monitor safe-haven flows.',
        dow: changePct > 0
            ? 'Blue-chips advancing on potential de-escalation — industrials and energy leading.'
            : 'Dow decline signals broad risk-off — Strait of Hormuz shipping disruption fears.',
        dxy: changePct > 0
            ? 'Dollar strengthening as safe-haven — flight to USD amid Middle East tensions.'
            : 'Dollar weakening may signal risk normalization — potential ceasefire tailwind.',
    };
    return contexts[instId] || '';
}

function showBannerAlert(message) {
    const banner = document.getElementById('alertBanner');
    document.getElementById('alertText').textContent = message;
    banner.classList.remove('hidden');
    setTimeout(() => banner.classList.add('hidden'), 15000);
}

function flashChartPanel(instId) {
    const panel = document.getElementById(`panel-${instId}`);
    if (panel) {
        panel.classList.add('alert-flash');
        setTimeout(() => panel.classList.remove('alert-flash'), 3000);
    }
}

function renderAlertLog() {
    const log = document.getElementById('alertLog');
    log.innerHTML = state.alerts.slice(0, 50).map(a => `
        <div class="alert-log-item ${a.level}">
            <div class="alert-log-time">${new Date(a.timestamp).toLocaleTimeString()}</div>
            <div class="alert-log-msg">${a.message}</div>
        </div>
    `).join('');
}

function playAlertSound() {
    try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        oscillator.connect(gain);
        gain.connect(audioCtx.destination);
        oscillator.frequency.value = 880;
        oscillator.type = 'sine';
        gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
        oscillator.start(audioCtx.currentTime);
        oscillator.stop(audioCtx.currentTime + 0.5);
    } catch (_) { /* silent fail if audio not available */ }
}

// ---------------------------------------------------------------------------
// 8. News Feed (US-Iran / Strait of Hormuz)
// ---------------------------------------------------------------------------
const NEWS_SEED = [
    {
        time: minutesAgo(3),
        headline: 'Pentagon confirms increased US naval presence near Strait of Hormuz as tensions simmer',
        source: 'Reuters',
        tags: ['hormuz'],
    },
    {
        time: minutesAgo(12),
        headline: 'Iran signals willingness to resume nuclear talks — State Dept. cautiously optimistic',
        source: 'AP News',
        tags: ['iran', 'ceasefire'],
    },
    {
        time: minutesAgo(28),
        headline: 'Oil tanker traffic through Strait of Hormuz drops 8% week-over-week amid security concerns',
        source: 'Bloomberg',
        tags: ['hormuz', 'oil'],
    },
    {
        time: minutesAgo(45),
        headline: 'IRGC conducts naval drills near Hormuz — US 5th Fleet monitoring closely',
        source: 'Al Jazeera',
        tags: ['iran', 'hormuz'],
    },
    {
        time: minutesAgo(67),
        headline: 'EU mediators propose new framework for US-Iran ceasefire in Gulf shipping lanes',
        source: 'Financial Times',
        tags: ['ceasefire', 'hormuz'],
    },
    {
        time: minutesAgo(90),
        headline: 'Brent crude surges as Houthi-linked group threatens Red Sea and Gulf shipping routes',
        source: 'CNBC',
        tags: ['oil', 'hormuz'],
    },
    {
        time: minutesAgo(120),
        headline: 'US Treasury expands Iran-related sanctions targeting oil export intermediaries',
        source: 'Wall Street Journal',
        tags: ['iran', 'sanctions', 'oil'],
    },
    {
        time: minutesAgo(155),
        headline: 'Gold hits session highs as Middle East de-escalation hopes fade after failed talks',
        source: 'MarketWatch',
        tags: ['iran'],
    },
    {
        time: minutesAgo(190),
        headline: 'Saudi Arabia and UAE call for diplomatic resolution to Hormuz strait tensions',
        source: 'Reuters',
        tags: ['hormuz', 'ceasefire'],
    },
    {
        time: minutesAgo(240),
        headline: 'Iran foreign minister: "Ceasefire achievable if sanctions eased" — full statement expected today',
        source: 'BBC News',
        tags: ['iran', 'ceasefire'],
    },
];

const LIVE_NEWS_POOL = [
    { headline: 'BREAKING: Iran and US agree to indirect talks on Gulf maritime security — Oman mediating', tags: ['iran', 'ceasefire', 'hormuz'], source: 'Reuters' },
    { headline: 'US carrier strike group repositions near Persian Gulf — Pentagon says "routine movement"', tags: ['hormuz'], source: 'CNN' },
    { headline: 'Iran oil exports reach 6-month high despite sanctions — tanker tracking data shows', tags: ['iran', 'oil', 'sanctions'], source: 'Bloomberg' },
    { headline: 'Strait of Hormuz insurance premiums rise 15% as underwriters reassess risk', tags: ['hormuz', 'oil'], source: 'Lloyd\'s List' },
    { headline: 'White House: "Ceasefire framework with Iran progressing" — energy markets react', tags: ['ceasefire', 'iran', 'oil'], source: 'AP News' },
    { headline: 'IRGC seizes foreign-flagged tanker near Hormuz — crew nationality unconfirmed', tags: ['iran', 'hormuz', 'oil'], source: 'Al Jazeera' },
    { headline: 'Gold rallies as traders hedge against potential Hormuz closure scenario', tags: ['hormuz'], source: 'MarketWatch' },
    { headline: 'US and Iran exchange prisoner swap proposals as goodwill measure ahead of ceasefire talks', tags: ['iran', 'ceasefire'], source: 'NYT' },
    { headline: 'Oil volatility index (OVX) spikes to 3-month high on Hormuz disruption fears', tags: ['oil', 'hormuz'], source: 'CBOE' },
    { headline: 'European allies push back on new Iran sanctions — fear oil supply disruption', tags: ['sanctions', 'iran', 'oil'], source: 'Financial Times' },
    { headline: 'Japan and South Korea secure alternative crude supply routes bypassing Hormuz', tags: ['hormuz', 'oil'], source: 'Nikkei Asia' },
    { headline: 'Iranian drone spotted near US destroyer in Persian Gulf — no hostile action taken', tags: ['iran', 'hormuz'], source: 'Stars and Stripes' },
];

function minutesAgo(m) {
    return new Date(Date.now() - m * 60000);
}

function initNewsFromSeed() {
    const feed = document.getElementById('newsFeed');
    feed.innerHTML = NEWS_SEED.map(n => renderNewsItem(n)).join('');
}

function addLiveNewsItem() {
    const pool = LIVE_NEWS_POOL;
    const item = pool[Math.floor(Math.random() * pool.length)];
    const newsItem = { ...item, time: new Date() };
    const feed = document.getElementById('newsFeed');
    feed.insertAdjacentHTML('afterbegin', renderNewsItem(newsItem));
    // Keep max 20
    while (feed.children.length > 20) {
        feed.removeChild(feed.lastChild);
    }
}

function renderNewsItem(n) {
    const timeStr = n.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const tags = (n.tags || []).map(t => `<span class="news-tag ${t}">${t}</span>`).join('');
    return `
        <div class="news-item">
            <div class="news-time">${timeStr}</div>
            <div class="news-headline">${tags} ${escapeHtml(n.headline)}</div>
            <div class="news-source">${escapeHtml(n.source)}</div>
        </div>
    `;
}

// ---------------------------------------------------------------------------
// 9. Data Fetching — Live & Demo
// ---------------------------------------------------------------------------
async function fetchAllData() {
    if (state.settings.dataSource === 'live') {
        await fetchLiveData();
    } else {
        fetchDemoData();
    }
}

// --- Live: Yahoo Finance via allorigins CORS proxy ---
async function fetchLiveData() {
    const proxy = 'https://api.allorigins.win/raw?url=';
    const results = await Promise.allSettled(
        INSTRUMENTS.map(async (inst) => {
            const tf = state.settings.chartTimeframe;
            const interval = tf === '1d' ? '5m' : tf === '5d' ? '15m' : '1d';
            const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(inst.symbol)}?range=${tf}&interval=${interval}`;
            const resp = await fetch(proxy + encodeURIComponent(url));
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            return { inst, data: await resp.json() };
        })
    );

    let anySuccess = false;
    for (const result of results) {
        if (result.status === 'fulfilled') {
            const { inst, data } = result.value;
            try {
                const chart = data.chart.result[0];
                const timestamps = chart.timestamp || [];
                const closes = chart.indicators.quote[0].close || [];
                const meta = chart.meta;

                const history = timestamps.map((ts, i) => ({
                    label: formatTimestamp(ts * 1000, state.settings.chartTimeframe),
                    value: closes[i],
                    timestamp: ts * 1000,
                })).filter(p => p.value != null);

                state.priceHistory[inst.id] = history;
                const lastPrice = history[history.length - 1]?.value ?? meta.regularMarketPrice;
                const prevClose = meta.chartPreviousClose ?? meta.previousClose ?? inst.basePrice;
                state.currentPrices[inst.id] = lastPrice;
                state.previousClose[inst.id] = prevClose;
                anySuccess = true;
            } catch (_) { /* skip this instrument */ }
        }
    }

    if (!anySuccess) {
        setConnectionStatus('error', 'API Error — falling back to demo');
        fetchDemoData();
        return;
    }

    setConnectionStatus('connected', 'Live');
    refreshUI();
}

// --- Demo: Realistic simulated market data ---
function fetchDemoData() {
    const now = Date.now();
    INSTRUMENTS.forEach(inst => {
        const existing = state.priceHistory[inst.id] || [];

        if (existing.length === 0) {
            // Generate initial history
            const points = 200;
            const history = [];
            let price = inst.basePrice;
            const volatilityMap = {
                sp500: 0.003, nasdaq: 0.004, dow: 0.0025,
                oil: 0.008, gold: 0.004, dxy: 0.002,
            };
            const vol = volatilityMap[inst.id] || 0.003;

            // Add a geopolitical shock somewhere in the series
            const shockPoint = Math.floor(points * 0.7 + Math.random() * points * 0.2);
            const shockMagnitude = inst.id === 'oil' ? 0.04 : inst.id === 'gold' ? 0.025 : -0.02;

            for (let i = 0; i < points; i++) {
                const drift = (Math.random() - 0.502) * vol;
                const shock = i === shockPoint ? shockMagnitude * (inst.id === 'dxy' ? -1 : 1) : 0;
                price *= (1 + drift + shock);
                const ts = now - (points - i) * 300000; // 5-min intervals
                history.push({
                    label: formatTimestamp(ts, state.settings.chartTimeframe),
                    value: price,
                    timestamp: ts,
                });
            }

            state.priceHistory[inst.id] = history;
            state.previousClose[inst.id] = history[0].value;
            state.openPrices[inst.id] = history[Math.floor(points * 0.2)].value;
        } else {
            // Append new tick
            const lastPrice = existing[existing.length - 1].value;
            const volMap = {
                sp500: 0.0015, nasdaq: 0.002, dow: 0.0012,
                oil: 0.004, gold: 0.002, dxy: 0.001,
            };
            const vol = volMap[inst.id] || 0.0015;

            // Occasional geopolitical-driven spike
            let geoShock = 0;
            if (Math.random() < 0.03) { // 3% chance each tick
                geoShock = (Math.random() - 0.5) * 0.02;
                if (inst.id === 'oil') geoShock = Math.abs(geoShock) * 2; // Oil spikes up on tension
                if (inst.id === 'gold') geoShock = Math.abs(geoShock) * 1.5; // Gold safe haven
            }

            const drift = (Math.random() - 0.501) * vol + geoShock;
            const newPrice = lastPrice * (1 + drift);

            existing.push({
                label: formatTimestamp(now, state.settings.chartTimeframe),
                value: newPrice,
                timestamp: now,
            });

            // Keep max 500 points
            if (existing.length > 500) existing.shift();
        }

        const history = state.priceHistory[inst.id];
        state.currentPrices[inst.id] = history[history.length - 1].value;
        if (!state.previousClose[inst.id]) {
            state.previousClose[inst.id] = history[0].value;
        }
    });

    setConnectionStatus('connected', 'Demo');
    refreshUI();
}

// ---------------------------------------------------------------------------
// 10. UI Refresh
// ---------------------------------------------------------------------------
function refreshUI() {
    INSTRUMENTS.forEach(inst => {
        const price = state.currentPrices[inst.id];
        const prevClose = state.previousClose[inst.id] ?? inst.basePrice;
        const history = state.priceHistory[inst.id] || [];

        // Summary card
        updateSummaryCard(inst, price, prevClose);

        // Chart
        updateChart(inst, history);
        updateChartPrice(inst, price, prevClose);

        // Volatility
        const vol = computeVolatility(history);
        updateVolatilityDisplay(inst, vol);

        // Alerts
        checkAlerts(inst, price, prevClose);
    });

    // Volatility table
    updateVolTable();

    // Timestamp
    document.getElementById('lastUpdate').textContent =
        `Updated: ${new Date().toLocaleTimeString()}`;
}

// ---------------------------------------------------------------------------
// 11. Data Loop
// ---------------------------------------------------------------------------
function startDataLoop() {
    fetchAllData();
    state.refreshTimer = setInterval(() => {
        fetchAllData();
        // Occasionally add news
        if (Math.random() < 0.3) addLiveNewsItem();
    }, state.settings.refreshInterval * 1000);
}

function restartDataLoop() {
    clearInterval(state.refreshTimer);
    startDataLoop();
}

// ---------------------------------------------------------------------------
// 12. Utilities
// ---------------------------------------------------------------------------
function formatPrice(val, decimals = 2) {
    if (val == null || isNaN(val)) return '—';
    return val.toLocaleString('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals,
    });
}

function formatTimestamp(ts, timeframe) {
    const d = new Date(ts);
    if (timeframe === '1d' || timeframe === '5d') {
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
}

function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r},${g},${b},${alpha})`;
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function setConnectionStatus(status, text) {
    const dot = document.querySelector('.status-dot');
    const label = document.querySelector('.status-text');
    dot.className = 'status-dot';
    if (status === 'connected') dot.classList.add('connected');
    if (status === 'error') dot.classList.add('error');
    label.textContent = text;
}
