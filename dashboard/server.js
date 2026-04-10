const express = require('express');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

// --- Symbol configuration ---
const SYMBOLS = {
  '^GSPC':    'S&P 500',
  '^IXIC':    'Nasdaq',
  '^DJI':     'Dow Jones',
  'CL=F':     'Crude Oil (WTI)',
  'DX-Y.NYB': 'US Dollar Index',
  'GC=F':     'Gold'
};

const SYMBOL_LIST = Object.keys(SYMBOLS).join(',');

// --- Yahoo Finance proxy: real-time quotes ---
app.get('/api/quotes', async (req, res) => {
  try {
    const url = `https://query1.finance.yahoo.com/v7/finance/quote?symbols=${encodeURIComponent(SYMBOL_LIST)}`;
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    if (!response.ok) throw new Error(`Yahoo API ${response.status}`);
    const data = await response.json();
    const quotes = (data.quoteResponse?.result || []).map(q => ({
      symbol:            q.symbol,
      name:              SYMBOLS[q.symbol] || q.shortName || q.symbol,
      price:             q.regularMarketPrice,
      change:            q.regularMarketChange,
      changePercent:     q.regularMarketChangePercent,
      previousClose:     q.regularMarketPreviousClose,
      open:              q.regularMarketOpen,
      dayHigh:           q.regularMarketDayHigh,
      dayLow:            q.regularMarketDayLow,
      volume:            q.regularMarketVolume,
      marketState:       q.marketState,
      lastUpdated:       q.regularMarketTime ? new Date(q.regularMarketTime * 1000).toISOString() : null
    }));
    res.json({ quotes, timestamp: Date.now() });
  } catch (err) {
    console.error('Quotes error:', err.message);
    res.status(502).json({ error: 'Failed to fetch quotes', message: err.message });
  }
});

// --- Yahoo Finance proxy: intraday chart data ---
app.get('/api/chart/:symbol', async (req, res) => {
  try {
    const symbol = req.params.symbol;
    const range = req.query.range || '1d';
    const interval = req.query.interval || '5m';
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?range=${range}&interval=${interval}&includePrePost=false`;
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    if (!response.ok) throw new Error(`Yahoo chart API ${response.status}`);
    const data = await response.json();
    const result = data.chart?.result?.[0];
    if (!result) throw new Error('No chart data returned');

    const timestamps = result.timestamp || [];
    const quote = result.indicators?.quote?.[0] || {};
    const meta = result.meta || {};

    const points = timestamps.map((ts, i) => ({
      time:   ts * 1000,
      open:   quote.open?.[i],
      high:   quote.high?.[i],
      low:    quote.low?.[i],
      close:  quote.close?.[i],
      volume: quote.volume?.[i]
    })).filter(p => p.close !== null && p.close !== undefined);

    res.json({
      symbol,
      name: SYMBOLS[symbol] || meta.shortName || symbol,
      currency: meta.currency,
      exchangeTimezoneName: meta.exchangeTimezoneName,
      previousClose: meta.chartPreviousClose || meta.previousClose,
      points,
      timestamp: Date.now()
    });
  } catch (err) {
    console.error(`Chart error (${req.params.symbol}):`, err.message);
    res.status(502).json({ error: 'Failed to fetch chart', message: err.message });
  }
});

// --- Volatility data (computed from chart data) ---
app.get('/api/volatility/:symbol', async (req, res) => {
  try {
    const symbol = req.params.symbol;
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}?range=1mo&interval=1d&includePrePost=false`;
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    if (!response.ok) throw new Error(`Yahoo API ${response.status}`);
    const data = await response.json();
    const result = data.chart?.result?.[0];
    if (!result) throw new Error('No data');

    const closes = (result.indicators?.quote?.[0]?.close || []).filter(c => c != null);
    if (closes.length < 2) throw new Error('Insufficient data');

    // Daily returns
    const returns = [];
    for (let i = 1; i < closes.length; i++) {
      returns.push((closes[i] - closes[i - 1]) / closes[i - 1]);
    }

    const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
    const variance = returns.reduce((a, r) => a + (r - mean) ** 2, 0) / (returns.length - 1);
    const dailyVol = Math.sqrt(variance);
    const annualizedVol = dailyVol * Math.sqrt(252);

    // Max drawdown over the period
    let peak = closes[0];
    let maxDrawdown = 0;
    for (const c of closes) {
      if (c > peak) peak = c;
      const dd = (peak - c) / peak;
      if (dd > maxDrawdown) maxDrawdown = dd;
    }

    // Average True Range (simplified using daily range)
    const highs = result.indicators?.quote?.[0]?.high || [];
    const lows = result.indicators?.quote?.[0]?.low || [];
    let atrSum = 0, atrCount = 0;
    for (let i = 0; i < highs.length; i++) {
      if (highs[i] != null && lows[i] != null) {
        atrSum += highs[i] - lows[i];
        atrCount++;
      }
    }
    const atr = atrCount > 0 ? atrSum / atrCount : 0;

    res.json({
      symbol,
      name: SYMBOLS[symbol] || symbol,
      dailyVolatility: (dailyVol * 100).toFixed(2),
      annualizedVolatility: (annualizedVol * 100).toFixed(2),
      maxDrawdown: (maxDrawdown * 100).toFixed(2),
      averageTrueRange: atr.toFixed(2),
      dataPoints: closes.length,
      timestamp: Date.now()
    });
  } catch (err) {
    console.error(`Volatility error (${req.params.symbol}):`, err.message);
    res.status(502).json({ error: 'Failed to compute volatility', message: err.message });
  }
});

