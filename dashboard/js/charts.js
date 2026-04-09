/* ========================================
   Chart Manager
   Real-time Chart.js integration
   ======================================== */

const ChartManager = (() => {
    let mainChart = null;
    let currentAsset = 'sp500';
    let currentTimeframe = '1m';
    let chartCanvas = null;

    const COLORS = {
        sp500:  { line: '#3b82f6', fill: 'rgba(59, 130, 246, 0.08)' },
        nasdaq: { line: '#8b5cf6', fill: 'rgba(139, 92, 246, 0.08)' },
        dow:    { line: '#06b6d4', fill: 'rgba(6, 182, 212, 0.08)' },
        oil:    { line: '#f97316', fill: 'rgba(249, 115, 22, 0.08)' },
        dxy:    { line: '#10b981', fill: 'rgba(16, 185, 129, 0.08)' },
        gold:   { line: '#fbbf24', fill: 'rgba(251, 191, 36, 0.08)' }
    };

    const TIMEFRAME_POINTS = {
        '1m': 60,
        '5m': 100,
        '15m': 200,
        '1h': 500,
        '1d': 1500
    };

    function init() {
        chartCanvas = document.getElementById('main-chart');
        createChart();
        setupTabListeners();
    }

    function createChart() {
        if (mainChart) mainChart.destroy();

        const ctx = chartCanvas.getContext('2d');
        const config = currentAsset === 'overlay' ? getOverlayConfig() : getSingleConfig();
        mainChart = new Chart(ctx, config);
    }

    function getSingleConfig() {
        const color = COLORS[currentAsset];
        const assets = MarketData.getAssetConfig();
        const asset = assets[currentAsset];

        return {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: asset.name,
                    data: [],
                    borderColor: color.line,
                    backgroundColor: color.fill,
                    borderWidth: 2,
                    pointRadius: 0,
                    pointHitRadius: 8,
                    fill: true,
                    tension: 0.3
                }]
            },
            options: getChartOptions(asset.name, false)
        };
    }

    function getOverlayConfig() {
        const assets = MarketData.getAssetConfig();
        const keys = MarketData.getAssetKeys();

        const datasets = keys.map(key => ({
            label: assets[key].name,
            data: [],
            borderColor: COLORS[key].line,
            backgroundColor: 'transparent',
            borderWidth: 1.5,
            pointRadius: 0,
            fill: false,
            tension: 0.3,
            yAxisID: 'y'
        }));

        return {
            type: 'line',
            data: { labels: [], datasets },
            options: getChartOptions('Normalized % Change (All Assets)', true)
        };
    }

    function getChartOptions(title, isNormalized) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 300 },
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    display: currentAsset === 'overlay',
                    position: 'top',
                    labels: {
                        color: '#9ca3af',
                        font: { size: 11 },
                        boxWidth: 12,
                        padding: 12
                    }
                },
                title: {
                    display: true,
                    text: title,
                    color: '#e5e7eb',
                    font: { size: 13, weight: '600' },
                    padding: { bottom: 10 }
                },
                tooltip: {
                    backgroundColor: '#1a2236',
                    titleColor: '#e5e7eb',
                    bodyColor: '#9ca3af',
                    borderColor: '#2a3a5c',
                    borderWidth: 1,
                    padding: 10,
                    displayColors: true,
                    callbacks: {
                        label: function(ctx) {
                            const val = ctx.parsed.y;
                            if (isNormalized) return `${ctx.dataset.label}: ${val.toFixed(2)}%`;
                            return `${ctx.dataset.label}: ${val.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    ticks: {
                        color: '#6b7280',
                        font: { size: 10 },
                        maxTicksLimit: 10,
                        maxRotation: 0
                    },
                    grid: { color: '#1e293b', lineWidth: 0.5 }
                },
                y: {
                    display: true,
                    position: 'right',
                    ticks: {
                        color: '#6b7280',
                        font: { size: 10, family: "'SF Mono', 'Consolas', monospace" },
                        callback: function(value) {
                            if (isNormalized) return value.toFixed(1) + '%';
                            return value.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 });
                        }
                    },
                    grid: { color: '#1e293b', lineWidth: 0.5 }
                }
            }
        };
    }

    function update(snapshot) {
        if (!mainChart) return;

        const maxPoints = TIMEFRAME_POINTS[currentTimeframe] || 60;

        if (currentAsset === 'overlay') {
            updateOverlayChart(snapshot, maxPoints);
        } else {
            updateSingleChart(snapshot, maxPoints);
        }

        mainChart.update('none');
    }

    function updateSingleChart(snapshot, maxPoints) {
        const history = snapshot.history[currentAsset];
        if (!history || history.length === 0) return;

        const sliced = history.slice(-maxPoints);
        mainChart.data.labels = sliced.map(p => formatTime(p.time));
        mainChart.data.datasets[0].data = sliced.map(p => p.price);

        // Color line based on day change
        const priceData = snapshot.prices[currentAsset];
        if (priceData) {
            const color = priceData.changePct >= 0 ? '#10b981' : '#ef4444';
            const fill = priceData.changePct >= 0 ? 'rgba(16, 185, 129, 0.08)' : 'rgba(239, 68, 68, 0.08)';
            mainChart.data.datasets[0].borderColor = color;
            mainChart.data.datasets[0].backgroundColor = fill;
        }
    }

    function updateOverlayChart(snapshot, maxPoints) {
        const keys = MarketData.getAssetKeys();
        const minLen = Math.min(...keys.map(k => (snapshot.history[k] || []).length));
        if (minLen < 2) return;

        const len = Math.min(minLen, maxPoints);

        // Normalize to % change from first visible point
        keys.forEach((key, idx) => {
            const history = snapshot.history[key].slice(-len);
            const basePrice = history[0].price;
            mainChart.data.datasets[idx].data = history.map(p =>
                ((p.price - basePrice) / basePrice) * 100
            );
        });

        const firstHistory = snapshot.history[keys[0]].slice(-len);
        mainChart.data.labels = firstHistory.map(p => formatTime(p.time));
    }

    function formatTime(timestamp) {
        const d = new Date(timestamp);
        return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    }

    function setupTabListeners() {
        document.querySelectorAll('.chart-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.chart-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentAsset = tab.dataset.asset;
                createChart();
            });
        });

        document.querySelectorAll('.tf-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tf-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                currentTimeframe = tab.dataset.tf;
            });
        });
    }

    function setAsset(assetKey) {
        currentAsset = assetKey;
        document.querySelectorAll('.chart-tab').forEach(t => {
            t.classList.toggle('active', t.dataset.asset === assetKey);
        });
        createChart();
    }

    return { init, update, setAsset };
})();
