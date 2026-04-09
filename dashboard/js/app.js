/* ========================================
   Main Application Controller
   Orchestrates all dashboard components
   ======================================== */

(function() {
    'use strict';

    // DOM references
    const clockEl = document.getElementById('clock');
    const lastUpdateEl = document.getElementById('last-update');
    const modeToggle = document.getElementById('mode-toggle');
    const connectionDot = document.getElementById('connection-dot');
    const connectionStatus = document.getElementById('connection-status');

    // Initialize all modules
    function init() {
        ChartManager.init();
        AlertSystem.init();
        NewsService.init();

        // Register data update handler
        MarketData.onUpdate(onDataUpdate);

        // Mode toggle
        modeToggle.addEventListener('change', () => {
            const mode = modeToggle.value;
            MarketData.setMode(mode);
            if (mode === 'api') {
                connectionStatus.textContent = 'API';
                connectionDot.className = 'dot dot-live';
            } else {
                connectionStatus.textContent = 'LIVE';
                connectionDot.className = 'dot dot-live';
            }
        });

        // Click ticker cards to switch chart
        document.querySelectorAll('.ticker-card').forEach(card => {
            card.addEventListener('click', () => {
                const symbol = card.dataset.symbol.toLowerCase();
                ChartManager.setAsset(symbol);
            });
        });

        // Start clock
        updateClock();
        setInterval(updateClock, 1000);

        // Start market data
        MarketData.start(3000);
    }

    // Called on each data tick
    function onDataUpdate(snapshot) {
        updateTickerCards(snapshot);
        updateVolatilityPanel(snapshot);
        updateCorrelationMatrix(snapshot);
        ChartManager.update(snapshot);
        AlertSystem.check(snapshot);
        updateLastUpdateTime();
    }

    function updateTickerCards(snapshot) {
        const assets = MarketData.getAssetConfig();
        const keys = MarketData.getAssetKeys();

        keys.forEach(key => {
            const data = snapshot.prices[key];
            const asset = assets[key];
            if (!data) return;

            const priceEl = document.getElementById(`price-${key}`);
            const changeEl = document.getElementById(`change-${key}`);
            const pctEl = document.getElementById(`pct-${key}`);
            const rangeEl = document.getElementById(`range-${key}`);

            if (!priceEl) return;

            // Detect price direction for flash
            const prevText = priceEl.textContent.replace(/,/g, '');
            const prevPrice = parseFloat(prevText);
            const newPrice = data.price;

            priceEl.textContent = formatPrice(newPrice, asset.decimals);

            // Direction class
            const dirClass = data.changePct >= 0 ? 'positive' : 'negative';
            priceEl.className = `ticker-price ${dirClass}`;

            const sign = data.change >= 0 ? '+' : '';
            changeEl.textContent = `${sign}${data.change.toFixed(asset.decimals)}`;
            changeEl.className = `change ${dirClass}`;

            pctEl.textContent = `(${sign}${data.changePct.toFixed(2)}%)`;
            pctEl.className = `change-pct ${dirClass}`;

            rangeEl.textContent = `${formatPrice(data.low, asset.decimals)} - ${formatPrice(data.high, asset.decimals)}`;

            // Flash card on price change
            if (!isNaN(prevPrice) && prevPrice !== newPrice) {
                const card = document.getElementById(`card-${key}`);
                if (card && !card.classList.contains('alert-active')) {
                    const flashClass = newPrice > prevPrice ? 'flash-green' : 'flash-red';
                    card.classList.add(flashClass);
                    setTimeout(() => card.classList.remove(flashClass), 600);
                }
            }
        });
    }

    function updateVolatilityPanel(snapshot) {
        const keys = MarketData.getAssetKeys();

        keys.forEach(key => {
            const vol = MarketData.getRealizedVolatility(key, 20);
            const barEl = document.getElementById(`volbar-${key}`);
            const numEl = document.getElementById(`volnum-${key}`);

            if (!barEl || !numEl) return;

            numEl.textContent = vol.toFixed(1) + '%';

            // Classify volatility level
            let pct, cls;
            if (vol < 15) { pct = (vol / 15) * 25; cls = 'vol-low'; }
            else if (vol < 25) { pct = 25 + ((vol - 15) / 10) * 25; cls = 'vol-medium'; }
            else if (vol < 40) { pct = 50 + ((vol - 25) / 15) * 25; cls = 'vol-high'; }
            else { pct = 75 + Math.min(((vol - 40) / 30) * 25, 25); cls = 'vol-extreme'; }

            barEl.style.width = Math.min(pct, 100) + '%';
            barEl.className = `vol-bar ${cls}`;

            // Color the number
            numEl.className = 'vol-number';
            if (vol >= 40) numEl.style.color = '#ef4444';
            else if (vol >= 25) numEl.style.color = '#f97316';
            else if (vol >= 15) numEl.style.color = '#f59e0b';
            else numEl.style.color = '#10b981';
        });
    }

    function updateCorrelationMatrix(snapshot) {
        const keys = MarketData.getAssetKeys();
        const labels = ['S&P', 'NDX', 'DOW', 'OIL', 'DXY', 'GOLD'];
        const body = document.getElementById('corr-body');

        let html = '';
        keys.forEach((key1, i) => {
            html += '<tr>';
            html += `<th>${labels[i]}</th>`;
            keys.forEach((key2, j) => {
                if (i === j) {
                    html += '<td class="corr-self">1.00</td>';
                } else {
                    const corr = MarketData.getCorrelation(key1, key2, 20);
                    const cls = Math.abs(corr) < 0.2 ? 'corr-neutral' :
                                corr > 0 ? 'corr-positive' : 'corr-negative';
                    html += `<td class="${cls}">${corr.toFixed(2)}</td>`;
                }
            });
            html += '</tr>';
        });

        body.innerHTML = html;
    }

    function updateClock() {
        const now = new Date();
        clockEl.textContent = now.toLocaleString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false,
            timeZone: 'America/New_York'
        }) + ' ET';
    }

    function updateLastUpdateTime() {
        const now = new Date();
        lastUpdateEl.textContent = now.toLocaleTimeString('en-US', { hour12: false });
    }

    function formatPrice(price, decimals) {
        return price.toLocaleString(undefined, {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }

    // Boot up when DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
