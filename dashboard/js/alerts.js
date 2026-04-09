/**
 * Alert System
 * Monitors price movements and triggers alerts for >2% moves.
 * Tracks alert history and displays banner notifications.
 */

const Alerts = (() => {
    const THRESHOLD = 2.0; // percent
    const alerts = [];
    const MAX_ALERTS = 50;
    const triggeredThisSession = new Set();
    let audioEnabled = true;

    // Check all instruments for threshold breaches
    function checkAlerts(marketData) {
        const newAlerts = [];

        for (const [key, data] of Object.entries(marketData)) {
            const changeAbs = Math.abs(data.change);
            const direction = data.change >= 0 ? 'up' : 'down';

            // Alert tiers
            const tiers = [
                { threshold: 5.0, level: 'critical', label: 'EXTREME MOVE' },
                { threshold: 3.0, level: 'critical', label: 'MAJOR MOVE' },
                { threshold: 2.0, level: 'warning', label: 'SIGNIFICANT MOVE' }
            ];

            for (const tier of tiers) {
                if (changeAbs >= tier.threshold) {
                    const alertKey = `${key}-${tier.label}-${direction}`;

                    // Deduplicate: only fire once per direction per tier per session
                    // Reset if price comes back and crosses again
                    if (!triggeredThisSession.has(alertKey)) {
                        triggeredThisSession.add(alertKey);

                        const alert = {
                            id: Date.now() + Math.random(),
                            time: new Date(),
                            instrument: data.name,
                            symbol: data.symbol,
                            level: tier.level,
                            label: tier.label,
                            change: data.change,
                            price: data.price,
                            direction: direction,
                            message: `${data.symbol} ${tier.label}: ${direction === 'up' ? '+' : ''}${data.change.toFixed(2)}% (${formatPrice(data.price, key)})`
                        };

                        alerts.unshift(alert);
                        newAlerts.push(alert);

                        if (alerts.length > MAX_ALERTS) {
                            alerts.pop();
                        }
                    }
                    break; // Only trigger highest tier
                }
            }

            // Clear triggers when price returns below threshold
            if (changeAbs < THRESHOLD) {
                for (const dir of ['up', 'down']) {
                    triggeredThisSession.delete(`${key}-SIGNIFICANT MOVE-${dir}`);
                    triggeredThisSession.delete(`${key}-MAJOR MOVE-${dir}`);
                    triggeredThisSession.delete(`${key}-EXTREME MOVE-${dir}`);
                }
            }
        }

        return newAlerts;
    }

    // Show banner alert at top of page
    function showBanner(alert) {
        const banner = document.getElementById('alert-banner');
        const text = document.getElementById('alert-text');
        if (!banner || !text) return;

        const arrow = alert.direction === 'up' ? '\u25B2' : '\u25BC';
        text.innerHTML = `<strong>${alert.label}</strong> &mdash; ${alert.symbol} ${arrow} ${alert.change >= 0 ? '+' : ''}${alert.change.toFixed(2)}% at ${formatPrice(alert.price, '')} &mdash; Geopolitical risk event may be driving this move`;

        banner.classList.remove('hidden');

        // Auto-hide after 10 seconds
        setTimeout(() => {
            banner.classList.add('hidden');
        }, 10000);
    }

    // Render alert log
    function renderAlertLog() {
        const container = document.getElementById('alert-log');
        if (!container) return;

        if (alerts.length === 0) {
            container.innerHTML = '<div class="alert-empty">No alerts triggered</div>';
            return;
        }

        container.innerHTML = alerts.map(a => {
            const arrow = a.direction === 'up' ? '\u25B2' : '\u25BC';
            const timeStr = a.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            return `
                <div class="alert-entry ${a.level}">
                    <span class="alert-time">${timeStr}</span>
                    <span class="alert-message">
                        <strong>${a.symbol}</strong> ${arrow} ${a.change >= 0 ? '+' : ''}${a.change.toFixed(2)}%
                        &mdash; ${a.label}
                    </span>
                </div>
            `;
        }).join('');
    }

    function clearAlerts() {
        alerts.length = 0;
        triggeredThisSession.clear();
        renderAlertLog();
    }

    function getAlerts() {
        return alerts;
    }

    function formatPrice(value, key) {
        if (typeof value !== 'number') return value;
        if (value > 10000) return '$' + value.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
        if (value > 100) return '$' + value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        return '$' + value.toFixed(2);
    }

    return {
        checkAlerts,
        showBanner,
        renderAlertLog,
        clearAlerts,
        getAlerts
    };
})();
