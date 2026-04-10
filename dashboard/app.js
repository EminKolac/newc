// ============================================================
// Market Risk Dashboard — Core Application
// Real-time charts, volatility metrics, alerts, geopolitical feed
// ============================================================

(function () {
    'use strict';

    // ── Asset Definitions ────────────────────────────────────
    const ASSETS = {
        sp500:  { label: 'S&P 500',   ticker: 'SPX',   base: 5450,  vol: 0.008, decimals: 2, color: '#3b82f6' },
        nasdaq: { label: 'Nasdaq',     ticker: 'IXIC',  base: 17100, vol: 0.010, decimals: 2, color: '#8b5cf6' },
        dow:    { label: 'Dow Jones',  ticker: 'DJI',   base: 41200, vol: 0.007, decimals: 2, color: '#06b6d4' },
        oil:    { label: 'Crude Oil',  ticker: 'WTI',   base: 78.50, vol: 0.015, decimals: 2, color: '#f97316' },
        gold:   { label: 'Gold',       ticker: 'XAU',   base: 2380,  vol: 0.006, decimals: 2, color: '#f59e0b' },
        dxy:    { label: 'USD Index',  ticker: 'DXY',   base: 104.20,vol: 0.003, decimals: 3, color: '#10b981' },
    };

    const ASSET_KEYS = Object.keys(ASSETS);
    const MAX_POINTS = 200;
    const UPDATE_MS = 3000;

    // ── State ────────────────────────────────────────────────
    const state = {
        prices: {},      // { sp500: [{ time, value }], ... }
        opens: {},       // opening prices
        highs: {},
        lows: {},
        charts: {},
        volChart: null,
        alertLog: [],
        newsItems: [],
        newsFilter: 'all',
        geopoliticalBias: 0,  // -1 bearish shock, 0 neutral, +1 bullish relief
        biasDecay: 0,
        eventCooldown: 0,
    };

    // ── Initialization ───────────────────────────────────────
    function init() {
        ASSET_KEYS.forEach(key => {
            const a = ASSETS[key];
            const startPrice = a.base * (1 + (Math.random() - 0.5) * 0.02);
            state.prices[key] = [];
            state.opens[key] = startPrice;
            state.highs[key] = startPrice;
            state.lows[key] = startPrice;
            // Seed historical data (60 points)
            let p = startPrice * (1 - a.vol * 3);
            for (let i = 60; i > 0; i--) {
                p = walkPrice(p, a.vol * 0.7);
                state.prices[key].push({ time: Date.now() - i * UPDATE_MS, value: p });
            }
            state.opens[key] = state.prices[key][0].value;
            state.highs[key] = Math.max(...state.prices[key].map(d => d.value));
            state.lows[key]  = Math.min(...state.prices[key].map(d => d.value));
        });

        buildCards();
        buildCharts();
        buildVolatilityChart();
        buildCorrelationTable();
        setupNewsFilter();
        seedNews();
        updateClock();
        setInterval(tick, UPDATE_MS);
        setInterval(updateClock, 1000);
        setInterval(maybeInjectNews, 12000);
    }

    // ── Price Random Walk ────────────────────────────────────
    function walkPrice(price, vol) {
        const drift = (Math.random() - 0.5) * 2;
        const jump = Math.random() < 0.02 ? (Math.random() - 0.5) * 4 : 0;
        return price * (1 + (drift + jump + state.geopoliticalBias * 0.3) * vol);
    }

    // ── Main Tick ────────────────────────────────────────────
    function tick() {
        // Decay geopolitical bias
        if (state.biasDecay > 0) {
            state.biasDecay--;
            if (state.biasDecay === 0) state.geopoliticalBias = 0;
        }
        if (state.eventCooldown > 0) state.eventCooldown--;

        const threshold = parseFloat(document.getElementById('alert-threshold').value) || 2;

        ASSET_KEYS.forEach(key => {
            const a = ASSETS[key];
            const last = state.prices[key][state.prices[key].length - 1].value;

            // Oil and gold react more to geopolitical events
            let effectiveVol = a.vol;
            if (state.geopoliticalBias !== 0) {
                if (key === 'oil') effectiveVol *= 2.5;
                if (key === 'gold') effectiveVol *= 1.8;
                if (key === 'dxy') effectiveVol *= 1.3;
            }

            const newPrice = walkPrice(last, effectiveVol);
            const now = Date.now();
            state.prices[key].push({ time: now, value: newPrice });
            if (state.prices[key].length > MAX_POINTS) state.prices[key].shift();

            // Track high/low
            if (newPrice > state.highs[key]) state.highs[key] = newPrice;
            if (newPrice < state.lows[key])  state.lows[key] = newPrice;

            // Check alerts
            const changeFromOpen = ((newPrice - state.opens[key]) / state.opens[key]) * 100;
            const changeFromLast = ((newPrice - last) / last) * 100;

            if (Math.abs(changeFromOpen) >= threshold) {
                triggerAlert(key, newPrice, changeFromOpen, 'from open');
            }
            if (Math.abs(changeFromLast) >= threshold * 0.5) {
                triggerAlert(key, newPrice, changeFromLast, 'sudden move');
            }
        });

        updateCards();
        updateCharts();
        updateTickerBar();
        updateVolatility();
        updateCorrelationTable();
    }

    // ── Summary Cards ────────────────────────────────────────
    function buildCards() {
        const container = document.getElementById('cards-row');
        container.innerHTML = ASSET_KEYS.map(key => {
            const a = ASSETS[key];
            return `
                <div class="summary-card" id="card-${key}" data-key="${key}">
                    <div class="card-label">${a.label} (${a.ticker})</div>
                    <div class="card-price" id="price-${key}">--</div>
                    <div class="card-change" id="change-${key}">--</div>
                    <div class="card-range" id="range-${key}">H: -- / L: --</div>
                </div>`;
        }).join('');
    }

    function updateCards() {
        ASSET_KEYS.forEach(key => {
            const a = ASSETS[key];
            const data = state.prices[key];
            const current = data[data.length - 1].value;
            const prev = data.length > 2 ? data[data.length - 2].value : current;
            const open = state.opens[key];
            const change = ((current - open) / open) * 100;

            const priceEl = document.getElementById(`price-${key}`);
            const changeEl = document.getElementById(`change-${key}`);
            const rangeEl = document.getElementById(`range-${key}`);
            const cardEl = document.getElementById(`card-${key}`);

            priceEl.textContent = formatPrice(current, a.decimals);
            const sign = change >= 0 ? '+' : '';
            const absDiff = Math.abs(current - open);
            changeEl.textContent = `${sign}${change.toFixed(2)}% (${sign}${formatPrice(absDiff, a.decimals)})`;
            changeEl.className = `card-change ${change >= 0 ? 'up' : 'down'}`;
            rangeEl.textContent = `H: ${formatPrice(state.highs[key], a.decimals)} / L: ${formatPrice(state.lows[key], a.decimals)}`;

            // Flash effect on significant moves
            if (current > prev * 1.001) {
                cardEl.classList.remove('flash-red');
                cardEl.classList.add('flash-green');
                setTimeout(() => cardEl.classList.remove('flash-green'), 500);
            } else if (current < prev * 0.999) {
                cardEl.classList.remove('flash-green');
                cardEl.classList.add('flash-red');
                setTimeout(() => cardEl.classList.remove('flash-red'), 500);
            }
        });
    }

    // ── Ticker Bar ───────────────────────────────────────────
    function updateTickerBar() {
        const bar = document.getElementById('ticker-bar');
        bar.innerHTML = ASSET_KEYS.map(key => {
            const a = ASSETS[key];
            const data = state.prices[key];
            const current = data[data.length - 1].value;
            const change = ((current - state.opens[key]) / state.opens[key]) * 100;
            const dir = change >= 0 ? 'up' : 'down';
            const arrow = change >= 0 ? '&#9650;' : '&#9660;';
            return `<div class="ticker-item">
                <span class="label">${a.ticker}</span>
                <span class="price">${formatPrice(current, a.decimals)}</span>
                <span class="change ${dir}">${arrow} ${change >= 0 ? '+' : ''}${change.toFixed(2)}%</span>
            </div>`;
        }).join('');
    }

    // ── Charts ───────────────────────────────────────────────
    function buildCharts() {
        ASSET_KEYS.forEach(key => {
            const a = ASSETS[key];
            const ctx = document.getElementById(`chart-${key}`).getContext('2d');
            const data = state.prices[key];

            const gradient = ctx.createLinearGradient(0, 0, 0, 250);
            gradient.addColorStop(0, a.color + '40');
            gradient.addColorStop(1, a.color + '05');

            state.charts[key] = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(d => formatTime(d.time)),
                    datasets: [{
                        label: a.label,
                        data: data.map(d => d.value),
                        borderColor: a.color,
                        backgroundColor: gradient,
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3,
                        pointRadius: 0,
                        pointHoverRadius: 4,
                        pointHoverBackgroundColor: a.color,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: { duration: 300 },
                    interaction: { intersect: false, mode: 'index' },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#1a2235',
                            titleColor: '#e2e8f0',
                            bodyColor: '#94a3b8',
                            borderColor: '#2a3550',
                            borderWidth: 1,
                            callbacks: {
                                label: ctx => `${a.label}: ${formatPrice(ctx.parsed.y, a.decimals)}`
                            }
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
                                        content: 'Open',
                                        enabled: true,
                                        position: 'start',
                                        backgroundColor: '#334155',
                                        color: '#94a3b8',
                                        font: { size: 10 }
                                    }
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            display: true,
                            grid: { color: '#1e293b' },
                            ticks: { color: '#64748b', maxTicksLimit: 6, font: { size: 10 } }
                        },
                        y: {
                            display: true,
                            grid: { color: '#1e293b' },
                            ticks: {
                                color: '#64748b', font: { size: 10 },
                                callback: v => formatPrice(v, a.decimals > 2 ? 2 : a.decimals)
                            }
                        }
                    }
                }
            });

            // Set canvas container height
            document.getElementById(`chart-${key}`).parentElement.style.height = '220px';
        });
    }

    function updateCharts() {
        ASSET_KEYS.forEach(key => {
            const chart = state.charts[key];
            const data = state.prices[key];
            const a = ASSETS[key];

            chart.data.labels = data.map(d => formatTime(d.time));
            chart.data.datasets[0].data = data.map(d => d.value);
            chart.update('none');

            // Update badge
            const current = data[data.length - 1].value;
            const change = ((current - state.opens[key]) / state.opens[key]) * 100;
            const badge = document.getElementById(`badge-${key}`);
            badge.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)}%`;
            badge.className = `chart-badge ${change >= 0 ? 'up' : 'down'}`;
        });
    }

    // ── Volatility ───────────────────────────────────────────
    function buildVolatilityChart() {
        const ctx = document.getElementById('chart-volatility').getContext('2d');
        state.volChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ASSET_KEYS.map(k => ASSETS[k].ticker),
                datasets: [{
                    label: 'Realized Vol (%)',
                    data: ASSET_KEYS.map(() => 0),
                    backgroundColor: ASSET_KEYS.map(k => ASSETS[k].color + '80'),
                    borderColor: ASSET_KEYS.map(k => ASSETS[k].color),
                    borderWidth: 1,
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { display: false }, ticks: { color: '#64748b', font: { size: 10 } } },
                    y: {
                        grid: { color: '#1e293b' },
                        ticks: { color: '#64748b', font: { size: 10 }, callback: v => v.toFixed(1) + '%' }
                    }
                }
            }
        });
    }

    function updateVolatility() {
        const volGrid = document.getElementById('vol-grid');
        const vols = {};

        ASSET_KEYS.forEach(key => {
            const data = state.prices[key].map(d => d.value);
            if (data.length < 5) { vols[key] = 0; return; }

            // Calculate realized volatility (annualized std dev of returns)
            const returns = [];
            for (let i = 1; i < data.length; i++) {
                returns.push(Math.log(data[i] / data[i - 1]));
            }
            const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
            const variance = returns.reduce((a, b) => a + (b - mean) ** 2, 0) / (returns.length - 1);
            const stdDev = Math.sqrt(variance);
            // Annualize: multiply by sqrt of trading periods per year
            const annualized = stdDev * Math.sqrt(252 * (86400000 / UPDATE_MS)) * 100;
            vols[key] = Math.min(annualized, 200); // cap display
        });

        // Show top metrics
        const volEntries = ASSET_KEYS.map(key => ({ key, vol: vols[key] }));
        volEntries.sort((a, b) => b.vol - a.vol);

        volGrid.innerHTML = volEntries.slice(0, 4).map(({ key, vol }) => {
            const level = vol > 30 ? 'high' : vol > 15 ? 'medium' : 'low';
            return `<div class="vol-item">
                <div class="vol-label">${ASSETS[key].ticker}</div>
                <div class="vol-value ${level}">${vol.toFixed(1)}%</div>
            </div>`;
        }).join('');

        // Update bar chart
        state.volChart.data.datasets[0].data = ASSET_KEYS.map(k => vols[k]);
        state.volChart.update('none');
    }

    // ── Correlation Matrix ───────────────────────────────────
    function buildCorrelationTable() {
        updateCorrelationTable();
    }

    function updateCorrelationTable() {
        const table = document.getElementById('corr-table');
        const returns = {};

        ASSET_KEYS.forEach(key => {
            const data = state.prices[key].map(d => d.value);
            const ret = [];
            // Use last 30 periods
            const start = Math.max(0, data.length - 31);
            for (let i = start + 1; i < data.length; i++) {
                ret.push(Math.log(data[i] / data[i - 1]));
            }
            returns[key] = ret;
        });

        function corr(a, b) {
            const n = Math.min(a.length, b.length);
            if (n < 3) return 0;
            const ax = a.slice(-n), bx = b.slice(-n);
            const ma = ax.reduce((s, v) => s + v, 0) / n;
            const mb = bx.reduce((s, v) => s + v, 0) / n;
            let cov = 0, va = 0, vb = 0;
            for (let i = 0; i < n; i++) {
                const da = ax[i] - ma, db = bx[i] - mb;
                cov += da * db; va += da * da; vb += db * db;
            }
            const denom = Math.sqrt(va * vb);
            return denom === 0 ? 0 : cov / denom;
        }

        let html = '<tr><th></th>' + ASSET_KEYS.map(k => `<th>${ASSETS[k].ticker}</th>`).join('') + '</tr>';
        ASSET_KEYS.forEach(ki => {
            html += `<tr><th>${ASSETS[ki].ticker}</th>`;
            ASSET_KEYS.forEach(kj => {
                const c = ki === kj ? 1 : corr(returns[ki], returns[kj]);
                const bg = corrColor(c);
                html += `<td style="background:${bg}; color: ${Math.abs(c) > 0.5 ? '#fff' : '#94a3b8'}">${c.toFixed(2)}</td>`;
            });
            html += '</tr>';
        });
        table.innerHTML = html;
    }

    function corrColor(c) {
        if (c >= 0) {
            const intensity = Math.floor(c * 180);
            return `rgba(16, 185, 129, ${(intensity / 255).toFixed(2)})`;
        } else {
            const intensity = Math.floor(-c * 180);
            return `rgba(239, 68, 68, ${(intensity / 255).toFixed(2)})`;
        }
    }

    // ── Alert System ─────────────────────────────────────────
    function triggerAlert(key, price, change, type) {
        const a = ASSETS[key];
        const id = `${key}-${type}-${Math.floor(Date.now() / 30000)}`; // throttle per 30s
        if (state.alertLog.some(al => al.id === id)) return;

        const alert = {
            id,
            time: Date.now(),
            asset: a.label,
            ticker: a.ticker,
            price,
            change,
            type,
        };
        state.alertLog.unshift(alert);
        if (state.alertLog.length > 50) state.alertLog.pop();

        // Show banner for big moves
        if (Math.abs(change) >= 2) {
            showBanner(alert);
        }

        // Play sound
        if (document.getElementById('alert-sound').checked) {
            playAlertSound();
        }

        renderAlerts();
    }

    function showBanner(alert) {
        const banner = document.getElementById('alert-banner');
        const text = document.getElementById('alert-text');
        const dir = alert.change > 0 ? 'UP' : 'DOWN';
        text.innerHTML = `<strong>${alert.ticker}</strong> ${dir} ${Math.abs(alert.change).toFixed(2)}% — ` +
            `${alert.type} at ${formatPrice(alert.price, ASSETS[Object.keys(ASSETS).find(k => ASSETS[k].ticker === alert.ticker)].decimals)}`;
        banner.classList.remove('hidden');
        clearTimeout(state.bannerTimeout);
        state.bannerTimeout = setTimeout(() => banner.classList.add('hidden'), 8000);
    }

    function dismissAlert() {
        document.getElementById('alert-banner').classList.add('hidden');
    }

    function renderAlerts() {
        const list = document.getElementById('alert-list');
        list.innerHTML = state.alertLog.slice(0, 30).map(al => {
            const dir = al.change > 0 ? '+' : '';
            return `<div class="alert-item">
                <div class="alert-time">${new Date(al.time).toLocaleTimeString()}</div>
                <div class="alert-msg">${al.ticker} ${dir}${al.change.toFixed(2)}%</div>
                <div class="alert-detail">${al.type} — ${formatPrice(al.price, 2)}</div>
            </div>`;
        }).join('');
    }

    function playAlertSound() {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.value = 880;
            osc.type = 'sine';
            gain.gain.value = 0.08;
            osc.start();
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.2);
            osc.stop(ctx.currentTime + 0.25);
        } catch (e) { /* Audio not available */ }
    }

    // ── Geopolitical News Feed ───────────────────────────────
    const NEWS_TEMPLATES = [
        // Ceasefire developments
        {
            tags: ['ceasefire', 'markets'],
            severity: 'high',
            impact: 'bullish',
            bias: 0.6,
            headlines: [
                'US-Iran ceasefire talks enter final stage; both sides signal readiness for framework agreement',
                'Breaking: US and Iran reach preliminary ceasefire agreement — full details expected within 48 hours',
                'Ceasefire monitors deployed to Persian Gulf as US-Iran talks yield breakthrough',
                'Senior US diplomat confirms "significant progress" in Iran ceasefire negotiations',
                'Iran signals willingness to accept ceasefire terms; oil futures drop on de-escalation hopes',
            ],
            bodies: [
                'Markets are reacting positively to signs of de-escalation. Energy prices are falling as supply disruption fears ease. Safe-haven assets retreating.',
                'Diplomatic sources say both sides have agreed on a monitoring mechanism. Regional shipping lanes expected to normalize within weeks.',
                'The breakthrough comes after months of back-channel diplomacy. Analysts expect oil prices to drop $5-8/bbl if agreement is finalized.',
            ]
        },
        {
            tags: ['ceasefire'],
            severity: 'medium',
            impact: 'neutral',
            bias: 0.2,
            headlines: [
                'US-Iran ceasefire negotiations resume in Oman; cautious optimism from both delegations',
                'European mediators join US-Iran talks to bridge remaining gaps in ceasefire proposal',
                'UN Security Council discusses resolution supporting US-Iran ceasefire framework',
                'Iran foreign ministry: ceasefire talks "constructive but complex"',
            ],
            bodies: [
                'Ongoing talks continue but significant hurdles remain on sanctions relief timeline and verification mechanisms.',
                'Market participants remain cautious, pricing in approximately 40% probability of near-term agreement.',
            ]
        },
        // Strait of Hormuz escalation
        {
            tags: ['hormuz', 'oil', 'military'],
            severity: 'high',
            impact: 'bearish',
            bias: -0.8,
            headlines: [
                'BREAKING: Iran IRGC conducts live-fire naval exercise in Strait of Hormuz; shipping traffic diverted',
                'Two commercial tankers report harassment by IRGC fast boats near Strait of Hormuz',
                'Pentagon deploys additional carrier strike group to Persian Gulf amid Hormuz tensions',
                'Iran threatens to close Strait of Hormuz if new sanctions imposed; oil spikes',
                'IRGC seizes foreign-flagged tanker in Strait of Hormuz — US demands immediate release',
            ],
            bodies: [
                'Oil prices surge as 20% of global oil supply transits through the Strait. Insurance premiums for Gulf shipping skyrocket 300%.',
                'The Pentagon has raised CENTCOM alert level. Oil futures jump on fears of sustained supply disruption through the world\'s most critical oil chokepoint.',
                'Global energy markets in turmoil. Brent crude up $6 in after-hours trading. Safe-haven flows into gold and US Treasuries.',
            ]
        },
        {
            tags: ['hormuz', 'oil'],
            severity: 'medium',
            impact: 'bearish',
            bias: -0.4,
            headlines: [
                'Naval activity increases near Strait of Hormuz; commercial shippers report minor delays',
                'Lloyd\'s of London raises war risk premiums for Strait of Hormuz transit by 150%',
                'US Fifth Fleet increases patrols in Strait of Hormuz as tensions simmer',
                'Satellite imagery shows increased Iranian naval deployments near Hormuz chokepoint',
            ],
            bodies: [
                'While no direct confrontation has occurred, the elevated military presence is keeping energy markets on edge.',
                'Shipping companies are evaluating alternative routes, though the Strait remains the only viable path for Persian Gulf crude exports.',
            ]
        },
        // Sanctions
        {
            tags: ['sanctions', 'oil'],
            severity: 'medium',
            impact: 'bearish',
            bias: -0.3,
            headlines: [
                'US Treasury announces new sanctions targeting Iranian oil exports and banking sector',
                'EU joins US in expanding sanctions on Iran; targets shipping and petrochemical sectors',
                'China pushes back on secondary sanctions affecting Iranian oil purchases',
                'New US sanctions target Iranian drone program and associated financial networks',
            ],
            bodies: [
                'The new sanctions are expected to remove 500K-800K bbl/day of Iranian crude from the market, tightening global supply.',
                'Sanctions pressure is contributing to uncertainty in energy markets, with traders pricing in higher risk premiums.',
            ]
        },
        // De-escalation
        {
            tags: ['ceasefire', 'hormuz'],
            severity: 'low',
            impact: 'bullish',
            bias: 0.5,
            headlines: [
                'Iran pulls back naval forces from Strait of Hormuz as goodwill gesture ahead of ceasefire talks',
                'Strait of Hormuz shipping returns to normal after Iran de-escalation; oil retreats',
                'US eases select sanctions as confidence-building measure in ceasefire process',
                'Gulf states welcome US-Iran diplomatic progress; regional risk premium declining',
            ],
            bodies: [
                'Markets rally as geopolitical risk premium unwinds. Energy complex drops sharply. Equity futures point higher.',
                'The de-escalation is being seen as a significant positive development for global energy security and trade flows.',
            ]
        },
        // Military
        {
            tags: ['military', 'markets'],
            severity: 'high',
            impact: 'bearish',
            bias: -0.6,
            headlines: [
                'US military assets in Persian Gulf placed on heightened alert; risk of direct confrontation rises',
                'Reports of exchange of fire between US Navy and IRGC patrol boats — details emerging',
                'Israel and US conduct joint military exercise simulating Iran strike scenarios',
                'Iran test-fires ballistic missile capable of reaching US bases in Gulf region',
            ],
            bodies: [
                'Market volatility spikes as investors rush to safe-haven assets. VIX surges above 30. Gold breaks to new highs.',
                'Defense stocks rally while broader market sells off. Crude oil jumps on supply disruption fears.',
            ]
        },
    ];

    function seedNews() {
        // Add 5 initial news items
        for (let i = 0; i < 5; i++) {
            const template = NEWS_TEMPLATES[Math.floor(Math.random() * NEWS_TEMPLATES.length)];
            const item = generateNewsItem(template, Date.now() - (5 - i) * 60000 * Math.random() * 10);
            state.newsItems.push(item);
        }
        renderNews();
    }

    function generateNewsItem(template, time) {
        return {
            time: time || Date.now(),
            headline: template.headlines[Math.floor(Math.random() * template.headlines.length)],
            body: template.bodies[Math.floor(Math.random() * template.bodies.length)],
            tags: template.tags,
            severity: template.severity,
            impact: template.impact,
        };
    }

    function maybeInjectNews() {
        if (Math.random() > 0.4) return; // 40% chance each 12s
        if (state.eventCooldown > 0) return;

        const template = NEWS_TEMPLATES[Math.floor(Math.random() * NEWS_TEMPLATES.length)];
        const item = generateNewsItem(template);
        state.newsItems.unshift(item);
        if (state.newsItems.length > 30) state.newsItems.pop();

        // Apply geopolitical bias to price movements
        state.geopoliticalBias = template.bias;
        state.biasDecay = Math.floor(5 + Math.random() * 10); // 5-15 ticks
        state.eventCooldown = 4; // min 4 ticks between events

        renderNews();
    }

    function renderNews() {
        const list = document.getElementById('news-list');
        const filtered = state.newsFilter === 'all'
            ? state.newsItems
            : state.newsItems.filter(n => n.tags.includes(state.newsFilter));

        list.innerHTML = filtered.slice(0, 20).map(item => {
            const timeStr = new Date(item.time).toLocaleTimeString();
            const tagsHtml = item.tags.map(t => `<span class="news-tag ${t}">${t}</span>`).join('');
            return `<div class="news-item severity-${item.severity}">
                <div class="news-time">${timeStr}</div>
                <div class="news-headline">${item.headline}</div>
                <div class="news-body">${item.body}</div>
                <div class="news-tags">${tagsHtml}</div>
                <div class="news-impact ${item.impact}">Market Impact: ${item.impact.toUpperCase()}</div>
            </div>`;
        }).join('');
    }

    function setupNewsFilter() {
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                state.newsFilter = btn.dataset.filter;
                renderNews();
            });
        });
    }

    // ── Utilities ────────────────────────────────────────────
    function formatPrice(val, decimals) {
        return val.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
    }

    function formatTime(ts) {
        return new Date(ts).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }

    function updateClock() {
        const now = new Date();
        document.getElementById('clock').textContent = now.toLocaleString('en-US', {
            weekday: 'short', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit',
        });
    }

    // Make dismissAlert available globally
    window.dismissAlert = dismissAlert;

    // ── Start ────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', init);
})();
