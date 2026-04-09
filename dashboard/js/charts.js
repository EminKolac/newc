/**
 * Charts Module
 * Manages all Chart.js instances for price charts, volatility, correlation, and risk gauge.
 */

const Charts = (() => {
    const charts = {};
    const chartConfigs = {};

    // Common chart defaults
    const commonDefaults = {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 0 },
        plugins: {
            legend: { display: false },
            tooltip: {
                mode: 'index',
                intersect: false,
                backgroundColor: '#1a2332',
                titleColor: '#e2e8f0',
                bodyColor: '#94a3b8',
                borderColor: '#2a3548',
                borderWidth: 1,
                titleFont: { size: 11 },
                bodyFont: { family: "'Courier New', monospace", size: 11 },
                padding: 8,
                displayColors: false,
                callbacks: {
                    label: function(ctx) {
                        return formatPrice(ctx.parsed.y, ctx.dataset.label);
                    }
                }
            }
        },
        scales: {
            x: {
                display: true,
                grid: { color: 'rgba(42, 53, 72, 0.5)', drawBorder: false },
                ticks: {
                    color: '#64748b',
                    font: { size: 9, family: "'Courier New', monospace" },
                    maxTicksLimit: 6,
                    callback: function(val, idx) {
                        const label = this.getLabelForValue(val);
                        if (!label) return '';
                        const d = new Date(label);
                        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
                    }
                }
            },
            y: {
                display: true,
                position: 'right',
                grid: { color: 'rgba(42, 53, 72, 0.3)', drawBorder: false },
                ticks: {
                    color: '#64748b',
                    font: { size: 9, family: "'Courier New', monospace" },
                    maxTicksLimit: 5
                }
            }
        },
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
        }
    };

    function formatPrice(value, label) {
        if (typeof value !== 'number') return value;
        if (value > 10000) return value.toFixed(0);
        if (value > 100) return value.toFixed(2);
        return value.toFixed(2);
    }

    // Create a price line chart
    function createPriceChart(canvasId, color, label) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 180);
        gradient.addColorStop(0, color + '40');
        gradient.addColorStop(1, color + '00');

        const config = {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: label,
                    data: [],
                    borderColor: color,
                    backgroundColor: gradient,
                    borderWidth: 1.5,
                    fill: true,
                    pointRadius: 0,
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: color,
                    tension: 0.3
                }]
            },
            options: JSON.parse(JSON.stringify(commonDefaults))
        };

        charts[canvasId] = new Chart(ctx, config);
        return charts[canvasId];
    }

    // Update a price chart with new data
    function updatePriceChart(canvasId, historyData, changePercent) {
        const chart = charts[canvasId];
        if (!chart || !historyData.length) return;

        const labels = historyData.map(d => d.time);
        const data = historyData.map(d => d.price);

        // Dynamic color based on direction
        const isUp = changePercent >= 0;
        const baseColor = isUp ? '#10b981' : '#ef4444';

        const ctx = chart.canvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 180);
        gradient.addColorStop(0, baseColor + '30');
        gradient.addColorStop(1, baseColor + '00');

        chart.data.labels = labels;
        chart.data.datasets[0].data = data;
        chart.data.datasets[0].borderColor = baseColor;
        chart.data.datasets[0].backgroundColor = gradient;

        chart.update('none');
    }

    // Create the volatility chart
    function createVolChart() {
        const ctx = document.getElementById('chart-vol');
        if (!ctx) return null;

        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 120);
        gradient.addColorStop(0, '#f59e0b40');
        gradient.addColorStop(1, '#f59e0b00');

        charts['chart-vol'] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Realized Vol',
                    data: [],
                    borderColor: '#f59e0b',
                    backgroundColor: gradient,
                    borderWidth: 1.5,
                    fill: true,
                    pointRadius: 0,
                    tension: 0.4
                }]
            },
            options: {
                ...JSON.parse(JSON.stringify(commonDefaults)),
                scales: {
                    ...JSON.parse(JSON.stringify(commonDefaults.scales)),
                    y: {
                        ...JSON.parse(JSON.stringify(commonDefaults.scales.y)),
                        ticks: {
                            ...JSON.parse(JSON.stringify(commonDefaults.scales.y.ticks)),
                            callback: (v) => v.toFixed(1) + '%'
                        }
                    }
                }
            }
        });
    }

    function updateVolChart(volData) {
        const chart = charts['chart-vol'];
        if (!chart || !volData.length) return;

        chart.data.labels = volData.map(d => d.time);
        chart.data.datasets[0].data = volData.map(d => d.vol);

        // Color shift based on vol level
        const lastVol = volData[volData.length - 1].vol;
        let color = '#10b981'; // low vol
        if (lastVol > 25) color = '#f59e0b';
        if (lastVol > 40) color = '#ef4444';

        const ctx = chart.canvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 120);
        gradient.addColorStop(0, color + '40');
        gradient.addColorStop(1, color + '00');

        chart.data.datasets[0].borderColor = color;
        chart.data.datasets[0].backgroundColor = gradient;

        chart.update('none');
    }

    // Create risk gauge (semi-circle)
    function createRiskGauge() {
        const ctx = document.getElementById('risk-gauge');
        if (!ctx) return;

        charts['risk-gauge'] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Risk', 'Remaining'],
                datasets: [{
                    data: [35, 65],
                    backgroundColor: ['#f59e0b', 'rgba(42, 53, 72, 0.3)'],
                    borderWidth: 0,
                    circumference: 180,
                    rotation: 270
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: { duration: 500 },
                cutout: '75%',
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }

    function updateRiskGauge(riskLevel) {
        const chart = charts['risk-gauge'];
        if (!chart) return;

        // riskLevel 0-100
        const clamped = Math.max(0, Math.min(100, riskLevel));
        chart.data.datasets[0].data = [clamped, 100 - clamped];

        let color = '#10b981';
        let label = 'LOW';
        if (clamped > 30) { color = '#3b82f6'; label = 'MODERATE'; }
        if (clamped > 50) { color = '#f59e0b'; label = 'ELEVATED'; }
        if (clamped > 70) { color = '#f97316'; label = 'HIGH'; }
        if (clamped > 85) { color = '#ef4444'; label = 'EXTREME'; }

        chart.data.datasets[0].backgroundColor[0] = color;
        chart.update();

        const riskLabel = document.getElementById('risk-label');
        if (riskLabel) {
            riskLabel.textContent = label;
            riskLabel.style.color = color;
        }
    }

    // Render correlation matrix
    function renderCorrelationMatrix(correlations, keys) {
        const container = document.getElementById('correlation-matrix');
        if (!container) return;

        const labels = { sp500: 'SPX', nasdaq: 'NDX', dow: 'DJI', oil: 'WTI', gold: 'XAU', dxy: 'DXY' };

        let html = '<table><tr><th></th>';
        for (const k of keys) {
            html += `<th>${labels[k]}</th>`;
        }
        html += '</tr>';

        for (const row of keys) {
            html += `<tr><th>${labels[row]}</th>`;
            for (const col of keys) {
                const val = correlations[row][col];
                const color = getCorrelationColor(val);
                html += `<td style="background:${color};color:${Math.abs(val) > 0.5 ? '#fff' : '#94a3b8'}">${val.toFixed(2)}</td>`;
            }
            html += '</tr>';
        }
        html += '</table>';

        container.innerHTML = html;
    }

    function getCorrelationColor(val) {
        const abs = Math.abs(val);
        if (val > 0) {
            const r = Math.floor(16 + (1 - abs) * 10);
            const g = Math.floor(185 * abs);
            const b = Math.floor(129 * abs);
            return `rgba(${r}, ${g}, ${b}, ${abs * 0.5 + 0.05})`;
        } else {
            const r = Math.floor(239 * abs);
            const g = Math.floor(68 * abs);
            const b = Math.floor(68 * abs);
            return `rgba(${r}, ${g}, ${b}, ${abs * 0.5 + 0.05})`;
        }
    }

    // Initialize all charts
    function initAll() {
        createPriceChart('chart-sp500', '#3b82f6', 'S&P 500');
        createPriceChart('chart-nasdaq', '#8b5cf6', 'NASDAQ');
        createPriceChart('chart-dow', '#06b6d4', 'DOW');
        createPriceChart('chart-oil', '#f97316', 'WTI Crude');
        createPriceChart('chart-gold', '#f59e0b', 'Gold');
        createPriceChart('chart-dxy', '#10b981', 'DXY');
        createVolChart();
        createRiskGauge();
    }

    return {
        initAll,
        updatePriceChart,
        updateVolChart,
        updateRiskGauge,
        renderCorrelationMatrix
    };
})();
