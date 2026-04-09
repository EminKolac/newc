/**
 * Main Application
 * Orchestrates all modules: market data, charts, alerts, and news feed.
 */

(function() {
    'use strict';

    // ---- Format Helpers ----
    function formatPrice(value, key) {
        if (typeof value !== 'number') return value;
        if (key === 'dxy') return value.toFixed(2);
        if (value > 10000) return value.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
        if (value > 100) return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        return value.toFixed(2);
    }

    function formatChange(change) {
        const sign = change >= 0 ? '+' : '';
        return sign + change.toFixed(2) + '%';
    }

    function getChangeClass(change) {
        if (Math.abs(change) < 0.01) return 'flat';
        return change >= 0 ? 'up' : 'down';
    }

    // ---- Clock ----
    function updateClock() {
        const el = document.getElementById('clock');
        if (!el) return;
        const now = new Date();
        el.textContent = now.toLocaleString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            timeZoneName: 'short'
        });
    }

    // ---- Market Status ----
    function updateMarketStatus() {
        const el = document.getElementById('market-status');
        if (!el) return;
        const now = new Date();
        const hour = now.getUTCHours();
        const day = now.getUTCDay();
        // NYSE: 14:30-21:00 UTC, Mon-Fri
        const isOpen = day >= 1 && day <= 5 && hour >= 14 && hour < 21;
        el.textContent = isOpen ? 'MARKET OPEN' : 'MARKET CLOSED';
        el.className = 'market-status ' + (isOpen ? 'open' : 'closed');
    }

    // ---- Ticker Strip ----
    function updateTickerStrip(data) {
        const container = document.getElementById('ticker-strip');
        if (!container) return;

        const items = Object.entries(data).map(([key, d]) => {
            const cls = getChangeClass(d.change);
            const arrow = d.change >= 0 ? '\u25B2' : '\u25BC';
            return `
                <div class="ticker-item">
                    <span class="ticker-symbol">${d.symbol}</span>
                    <span class="ticker-price ${cls === 'up' ? 'text-up' : cls === 'down' ? 'text-down' : 'text-flat'}">${formatPrice(d.price, key)}</span>
                    <span class="ticker-change ${cls}">${arrow} ${formatChange(d.change)}</span>
                </div>
            `;
        });

        container.innerHTML = items.join('');
    }

    // ---- Price Cards ----
    function updatePriceCards(data) {
        const container = document.getElementById('price-cards');
        if (!container) return;

        const html = Object.entries(data).map(([key, d]) => {
            const cls = getChangeClass(d.change);
            const arrow = d.change >= 0 ? '\u25B2' : '\u25BC';
            const prefix = key === 'dxy' ? '' : '$';
            return `
                <div class="price-card" id="card-${key}">
                    <div>
                        <div class="price-card-name">${d.name}</div>
                        <div style="font-size:10px;color:var(--text-muted)">${d.symbol}</div>
                    </div>
                    <div class="price-card-value ${cls === 'up' ? 'text-up' : cls === 'down' ? 'text-down' : ''}">${prefix}${formatPrice(d.price, key)}</div>
                    <div class="price-card-change ${cls === 'up' ? 'bg-up' : cls === 'down' ? 'bg-down' : 'bg-flat'}">${arrow} ${formatChange(d.change)}</div>
                </div>
            `;
        }).join('');

        container.innerHTML = html;
    }

    // Flash price cards on significant moves
    let flashTimers = {};
    function flashPriceCard(key, direction) {
        const card = document.getElementById('card-' + key);
        if (!card) return;

        card.classList.remove('flash-up', 'flash-down');
        void card.offsetWidth; // Trigger reflow
        card.classList.add(direction === 'up' ? 'flash-up' : 'flash-down');

        if (flashTimers[key]) clearTimeout(flashTimers[key]);
        flashTimers[key] = setTimeout(() => {
            card.classList.remove('flash-up', 'flash-down');
        }, 1500);
    }

    // ---- Volatility Metrics ----
    function updateVolMetrics(data) {
        const container = document.getElementById('vol-metrics');
        const badge = document.getElementById('vol-regime');
        if (!container) return;

        // Calculate aggregate metrics
        const keys = Object.keys(data);
        const vols = keys.map(k => data[k].realizedVol);
        const avgVol = vols.reduce((a, b) => a + b, 0) / vols.length;
        const maxVol = Math.max(...vols);
        const maxVolInstrument = keys[vols.indexOf(maxVol)];

        // Simple VIX-like proxy from S&P realized vol
        const vixProxy = data.sp500.realizedVol * 1.2 + 5;

        // Avg absolute change
        const avgAbsChange = keys.map(k => Math.abs(data[k].change)).reduce((a, b) => a + b, 0) / keys.length;

        const metrics = [
            { label: 'VIX Proxy', value: vixProxy.toFixed(1), color: vixProxy > 25 ? 'var(--accent-red)' : vixProxy > 18 ? 'var(--accent-amber)' : 'var(--accent-green)' },
            { label: 'Avg Realized Vol', value: avgVol.toFixed(1) + '%', color: avgVol > 30 ? 'var(--accent-red)' : 'var(--accent-amber)' },
            { label: 'Highest Vol', value: `${data[maxVolInstrument].symbol} ${maxVol.toFixed(1)}%`, color: 'var(--accent-orange)' },
            { label: 'Avg |Change|', value: avgAbsChange.toFixed(2) + '%', color: avgAbsChange > 1 ? 'var(--accent-red)' : 'var(--accent-cyan)' }
        ];

        container.innerHTML = metrics.map(m => `
            <div class="vol-metric">
                <div class="vol-metric-label">${m.label}</div>
                <div class="vol-metric-value" style="color:${m.color}">${m.value}</div>
            </div>
        `).join('');

        // Vol regime badge
        if (badge) {
            if (vixProxy > 30) {
                badge.textContent = 'EXTREME';
                badge.className = 'badge extreme';
            } else if (vixProxy > 22) {
                badge.textContent = 'ELEVATED';
                badge.className = 'badge elevated';
            } else {
                badge.textContent = 'NORMAL';
                badge.className = 'badge';
            }
        }
    }

    // ---- Risk Index Calculation ----
    function calculateRiskIndex(data) {
        // Composite risk score based on:
        // 1. Oil price spike (weight: 30%)
        // 2. Equity sell-off (weight: 25%)
        // 3. Gold safe-haven flow (weight: 20%)
        // 4. Volatility level (weight: 15%)
        // 5. Dollar strength (weight: 10%)

        const oilChange = Math.abs(data.oil.change);
        const equityAvg = (Math.abs(data.sp500.change) + Math.abs(data.nasdaq.change) + Math.abs(data.dow.change)) / 3;
        const goldChange = Math.abs(data.gold.change);
        const volLevel = data.sp500.realizedVol;
        const dxyChange = Math.abs(data.dxy.change);

        const oilScore = Math.min(oilChange * 12, 100) * 0.30;
        const equityScore = Math.min(equityAvg * 15, 100) * 0.25;
        const goldScore = Math.min(goldChange * 15, 100) * 0.20;
        const volScore = Math.min(volLevel * 2, 100) * 0.15;
        const dxyScore = Math.min(dxyChange * 20, 100) * 0.10;

        let risk = oilScore + equityScore + goldScore + volScore + dxyScore;

        // Boost if geo shock active
        if (MarketData.isGeoShockActive()) {
            risk = Math.min(risk * 1.5, 100);
        }

        return Math.min(Math.max(risk, 5), 100);
    }

    // ---- Chart Timeframe Controls ----
    function setupTimeframeControls() {
        document.querySelectorAll('.tf-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tf-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                // Timeframe affects how much history we show
                // In simulation mode this is cosmetic; with real data it would fetch different granularity
            });
        });
    }

    // ---- Alert Dismiss ----
    function setupAlertDismiss() {
        const dismissBtn = document.getElementById('alert-dismiss');
        if (dismissBtn) {
            dismissBtn.addEventListener('click', () => {
                document.getElementById('alert-banner').classList.add('hidden');
            });
        }

        const clearBtn = document.getElementById('clear-alerts');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                Alerts.clearAlerts();
            });
        }
    }

    // ---- Previous prices for flash detection ----
    let prevPrices = {};

    // ---- Main Update Loop ----
    function update() {
        // Advance simulation
        MarketData.tick();

        // Get all data
        const data = MarketData.getAll();
        const keys = MarketData.getInstrumentKeys();

        // Update UI components
        updateClock();
        updateMarketStatus();
        updateTickerStrip(data);
        updatePriceCards(data);
        updateVolMetrics(data);

        // Update charts
        const chartMap = {
            sp500: 'chart-sp500',
            nasdaq: 'chart-nasdaq',
            dow: 'chart-dow',
            oil: 'chart-oil',
            gold: 'chart-gold',
            dxy: 'chart-dxy'
        };

        for (const [key, chartId] of Object.entries(chartMap)) {
            Charts.updatePriceChart(chartId, MarketData.getHistory(key), data[key].change);
        }

        // Vol chart
        Charts.updateVolChart(MarketData.getVolHistory());

        // Risk gauge
        const risk = calculateRiskIndex(data);
        Charts.updateRiskGauge(risk);

        // Correlation matrix (update every 10th tick for performance)
        if (!window._tickCount) window._tickCount = 0;
        window._tickCount++;
        if (window._tickCount % 10 === 0) {
            Charts.renderCorrelationMatrix(MarketData.getCorrelations(), keys);
        }

        // Check alerts
        const newAlerts = Alerts.checkAlerts(data);
        if (newAlerts.length > 0) {
            Alerts.showBanner(newAlerts[0]);
            Alerts.renderAlertLog();
        }

        // Flash cards on price movement
        for (const key of keys) {
            if (prevPrices[key] !== undefined) {
                const diff = data[key].price - prevPrices[key];
                if (Math.abs(diff) > 0) {
                    flashPriceCard(key, diff > 0 ? 'up' : 'down');
                }
            }
            prevPrices[key] = data[key].price;
        }

        // News feed tick
        const newsEvent = NewsFeed.tick();
        if (newsEvent) {
            NewsFeed.render();
        }
    }

    // ---- Initialize ----
    function init() {
        MarketData.init();
        Charts.initAll();
        NewsFeed.init();
        NewsFeed.render();
        setupTimeframeControls();
        setupAlertDismiss();

        // Initial correlation matrix
        Charts.renderCorrelationMatrix(
            MarketData.getCorrelations(),
            MarketData.getInstrumentKeys()
        );

        // Initial render
        update();

        // Start the loop - 1 second interval
        setInterval(update, 1000);

        console.log('%c[Market Command Center] Dashboard initialized', 'color: #06b6d4; font-weight: bold');
        console.log('%cTracking: SPX, IXIC, DJI, WTI, XAU, DXY', 'color: #94a3b8');
        console.log('%cAlert threshold: ±2%', 'color: #f59e0b');
        console.log('%cGeopolitical context: US-Iran / Strait of Hormuz', 'color: #f97316');
    }

    // Boot when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
