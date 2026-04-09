/**
 * Market Data Engine
 * Provides simulated real-time data with hooks for real API integration.
 * Instruments: S&P 500, NASDAQ, DOW, WTI Crude, Gold, DXY
 */

const MarketData = (() => {
    // Base prices (realistic starting points)
    const instruments = {
        sp500:  { name: 'S&P 500',    symbol: 'SPX',    price: 5218.00, open: 5218.00, prevClose: 5218.00, high: 5218.00, low: 5218.00, volatility: 0.0008, color: '#3b82f6' },
        nasdaq: { name: 'NASDAQ',     symbol: 'IXIC',   price: 16340.00, open: 16340.00, prevClose: 16340.00, high: 16340.00, low: 16340.00, volatility: 0.0012, color: '#8b5cf6' },
        dow:    { name: 'DOW JONES',  symbol: 'DJI',    price: 39128.00, open: 39128.00, prevClose: 39128.00, high: 39128.00, low: 39128.00, volatility: 0.0007, color: '#06b6d4' },
        oil:    { name: 'CRUDE OIL',  symbol: 'WTI',    price: 78.42,   open: 78.42,   prevClose: 78.42,   high: 78.42,   low: 78.42,   volatility: 0.0018, color: '#f97316' },
        gold:   { name: 'GOLD',       symbol: 'XAU',    price: 2342.50, open: 2342.50, prevClose: 2342.50, high: 2342.50, low: 2342.50, volatility: 0.0006, color: '#f59e0b' },
        dxy:    { name: 'US DOLLAR',  symbol: 'DXY',    price: 104.28,  open: 104.28,  prevClose: 104.28,  high: 104.28,  low: 104.28,  volatility: 0.0004, color: '#10b981' }
    };

    // History buffers for charts
    const history = {};
    const MAX_HISTORY = 300;

    // Correlation structure: oil up => gold up, dxy down, equities mixed
    const correlations = {
        sp500:  { sp500: 1.00, nasdaq: 0.92, dow: 0.95, oil: -0.35, gold: -0.20, dxy: 0.15 },
        nasdaq: { sp500: 0.92, nasdaq: 1.00, dow: 0.88, oil: -0.30, gold: -0.15, dxy: 0.10 },
        dow:    { sp500: 0.95, nasdaq: 0.88, dow: 1.00, oil: -0.32, gold: -0.18, dxy: 0.12 },
        oil:    { sp500: -0.35, nasdaq: -0.30, dow: -0.32, oil: 1.00, gold: 0.45, dxy: -0.55 },
        gold:   { sp500: -0.20, nasdaq: -0.15, dow: -0.18, oil: 0.45, gold: 1.00, dxy: -0.60 },
        dxy:    { sp500: 0.15, nasdaq: 0.10, dow: 0.12, oil: -0.55, gold: -0.60, dxy: 1.00 }
    };

    // Volatility history for vol chart
    const volHistory = [];
    const MAX_VOL_HISTORY = 120;

    // Geopolitical shock state
    let geoShockActive = false;
    let geoShockCountdown = 0;
    let geoShockMagnitude = 0;

    // Initialize history
    function init() {
        const now = Date.now();
        for (const key of Object.keys(instruments)) {
            history[key] = [];
            // Pre-fill with some historical data
            const inst = instruments[key];
            let p = inst.price * (1 - 0.005); // Start slightly lower
            for (let i = 60; i >= 0; i--) {
                const t = now - i * 1000;
                const change = (Math.random() - 0.48) * inst.volatility * p;
                p += change;
                history[key].push({ time: t, price: p });
            }
            inst.price = p;
            inst.open = history[key][0].price;
            inst.prevClose = inst.open * (1 + (Math.random() - 0.5) * 0.005);
            inst.high = Math.max(...history[key].map(h => h.price));
            inst.low = Math.min(...history[key].map(h => h.price));
        }
    }

    // Generate correlated random returns
    function generateReturns() {
        // Independent standard normals
        const z = {};
        for (const key of Object.keys(instruments)) {
            z[key] = randn();
        }

        // Apply rough correlation via Cholesky-like mixing
        const keys = Object.keys(instruments);
        const returns = {};

        for (const key of keys) {
            let r = 0;
            for (const other of keys) {
                const corr = correlations[key][other] || 0;
                r += corr * z[other];
            }
            // Normalize and scale
            r = (r / keys.length) * instruments[key].volatility;

            // Geopolitical shock amplification
            if (geoShockActive && geoShockCountdown > 0) {
                if (key === 'oil') {
                    r += geoShockMagnitude * 0.003; // Oil spikes up
                } else if (key === 'gold') {
                    r += geoShockMagnitude * 0.002; // Gold safe haven
                } else if (key === 'dxy') {
                    r += geoShockMagnitude * 0.001; // Dollar strengthens
                } else {
                    r -= geoShockMagnitude * 0.002; // Equities sell off
                }
                geoShockCountdown--;
                if (geoShockCountdown <= 0) {
                    geoShockActive = false;
                }
            }

            returns[key] = r;
        }

        return returns;
    }

    // Standard normal random variable (Box-Muller)
    function randn() {
        let u = 0, v = 0;
        while (u === 0) u = Math.random();
        while (v === 0) v = Math.random();
        return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    }

    // Tick: advance all prices by one step
    function tick() {
        const now = Date.now();
        const returns = generateReturns();

        for (const [key, inst] of Object.entries(instruments)) {
            const r = returns[key];
            const oldPrice = inst.price;
            inst.price = oldPrice * (1 + r);

            // Update high/low
            if (inst.price > inst.high) inst.high = inst.price;
            if (inst.price < inst.low) inst.low = inst.price;

            // Push history
            history[key].push({ time: now, price: inst.price });
            if (history[key].length > MAX_HISTORY) {
                history[key].shift();
            }
        }

        // Update aggregate volatility
        const avgVol = calculateRealizedVol('sp500', 30);
        volHistory.push({ time: now, vol: avgVol });
        if (volHistory.length > MAX_VOL_HISTORY) {
            volHistory.shift();
        }
    }

    // Calculate realized volatility (annualized, from last N ticks)
    function calculateRealizedVol(key, window) {
        const h = history[key];
        if (h.length < window + 1) return 0;

        const returns = [];
        for (let i = h.length - window; i < h.length; i++) {
            returns.push(Math.log(h[i].price / h[i - 1].price));
        }

        const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
        const variance = returns.reduce((a, b) => a + (b - mean) ** 2, 0) / (returns.length - 1);
        // Annualize (assuming 1-sec ticks, ~252 trading days * 6.5 hrs * 3600 sec)
        return Math.sqrt(variance) * Math.sqrt(252 * 6.5 * 3600) * 100;
    }

    // Calculate % change from previous close
    function getChange(key) {
        const inst = instruments[key];
        return ((inst.price - inst.prevClose) / inst.prevClose) * 100;
    }

    // Get absolute change
    function getAbsChange(key) {
        const inst = instruments[key];
        return inst.price - inst.prevClose;
    }

    // Trigger a geopolitical shock event
    function triggerGeoShock(magnitude) {
        geoShockActive = true;
        geoShockCountdown = 30 + Math.floor(Math.random() * 30); // 30-60 ticks
        geoShockMagnitude = magnitude; // 1 = moderate, 2 = severe, 3 = extreme
    }

    // Get all instrument data
    function getAll() {
        const data = {};
        for (const [key, inst] of Object.entries(instruments)) {
            data[key] = {
                ...inst,
                change: getChange(key),
                absChange: getAbsChange(key),
                realizedVol: calculateRealizedVol(key, 30)
            };
        }
        return data;
    }

    function getHistory(key) {
        return history[key] || [];
    }

    function getVolHistory() {
        return volHistory;
    }

    function getCorrelations() {
        return correlations;
    }

    function getInstrumentKeys() {
        return Object.keys(instruments);
    }

    function isGeoShockActive() {
        return geoShockActive;
    }

    return {
        init,
        tick,
        getAll,
        getHistory,
        getVolHistory,
        getCorrelations,
        getInstrumentKeys,
        getChange,
        getAbsChange,
        calculateRealizedVol,
        triggerGeoShock,
        isGeoShockActive
    };
})();
