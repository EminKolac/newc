/* ========================================
   Alert System
   Monitors for significant price moves
   ======================================== */

const AlertSystem = (() => {
    let alertCount = 0;
    let alertLog = [];
    let lastAlertTime = {};   // { assetKey: timestamp } to prevent spam
    let threshold = 2.0;      // default 2%
    let soundEnabled = true;
    let audioCtx = null;

    const ALERT_COOLDOWN = 30000; // 30 seconds between alerts for same asset

    function init() {
        // Threshold control
        const thresholdInput = document.getElementById('alert-threshold');
        thresholdInput.addEventListener('change', () => {
            threshold = parseFloat(thresholdInput.value) || 2.0;
        });

        // Sound toggle
        const soundToggle = document.getElementById('alert-sound');
        soundToggle.addEventListener('change', () => {
            soundEnabled = soundToggle.checked;
        });

        // Dismiss banner
        document.getElementById('alert-dismiss').addEventListener('click', () => {
            document.getElementById('alert-banner').classList.add('hidden');
        });

        // Initialize audio context on first user interaction
        document.addEventListener('click', () => {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
        }, { once: true });
    }

    function check(snapshot) {
        const now = Date.now();
        const keys = MarketData.getAssetKeys();
        const assets = MarketData.getAssetConfig();

        keys.forEach(key => {
            const data = snapshot.prices[key];
            if (!data) return;

            const pctChange = Math.abs(data.changePct);
            if (pctChange >= threshold) {
                // Check cooldown
                if (lastAlertTime[key] && (now - lastAlertTime[key]) < ALERT_COOLDOWN) return;
                lastAlertTime[key] = now;

                const direction = data.changePct > 0 ? 'UP' : 'DOWN';
                const isCritical = pctChange >= threshold * 1.5;
                const asset = assets[key];

                const alert = {
                    time: now,
                    asset: key,
                    assetName: asset.name,
                    price: data.price,
                    changePct: data.changePct,
                    direction,
                    isCritical,
                    message: `${asset.name} ${direction} ${Math.abs(data.changePct).toFixed(2)}%`,
                    detail: `Price: ${data.price.toLocaleString(undefined, { minimumFractionDigits: asset.decimals })} | Change: ${data.change >= 0 ? '+' : ''}${data.change.toFixed(asset.decimals)}`
                };

                addAlert(alert);

                // Show banner for critical alerts
                if (isCritical) {
                    showBanner(alert);
                }

                // Flash the ticker card
                flashCard(key, direction);

                // Play sound
                if (soundEnabled) playAlertSound(isCritical);
            }
        });

        // Also check for rapid intraday moves using recent price history
        checkRapidMoves(snapshot, now);
    }

    function checkRapidMoves(snapshot, now) {
        const keys = MarketData.getAssetKeys();
        const assets = MarketData.getAssetConfig();

        keys.forEach(key => {
            const history = snapshot.history[key];
            if (!history || history.length < 10) return;

            // Check 10-period move
            const recent = history[history.length - 1].price;
            const past = history[Math.max(0, history.length - 10)].price;
            const rapidPct = ((recent - past) / past) * 100;

            if (Math.abs(rapidPct) >= threshold * 0.75) {
                const cooldownKey = key + '_rapid';
                if (lastAlertTime[cooldownKey] && (now - lastAlertTime[cooldownKey]) < ALERT_COOLDOWN * 2) return;
                lastAlertTime[cooldownKey] = now;

                const direction = rapidPct > 0 ? 'UP' : 'DOWN';
                const asset = assets[key];

                addAlert({
                    time: now,
                    asset: key,
                    assetName: asset.name,
                    price: snapshot.prices[key].price,
                    changePct: rapidPct,
                    direction,
                    isCritical: false,
                    message: `RAPID MOVE: ${asset.name} ${direction} ${Math.abs(rapidPct).toFixed(2)}% in 10 ticks`,
                    detail: `Short-term momentum alert | Possible geopolitical catalyst`
                });
            }
        });
    }

    function addAlert(alert) {
        alertLog.unshift(alert);
        if (alertLog.length > 50) alertLog.pop();

        alertCount++;
        document.getElementById('alert-count').textContent = alertCount;

        renderAlertLog();
    }

    function renderAlertLog() {
        const container = document.getElementById('alert-log');
        container.innerHTML = alertLog.map(a => {
            const timeStr = new Date(a.time).toLocaleTimeString('en-US', { hour12: false });
            const cls = a.isCritical ? 'alert-critical' : 'alert-warning';
            return `
                <div class="alert-entry ${cls}">
                    <div class="alert-entry-time">${timeStr}</div>
                    <div class="alert-entry-message">${a.message}</div>
                    <div class="alert-entry-detail">${a.detail}</div>
                </div>
            `;
        }).join('');
    }

    function showBanner(alert) {
        const banner = document.getElementById('alert-banner');
        const text = document.getElementById('alert-text');
        text.textContent = `CRITICAL: ${alert.message} - ${alert.detail}`;
        banner.classList.remove('hidden');

        // Auto-dismiss after 10s
        setTimeout(() => {
            banner.classList.add('hidden');
        }, 10000);
    }

    function flashCard(assetKey, direction) {
        const card = document.getElementById(`card-${assetKey}`);
        if (!card) return;

        card.classList.add('alert-active');
        card.classList.add(direction === 'UP' ? 'flash-green' : 'flash-red');

        setTimeout(() => {
            card.classList.remove('flash-green', 'flash-red');
        }, 600);

        setTimeout(() => {
            card.classList.remove('alert-active');
        }, 5000);
    }

    function playAlertSound(isCritical) {
        if (!audioCtx) return;
        try {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain);
            gain.connect(audioCtx.destination);

            osc.frequency.value = isCritical ? 880 : 660;
            osc.type = 'sine';
            gain.gain.value = 0.1;
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);

            osc.start();
            osc.stop(audioCtx.currentTime + 0.3);

            if (isCritical) {
                // Double beep for critical
                setTimeout(() => {
                    const osc2 = audioCtx.createOscillator();
                    const gain2 = audioCtx.createGain();
                    osc2.connect(gain2);
                    gain2.connect(audioCtx.destination);
                    osc2.frequency.value = 1100;
                    osc2.type = 'sine';
                    gain2.gain.value = 0.1;
                    gain2.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
                    osc2.start();
                    osc2.stop(audioCtx.currentTime + 0.3);
                }, 200);
            }
        } catch (e) {
            // Audio not available
        }
    }

    return { init, check };
})();
