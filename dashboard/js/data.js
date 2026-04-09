/* ========================================
   Market Data Service
   Handles real-time data via simulation or API
   ======================================== */

const MarketData = (() => {
    // Asset configuration with realistic baseline prices
    const ASSETS = {
        sp500:  { name: 'S&P 500',       symbol: '^GSPC',    basePrice: 5250,  volatility: 0.012, decimals: 2 },
        nasdaq: { name: 'NASDAQ',         symbol: '^IXIC',    basePrice: 16400, volatility: 0.015, decimals: 2 },
        dow:    { name: 'Dow Jones',      symbol: '^DJI',     basePrice: 39200, volatility: 0.010, decimals: 2 },
        oil:    { name: 'Crude Oil WTI',  symbol: 'CL=F',     basePrice: 82.50, volatility: 0.025, decimals: 2 },
        dxy:    { name: 'US Dollar Index',symbol: 'DX-Y.NYB', basePrice: 104.20,volatility: 0.005, decimals: 3 },
        gold:   { name: 'Gold',           symbol: 'GC=F',     basePrice: 2340,  volatility: 0.010, decimals: 2 }
    };

    const ASSET_KEYS = Object.keys(ASSETS);

    // State
    let priceHistory = {};    // { assetKey: [{ time, price, open, high, low }] }
    let currentPrices = {};   // { assetKey: { price, change, changePct, open, high, low, prevClose } }
    let returnHistory = {};   // { assetKey: [returns] } for volatility calculation
    let listeners = [];
    let updateInterval = null;
    let mode = 'simulation';
    let tickCount = 0;

    // Geopolitical shock state - simulates crisis events
    let crisisMode = false;
    let crisisIntensity = 0;
    let crisisCooldown = 0;

    function init() {
        ASSET_KEYS.forEach(key => {
            const asset = ASSETS[key];
            const open = asset.basePrice * (1 + (Math.random() - 0.5) * 0.005);
            currentPrices[key] = {
                price: open,
                change: 0,
                changePct: 0,
                open: open,
                high: open,
                low: open,
                prevClose: asset.basePrice
            };
            priceHistory[key] = [{ time: Date.now(), price: open }];
            returnHistory[key] = [];
        });
    }

    // Geometric Brownian Motion with mean-reversion and crisis shocks
    function simulateTick() {
        tickCount++;

        // Random crisis events (every ~100 ticks on average)
        if (!crisisMode && Math.random() < 0.01) {
            crisisMode = true;
            crisisIntensity = 0.5 + Math.random() * 1.5; // 0.5x to 2x multiplier
            crisisCooldown = 15 + Math.floor(Math.random() * 30);
            // Notify news system of a crisis event
            if (typeof NewsService !== 'undefined') {
                NewsService.triggerCrisisEvent(crisisIntensity);
            }
        }

        if (crisisMode) {
            crisisCooldown--;
            if (crisisCooldown <= 0) {
                crisisMode = false;
                crisisIntensity = 0;
            }
        }

        const now = Date.now();

        ASSET_KEYS.forEach(key => {
            const asset = ASSETS[key];
            const curr = currentPrices[key];
            const prevPrice = curr.price;

            // Base random walk
            let vol = asset.volatility;
            let drift = 0;

            // Crisis effects: different assets react differently
            if (crisisMode) {
                const ci = crisisIntensity;
                if (key === 'oil') {
                    // Oil spikes up during Iran tensions
                    drift = 0.003 * ci;
                    vol *= (1 + ci * 1.5);
                } else if (key === 'gold') {
                    // Gold is safe haven, tends to rise
                    drift = 0.002 * ci;
                    vol *= (1 + ci * 0.8);
                } else if (key === 'dxy') {
                    // Dollar strengthens moderately
                    drift = 0.001 * ci;
                    vol *= (1 + ci * 0.5);
                } else {
                    // Equities drop during crisis
                    drift = -0.003 * ci;
                    vol *= (1 + ci * 1.2);
                }
            }

            // Mean reversion toward base price (weak)
            const deviation = (prevPrice - asset.basePrice) / asset.basePrice;
            drift -= deviation * 0.002;

            // Generate return with fat tails (mixture of normals)
            let z = randn();
            if (Math.random() < 0.05) z *= 2.5; // fat tail event

            const ret = drift + vol * z * Math.sqrt(1 / 390); // ~1 min in trading day
            const newPrice = prevPrice * (1 + ret);

            // Update state
            curr.price = Math.max(newPrice, asset.basePrice * 0.5); // floor
            curr.high = Math.max(curr.high, curr.price);
            curr.low = Math.min(curr.low, curr.price);
            curr.change = curr.price - curr.prevClose;
            curr.changePct = (curr.change / curr.prevClose) * 100;

            // Store history
            priceHistory[key].push({ time: now, price: curr.price });
            if (priceHistory[key].length > 2000) {
                priceHistory[key] = priceHistory[key].slice(-1500);
            }

            // Store returns for volatility
            returnHistory[key].push(ret);
            if (returnHistory[key].length > 100) {
                returnHistory[key] = returnHistory[key].slice(-100);
            }
        });

        notifyListeners();
    }

    // Box-Muller transform for normal random
    function randn() {
        let u = 0, v = 0;
        while (u === 0) u = Math.random();
        while (v === 0) v = Math.random();
        return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    }

    function start(intervalMs = 3000) {
        init();
        if (updateInterval) clearInterval(updateInterval);
        updateInterval = setInterval(() => {
            if (mode === 'simulation') {
                simulateTick();
            }
        }, intervalMs);
        // Immediate first tick
        simulateTick();
    }

    function stop() {
        if (updateInterval) {
            clearInterval(updateInterval);
            updateInterval = null;
        }
    }

    function setMode(newMode) {
        mode = newMode;
    }

    function onUpdate(callback) {
        listeners.push(callback);
    }

    function notifyListeners() {
        const snapshot = getSnapshot();
        listeners.forEach(cb => cb(snapshot));
    }

    function getSnapshot() {
        return {
            prices: JSON.parse(JSON.stringify(currentPrices)),
            history: priceHistory,
            returns: returnHistory,
            crisisMode,
            crisisIntensity,
            tickCount
        };
    }

    function getAssetConfig() {
        return ASSETS;
    }

    function getAssetKeys() {
        return ASSET_KEYS;
    }

    // Calculate realized volatility (annualized) from return history
    function getRealizedVolatility(key, periods = 20) {
        const rets = returnHistory[key];
        if (!rets || rets.length < 2) return 0;

        const slice = rets.slice(-periods);
        const mean = slice.reduce((a, b) => a + b, 0) / slice.length;
        const variance = slice.reduce((a, r) => a + (r - mean) ** 2, 0) / (slice.length - 1);
        const stdDev = Math.sqrt(variance);
        // Annualize (assuming ~390 ticks per day, 252 trading days)
        return stdDev * Math.sqrt(390 * 252) * 100;
    }

    // Calculate correlation between two assets
    function getCorrelation(key1, key2, periods = 20) {
        const r1 = returnHistory[key1];
        const r2 = returnHistory[key2];
        if (!r1 || !r2 || r1.length < periods || r2.length < periods) return 0;

        const s1 = r1.slice(-periods);
        const s2 = r2.slice(-periods);
        const n = Math.min(s1.length, s2.length);

        const mean1 = s1.slice(0, n).reduce((a, b) => a + b, 0) / n;
        const mean2 = s2.slice(0, n).reduce((a, b) => a + b, 0) / n;

        let cov = 0, var1 = 0, var2 = 0;
        for (let i = 0; i < n; i++) {
            const d1 = s1[i] - mean1;
            const d2 = s2[i] - mean2;
            cov += d1 * d2;
            var1 += d1 * d1;
            var2 += d2 * d2;
        }

        const denom = Math.sqrt(var1 * var2);
        return denom === 0 ? 0 : cov / denom;
    }

    return {
        init,
        start,
        stop,
        setMode,
        onUpdate,
        getSnapshot,
        getAssetConfig,
        getAssetKeys,
        getRealizedVolatility,
        getCorrelation,
        ASSETS
    };
})();
