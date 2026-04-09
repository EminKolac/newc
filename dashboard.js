// ============================================================
// Geopolitical Market Dashboard - Main Engine
// Tracks: S&P 500, Nasdaq, Dow, WTI Oil, Gold, DXY
// Features: Real-time charts, volatility, alerts, news feed
// ============================================================

(function () {
    'use strict';

    // ---- Asset Configuration ----
    const ASSETS = {
        sp500:  { name: 'S&P 500',   base: 5250,   volatility: 0.008, color: '#3b82f6', decimals: 2 },
        nasdaq: { name: 'NASDAQ',     base: 16400,  volatility: 0.010, color: '#8b5cf6', decimals: 2 },
        dow:    { name: 'Dow Jones',  base: 39200,  volatility: 0.007, color: '#06b6d4', decimals: 2 },
        oil:    { name: 'WTI Oil',    base: 82.50,  volatility: 0.015, color: '#f97316', decimals: 2 },
        gold:   { name: 'Gold',       base: 2340,   volatility: 0.006, color: '#fbbf24', decimals: 2 },
        dxy:    { name: 'DXY',        base: 104.20, volatility: 0.003, color: '#10b981', decimals: 3 },
    };

    const ASSET_KEYS = Object.keys(ASSETS);
    const MAX_DATA_POINTS = 120;
    const ALERT_THRESHOLD = 2.0; // percent
    const UPDATE_INTERVAL = 1000; // ms

    // ---- State ----
    const state = {
        prices: {},       // current price per asset
        openPrices: {},   // session open price
        history: {},      // array of price history per asset
        charts: {},       // Chart.js instances
        alerts: [],       // alert log
        newsFilter: 'all',
        newsItems: [],
        vix: 22,
        geopoliticalRisk: 'ELEVATED',
        eventQueue: [],   // scheduled geopolitical events
    };

    // ---- Initialize State ----
    function initState() {
        for (const key of ASSET_KEYS) {
            const asset = ASSETS[key];
            const jitter = (Math.random() - 0.5) * asset.base * 0.01;
            state.openPrices[key] = asset.base + jitter;
            state.prices[key] = state.openPrices[key];
            state.history[key] = [];
            // Seed 60 historical points
            let p = state.openPrices[key];
            for (let i = 0; i < 60; i++) {
                p += (Math.random() - 0.5) * asset.base * asset.volatility * 0.3;
                state.history[key].push(p);
            }
            state.prices[key] = p;
        }
    }

    // ---- Price Simulation Engine ----
    // Models mean-reverting random walk with occasional shocks from geopolitical events
    let shockMultiplier = 1.0;
    let shockDirection = 0; // -1 escalation, +1 de-escalation
    let shockDecay = 0;

    function triggerGeopoliticalShock(direction, magnitude) {
        shockDirection = direction;
        shockMultiplier = magnitude;
        shockDecay = 30; // decays over 30 ticks
    }

    function simulateTick() {
        // Decay shock
        if (shockDecay > 0) {
            shockDecay--;
            if (shockDecay === 0) {
                shockMultiplier = 1.0;
                shockDirection = 0;
            }
        }

        for (const key of ASSET_KEYS) {
            const asset = ASSETS[key];
            const prev = state.prices[key];
            let vol = asset.volatility;

            // Apply shock
            if (shockDecay > 0) {
                vol *= shockMultiplier;
                // Directional bias based on asset type
                let bias = 0;
                if (shockDirection === -1) {
                    // Escalation: stocks down, oil up, gold up, USD mixed
                    if (['sp500', 'nasdaq', 'dow'].includes(key)) bias = -0.3;
                    else if (key === 'oil') bias = 0.5;
                    else if (key === 'gold') bias = 0.3;
                    else if (key === 'dxy') bias = 0.1;
                } else if (shockDirection === 1) {
                    // De-escalation: stocks up, oil down, gold down
                    if (['sp500', 'nasdaq', 'dow'].includes(key)) bias = 0.3;
                    else if (key === 'oil') bias = -0.4;
                    else if (key === 'gold') bias = -0.2;
                    else if (key === 'dxy') bias = -0.05;
                }
                const change = (Math.random() - 0.5 + bias) * asset.base * vol;
                state.prices[key] = prev + change;
            } else {
                // Normal random walk with slight mean reversion
                const meanRev = (asset.base - prev) * 0.001;
                const change = (Math.random() - 0.5) * asset.base * vol + meanRev;
                state.prices[key] = prev + change;
            }

            // Clamp to reasonable range
            state.prices[key] = Math.max(asset.base * 0.7, Math.min(asset.base * 1.3, state.prices[key]));

            // Update history
            state.history[key].push(state.prices[key]);
            if (state.history[key].length > MAX_DATA_POINTS) {
                state.history[key].shift();
            }

            // Check alerts
            const pctChange = ((state.prices[key] - state.openPrices[key]) / state.openPrices[key]) * 100;
            if (Math.abs(pctChange) >= ALERT_THRESHOLD) {
                const existing = state.alerts.find(a =>
                    a.asset === key && Math.abs(a.pct - pctChange) < 0.3 &&
                    (Date.now() - a.timestamp) < 30000
                );
                if (!existing) {
                    addAlert(key, pctChange);
                }
            }
        }

        // Update VIX proxy
        const avgVol = ASSET_KEYS.reduce((sum, key) => {
            const h = state.history[key];
            if (h.length < 10) return sum;
            const returns = [];
            for (let i = 1; i < Math.min(h.length, 20); i++) {
                returns.push((h[i] - h[i - 1]) / h[i - 1]);
            }
            const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
            const variance = returns.reduce((a, b) => a + (b - mean) ** 2, 0) / returns.length;
            return sum + Math.sqrt(variance);
        }, 0) / ASSET_KEYS.length;

        state.vix = Math.max(10, Math.min(80, avgVol * 3000 + (shockMultiplier > 1 ? shockMultiplier * 8 : 0)));
    }

    // ---- Alert System ----
    function addAlert(assetKey, pctChange) {
        const asset = ASSETS[assetKey];
        const severity = Math.abs(pctChange) >= 3 ? 'critical' : 'warning';
        const direction = pctChange > 0 ? 'UP' : 'DOWN';
        const geoCause = shockDecay > 0
            ? (shockDirection === -1 ? ' | Linked to Iran escalation' : ' | Linked to ceasefire progress')
            : '';

        const alert = {
            asset: assetKey,
            name: asset.name,
            pct: pctChange,
            direction,
            severity,
            geoCause,
            timestamp: Date.now(),
            time: new Date().toLocaleTimeString(),
        };

        state.alerts.unshift(alert);
        if (state.alerts.length > 50) state.alerts.pop();

        // Show banner for critical alerts
        if (severity === 'critical') {
            showBanner(
                `${asset.name} ${direction} ${Math.abs(pctChange).toFixed(2)}%${geoCause}`,
                severity
            );
        }

        renderAlerts();
    }

    function showBanner(text, severity) {
        const banner = document.getElementById('alert-banner');
        const alertText = document.getElementById('alert-text');
        banner.className = `alert-banner ${severity}`;
        alertText.textContent = text;
        // Auto-dismiss after 8 seconds
        clearTimeout(banner._timeout);
        banner._timeout = setTimeout(() => {
            banner.classList.add('hidden');
        }, 8000);
    }

    window.dismissAlert = function () {
        document.getElementById('alert-banner').classList.add('hidden');
    };

    // ---- Chart Setup ----
    function createChart(key) {
        const ctx = document.getElementById(`chart-${key}`).getContext('2d');
        const asset = ASSETS[key];
        const gradient = ctx.createLinearGradient(0, 0, 0, 160);
        gradient.addColorStop(0, asset.color + '40');
        gradient.addColorStop(1, asset.color + '00');

        state.charts[key] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: state.history[key].map((_, i) => i),
                datasets: [{
                    data: [...state.history[key]],
                    borderColor: asset.color,
                    backgroundColor: gradient,
                    borderWidth: 1.5,
                    pointRadius: 0,
                    pointHitRadius: 8,
                    fill: true,
                    tension: 0.3,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 0 },
                interaction: {
                    intersect: false,
                    mode: 'index',
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1a2235',
                        borderColor: asset.color,
                        borderWidth: 1,
                        titleFont: { family: "'SF Mono', monospace", size: 11 },
                        bodyFont: { family: "'SF Mono', monospace", size: 12 },
                        callbacks: {
                            title: () => asset.name,
                            label: (ctx) => ctx.parsed.y.toFixed(asset.decimals),
                        }
                    }
                },
                scales: {
                    x: { display: false },
                    y: {
                        display: true,
                        grid: {
                            color: 'rgba(42, 53, 80, 0.3)',
                            drawBorder: false,
                        },
                        ticks: {
                            font: { family: "'SF Mono', monospace", size: 10 },
                            color: '#6b7280',
                            maxTicksLimit: 5,
                            callback: (v) => v.toFixed(asset.decimals <= 2 ? 0 : 2),
                        },
                        border: { display: false },
                    }
                }
            }
        });
    }

    function updateChart(key) {
        const chart = state.charts[key];
        const data = state.history[key];
        chart.data.labels = data.map((_, i) => i);
        chart.data.datasets[0].data = [...data];

        // Color line based on open vs current
        const change = state.prices[key] - state.openPrices[key];
        const color = change >= 0 ? '#10b981' : '#ef4444';
        chart.data.datasets[0].borderColor = color;

        const ctx = chart.ctx;
        const gradient = ctx.createLinearGradient(0, 0, 0, 160);
        gradient.addColorStop(0, color + '30');
        gradient.addColorStop(1, color + '00');
        chart.data.datasets[0].backgroundColor = gradient;

        chart.update('none');
    }

    // ---- Ticker Strip ----
    function renderTicker() {
        const strip = document.getElementById('ticker-strip');
        strip.innerHTML = ASSET_KEYS.map(key => {
            const asset = ASSETS[key];
            const price = state.prices[key];
            const change = ((price - state.openPrices[key]) / state.openPrices[key]) * 100;
            const dir = change >= 0 ? 'up' : 'down';
            const arrow = change >= 0 ? '\u25B2' : '\u25BC';
            return `
                <div class="ticker-item">
                    <span class="name">${asset.name}</span>
                    <span class="price">${price.toFixed(asset.decimals)}</span>
                    <span class="change ${dir}">${arrow} ${Math.abs(change).toFixed(2)}%</span>
                </div>
            `;
        }).join('');
    }

    // ---- Price Display ----
    function updatePriceDisplay() {
        for (const key of ASSET_KEYS) {
            const asset = ASSETS[key];
            const price = state.prices[key];
            const change = ((price - state.openPrices[key]) / state.openPrices[key]) * 100;
            const dir = change >= 0 ? 'up' : 'down';
            const arrow = change >= 0 ? '+' : '';

            const priceEl = document.getElementById(`price-${key}`);
            const changeEl = document.getElementById(`change-${key}`);
            if (priceEl) priceEl.textContent = price.toFixed(asset.decimals);
            if (changeEl) {
                changeEl.textContent = `${arrow}${change.toFixed(2)}%`;
                changeEl.className = `chart-change ${dir}`;
            }
        }
    }

    // ---- Volatility Metrics ----
    function calcVolatility(key) {
        const h = state.history[key];
        if (h.length < 10) return { atr: 0, stdDev: 0, range: 0, vScore: 0 };

        // Calculate returns
        const returns = [];
        for (let i = 1; i < h.length; i++) {
            returns.push((h[i] - h[i - 1]) / h[i - 1]);
        }

        // ATR proxy (average absolute return)
        const atr = returns.reduce((s, r) => s + Math.abs(r), 0) / returns.length;

        // Standard deviation of last 20 returns
        const recent = returns.slice(-20);
        const mean = recent.reduce((a, b) => a + b, 0) / recent.length;
        const variance = recent.reduce((a, b) => a + (b - mean) ** 2, 0) / recent.length;
        const stdDev = Math.sqrt(variance);

        // Intraday range %
        const last20 = h.slice(-20);
        const high = Math.max(...last20);
        const low = Math.min(...last20);
        const mid = (high + low) / 2;
        const range = ((high - low) / mid) * 100;

        // Composite volatility score (0-100)
        const vScore = Math.min(100, (stdDev * 5000 + range * 10 + atr * 3000));

        return { atr: atr * 100, stdDev: stdDev * 100, range, vScore };
    }

    function renderVolatility() {
        const tbody = document.getElementById('vol-table-body');
        tbody.innerHTML = ASSET_KEYS.map(key => {
            const asset = ASSETS[key];
            const v = calcVolatility(key);
            let scoreClass = 'low';
            if (v.vScore > 60) scoreClass = 'extreme';
            else if (v.vScore > 40) scoreClass = 'high';
            else if (v.vScore > 20) scoreClass = 'medium';

            return `
                <tr>
                    <td style="color: ${asset.color}; font-weight: 600">${asset.name}</td>
                    <td>${v.atr.toFixed(3)}%</td>
                    <td>${v.stdDev.toFixed(3)}%</td>
                    <td>${v.range.toFixed(2)}%</td>
                    <td><span class="vscore ${scoreClass}">${v.vScore.toFixed(0)}</span></td>
                </tr>
            `;
        }).join('');

        // VIX gauge
        const vix = state.vix;
        const pct = Math.min(100, (vix / 80) * 100);
        document.getElementById('vix-marker').style.left = `calc(${pct}% - 2px)`;
        const vixValueEl = document.getElementById('vix-value');
        vixValueEl.textContent = vix.toFixed(1);
        if (vix > 40) vixValueEl.style.color = '#ef4444';
        else if (vix > 25) vixValueEl.style.color = '#f59e0b';
        else vixValueEl.style.color = '#10b981';
    }

    // ---- Correlation Matrix ----
    function calcCorrelation(a, b) {
        const n = Math.min(a.length, b.length, 30);
        const aSlice = a.slice(-n);
        const bSlice = b.slice(-n);

        const aReturns = [], bReturns = [];
        for (let i = 1; i < n; i++) {
            aReturns.push((aSlice[i] - aSlice[i - 1]) / aSlice[i - 1]);
            bReturns.push((bSlice[i] - bSlice[i - 1]) / bSlice[i - 1]);
        }

        const aMean = aReturns.reduce((s, v) => s + v, 0) / aReturns.length;
        const bMean = bReturns.reduce((s, v) => s + v, 0) / bReturns.length;

        let cov = 0, aVar = 0, bVar = 0;
        for (let i = 0; i < aReturns.length; i++) {
            const da = aReturns[i] - aMean;
            const db = bReturns[i] - bMean;
            cov += da * db;
            aVar += da * da;
            bVar += db * db;
        }

        const denom = Math.sqrt(aVar * bVar);
        return denom === 0 ? 0 : cov / denom;
    }

    function renderCorrelation() {
        const el = document.getElementById('corr-matrix');
        const labels = ['', 'SPX', 'NDX', 'DJI', 'OIL', 'XAU', 'DXY'];
        let html = labels.map(l => `<div class="corr-cell header">${l}</div>`).join('');

        for (let i = 0; i < ASSET_KEYS.length; i++) {
            html += `<div class="corr-cell header">${labels[i + 1]}</div>`;
            for (let j = 0; j < ASSET_KEYS.length; j++) {
                const corr = i === j ? 1 : calcCorrelation(
                    state.history[ASSET_KEYS[i]],
                    state.history[ASSET_KEYS[j]]
                );
                const abs = Math.abs(corr);
                let bg;
                if (corr > 0) {
                    bg = `rgba(16, 185, 129, ${abs * 0.6})`;
                } else {
                    bg = `rgba(239, 68, 68, ${abs * 0.6})`;
                }
                html += `<div class="corr-cell" style="background:${bg}" title="${ASSET_KEYS[i]} vs ${ASSET_KEYS[j]}: ${corr.toFixed(2)}">${corr.toFixed(2)}</div>`;
            }
        }
        el.innerHTML = html;
    }

    // ---- Alerts Render ----
    function renderAlerts() {
        const list = document.getElementById('alerts-list');
        const countEl = document.getElementById('alert-count');
        countEl.textContent = state.alerts.length;

        list.innerHTML = state.alerts.slice(0, 20).map(a => `
            <div class="alert-item ${a.severity}">
                <span class="alert-time">${a.time}</span>
                <span class="alert-msg">${a.name} ${a.direction}${a.geoCause}</span>
                <span class="alert-pct" style="color: ${a.direction === 'UP' ? 'var(--green)' : 'var(--red)'}">
                    ${a.direction === 'UP' ? '+' : ''}${a.pct.toFixed(2)}%
                </span>
            </div>
        `).join('');
    }

    // ---- News Feed ----
    const NEWS_TEMPLATES = [
        // Escalation
        { headline: 'Iranian Revolutionary Guard conducts naval exercises near Strait of Hormuz', tags: ['iran', 'hormuz', 'military'], type: 'escalation', shock: [-1, 2.5] },
        { headline: 'US deploys additional carrier strike group to Persian Gulf', tags: ['iran', 'military'], type: 'escalation', shock: [-1, 2.0] },
        { headline: 'Iran threatens to block oil tanker traffic through Strait of Hormuz', tags: ['iran', 'hormuz', 'oil'], type: 'escalation', shock: [-1, 3.0] },
        { headline: 'Satellite imagery shows Iranian missile batteries repositioned near Hormuz', tags: ['iran', 'hormuz', 'military'], type: 'escalation', shock: [-1, 2.2] },
        { headline: 'Unconfirmed reports of Iranian drone activity over oil tankers in Gulf', tags: ['iran', 'hormuz', 'oil'], type: 'escalation', shock: [-1, 2.8] },
        { headline: 'US imposes new sanctions targeting Iranian oil exports', tags: ['iran', 'oil', 'sanctions'], type: 'escalation', shock: [-1, 1.5] },
        { headline: 'IRGC Navy seizes commercial tanker near Strait of Hormuz', tags: ['iran', 'hormuz', 'oil', 'breaking'], type: 'escalation', shock: [-1, 3.5] },
        { headline: 'Pentagon confirms Iranian-backed militia attack on US base in Iraq', tags: ['iran', 'military', 'breaking'], type: 'escalation', shock: [-1, 2.5] },
        { headline: 'Oil prices spike on reports of disrupted Hormuz shipping lanes', tags: ['hormuz', 'oil'], type: 'escalation', shock: [-1, 2.0] },
        { headline: 'Insurance rates for Gulf oil shipments surge to multi-year highs', tags: ['hormuz', 'oil'], type: 'escalation', shock: [-1, 1.2] },

        // De-escalation
        { headline: 'US and Iran agree to resume indirect ceasefire negotiations in Oman', tags: ['iran', 'ceasefire', 'diplomacy'], type: 'deescalation', shock: [1, 2.0] },
        { headline: 'Iran signals willingness to guarantee Strait of Hormuz shipping freedom', tags: ['iran', 'hormuz', 'ceasefire', 'diplomacy'], type: 'deescalation', shock: [1, 2.5] },
        { headline: 'EU mediators report "constructive progress" in Iran nuclear talks', tags: ['iran', 'diplomacy', 'ceasefire'], type: 'deescalation', shock: [1, 1.8] },
        { headline: 'Iran releases detained oil tanker crew as goodwill gesture', tags: ['iran', 'hormuz', 'oil', 'ceasefire'], type: 'deescalation', shock: [1, 2.0] },
        { headline: 'Saudi-Iran diplomatic channel reopened with US backing', tags: ['iran', 'diplomacy', 'ceasefire'], type: 'deescalation', shock: [1, 1.5] },
        { headline: 'US reduces naval posture in Gulf amid ceasefire optimism', tags: ['iran', 'military', 'ceasefire'], type: 'deescalation', shock: [1, 1.8] },
        { headline: 'BREAKING: Framework agreement reached on Iran ceasefire terms', tags: ['iran', 'ceasefire', 'diplomacy', 'breaking'], type: 'deescalation', shock: [1, 3.5] },
        { headline: 'Oil markets stabilize as Hormuz threat assessment downgraded', tags: ['hormuz', 'oil', 'ceasefire'], type: 'deescalation', shock: [1, 1.5] },
        { headline: 'Iran halts uranium enrichment escalation pending talks outcome', tags: ['iran', 'diplomacy', 'ceasefire'], type: 'deescalation', shock: [1, 2.2] },
        { headline: 'Shipping insurers reduce Gulf risk premiums after diplomatic breakthrough', tags: ['hormuz', 'oil', 'ceasefire'], type: 'deescalation', shock: [1, 1.3] },

        // Neutral / informational
        { headline: 'OPEC+ emergency meeting called to discuss Gulf supply disruption risks', tags: ['oil', 'hormuz'], type: 'neutral', shock: null },
        { headline: 'Global oil inventories drop to 5-year low amid Middle East uncertainty', tags: ['oil'], type: 'neutral', shock: null },
        { headline: 'Analysts warn of $120 oil if Strait of Hormuz disrupted for >48 hours', tags: ['hormuz', 'oil'], type: 'neutral', shock: null },
        { headline: 'Gold demand surges as investors seek safe haven assets', tags: ['iran'], type: 'neutral', shock: null },
        { headline: 'US Treasury Secretary: monitoring Middle East situation closely', tags: ['iran', 'diplomacy'], type: 'neutral', shock: null },
    ];

    const NEWS_SOURCES = ['Reuters', 'Bloomberg', 'AP', 'Al Jazeera', 'WSJ', 'FT', 'BBC', 'CNBC'];

    let newsIndex = 0;
    function generateNewsItem() {
        const template = NEWS_TEMPLATES[newsIndex % NEWS_TEMPLATES.length];
        newsIndex++;

        const item = {
            ...template,
            source: NEWS_SOURCES[Math.floor(Math.random() * NEWS_SOURCES.length)],
            time: new Date().toLocaleTimeString(),
            id: Date.now(),
        };

        state.newsItems.unshift(item);
        if (state.newsItems.length > 30) state.newsItems.pop();

        // Trigger market shock if applicable
        if (template.shock) {
            triggerGeopoliticalShock(template.shock[0], template.shock[1]);

            // Update threat level
            if (template.shock[0] === -1) {
                state.geopoliticalRisk = template.shock[1] >= 3 ? 'CRITICAL' : 'HIGH';
            } else {
                state.geopoliticalRisk = template.shock[1] >= 3 ? 'LOW' : 'MODERATE';
            }
            updateThreatLevel();
        }

        renderNews();
    }

    function renderNews() {
        const list = document.getElementById('news-list');
        const filtered = state.newsFilter === 'all'
            ? state.newsItems
            : state.newsItems.filter(n => n.tags.includes(state.newsFilter));

        list.innerHTML = filtered.map(n => `
            <div class="news-item ${n.type}">
                <div class="news-meta">
                    <span class="news-source">${n.source}</span>
                    <span class="news-time">${n.time}</span>
                </div>
                <div class="news-headline">${n.headline}</div>
                <div class="news-tags">
                    ${n.tags.map(t => `<span class="news-tag ${t}">${t}</span>`).join('')}
                </div>
            </div>
        `).join('');
    }

    function updateThreatLevel() {
        const el = document.getElementById('threat-value');
        const container = document.querySelector('.threat-level');
        el.textContent = state.geopoliticalRisk;

        const colors = {
            LOW: { color: '#10b981', border: '#10b981', bg: 'rgba(16,185,129,0.1)' },
            MODERATE: { color: '#f59e0b', border: '#f59e0b', bg: 'rgba(245,158,11,0.1)' },
            ELEVATED: { color: '#f97316', border: '#f97316', bg: 'rgba(249,115,22,0.1)' },
            HIGH: { color: '#ef4444', border: '#ef4444', bg: 'rgba(239,68,68,0.1)' },
            CRITICAL: { color: '#dc2626', border: '#dc2626', bg: 'rgba(220,38,38,0.15)' },
        };

        const c = colors[state.geopoliticalRisk] || colors.ELEVATED;
        el.style.color = c.color;
        container.style.borderColor = c.border;
        container.style.background = c.bg;
    }

    // ---- Clock ----
    function updateClock() {
        const now = new Date();
        const options = {
            timeZone: 'America/New_York',
            hour: '2-digit', minute: '2-digit', second: '2-digit',
            hour12: true,
        };
        const etTime = now.toLocaleTimeString('en-US', options);
        document.getElementById('clock').textContent = `${etTime} ET | ${now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
    }

    // ---- News Filter Buttons ----
    function setupNewsFilters() {
        document.querySelectorAll('.news-filter').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.news-filter').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.newsFilter = btn.dataset.filter;
                renderNews();
            });
        });
    }

    // ---- Timeframe Buttons ----
    function setupTimeframeButtons() {
        document.querySelectorAll('.tf-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                // In a real app, this would change chart timeframes
                // For demo, we just toggle the active state
            });
        });
    }

    // ---- Main Update Loop ----
    function update() {
        simulateTick();
        updatePriceDisplay();
        renderTicker();
        for (const key of ASSET_KEYS) {
            updateChart(key);
        }
        renderVolatility();
        updateClock();
    }

    // ---- Schedule News Events ----
    function scheduleNews() {
        // First news item immediately
        generateNewsItem();

        // Then every 8-15 seconds
        function scheduleNext() {
            const delay = 8000 + Math.random() * 7000;
            setTimeout(() => {
                generateNewsItem();
                scheduleNext();
            }, delay);
        }
        scheduleNext();
    }

    // ---- Correlation Update (less frequent) ----
    function startCorrelationUpdates() {
        renderCorrelation();
        setInterval(renderCorrelation, 5000);
    }

    // ---- Initialize ----
    function init() {
        initState();

        // Create charts
        for (const key of ASSET_KEYS) {
            createChart(key);
        }

        // Initial renders
        updatePriceDisplay();
        renderTicker();
        renderVolatility();
        renderAlerts();
        updateClock();
        updateThreatLevel();

        // Setup interactions
        setupNewsFilters();
        setupTimeframeButtons();

        // Start update loops
        setInterval(update, UPDATE_INTERVAL);
        scheduleNews();
        startCorrelationUpdates();
    }

    // Boot
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