// --- News proxy (Google News RSS parsed to JSON) ---
app.get('/api/news', async (req, res) => {
  try {
    const queries = [
      'US Iran ceasefire',
      'Strait of Hormuz',
      'Iran sanctions oil',
      'Middle East oil supply'
    ];
    const allItems = [];

    for (const q of queries) {
      try {
        const url = `https://news.google.com/rss/search?q=${encodeURIComponent(q)}&hl=en-US&gl=US&ceid=US:en`;
        const response = await fetch(url, {
          headers: { 'User-Agent': 'Mozilla/5.0' }
        });
        if (!response.ok) continue;
        const xml = await response.text();

        // Simple XML parsing for RSS items
        const items = xml.match(/<item>([\s\S]*?)<\/item>/g) || [];
        for (const item of items.slice(0, 5)) {
          const title = (item.match(/<title>([\s\S]*?)<\/title>/) || [])[1] || '';
          const link = (item.match(/<link>([\s\S]*?)<\/link>/) || [])[1] || '';
          const pubDate = (item.match(/<pubDate>([\s\S]*?)<\/pubDate>/) || [])[1] || '';
          const source = (item.match(/<source[^>]*>([\s\S]*?)<\/source>/) || [])[1] || '';
          allItems.push({
            title: title.replace(/<!\[CDATA\[|\]\]>/g, '').trim(),
            link: link.trim(),
            pubDate: pubDate.trim(),
            source: source.replace(/<!\[CDATA\[|\]\]>/g, '').trim(),
            query: q
          });
        }
      } catch { /* skip failed query */ }
    }

    // Deduplicate by title and sort by date
    const seen = new Set();
    const unique = allItems.filter(item => {
      const key = item.title.toLowerCase();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    }).sort((a, b) => new Date(b.pubDate) - new Date(a.pubDate)).slice(0, 20);

    res.json({ news: unique, timestamp: Date.now() });
  } catch (err) {
    console.error('News error:', err.message);
    res.status(502).json({ error: 'Failed to fetch news', message: err.message });
  }
});

// --- Fallback to index.html ---
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`\n  Geopolitical Market Dashboard`);
  console.log(`  =============================`);
  console.log(`  Running at http://localhost:${PORT}`);
  console.log(`  Tracking: ${Object.values(SYMBOLS).join(', ')}`);
  console.log(`  Press Ctrl+C to stop\n`);
});
