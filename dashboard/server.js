import express from 'express';
import path from 'path';
import https from 'https';
import { fileURLToPath } from 'url';
import YahooFinance from 'yahoo-finance2';

const yf = new YahooFinance();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'public')));

// Tracked instruments
const SYMBOLS = {
  '^GSPC':    { name: 'S&P 500',        category: 'index' },
  '^IXIC':    { name: 'Nasdaq Composite', category: 'index' },
  '^DJI':     { name: 'Dow Jones',       category: 'index' },
  'CL=F':     { name: 'Crude Oil (WTI)', category: 'commodity' },
  'DX-Y.NYB': { name: 'US Dollar Index', category: 'currency' },
  'GC=F':     { name: 'Gold',            category: 'commodity' },
};

// In-memory store for latest quotes and history
let latestQuotes = {};
let priceHistory = {};
let alerts = [];
let sseClients = [];

// SSE endpoint for real-time streaming
app.get('/api/stream', (req, res) => {
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    Connection: 'keep-alive',
  });
  res.write('data: {"type":"connected"}\n\n');
  sseClients.push(res);
  req.on('close', () => {
    sseClients = sseClients.filter((c) => c !== res);
  });
});

function broadcast(data) {
  const msg = `data: ${JSON.stringify(data)}\n\n`;
  sseClients.forEach((c) => c.write(msg));
}

// Fetch current quotes for all symbols
async function fetchQuotes() {
  const results = {};
  const symbolKeys = Object.keys(SYMBOLS);

  for (const symbol of symbolKeys) {
    try {
      const quote = await yf.quote(symbol);
      const prev = quote.regularMarketPreviousClose || quote.regularMarketOpen || 0;
      const current = quote.regularMarketPrice || 0;
      const change = current - prev;
      const changePct = prev ? ((change / prev) * 100) : 0;
      const dayHigh = quote.regularMarketDayHigh || current;
      const dayLow = quote.regularMarketDayLow || current;
      const dayRange = prev ? (((dayHigh - dayLow) / prev) * 100) : 0;

      results[symbol] = {
        symbol,
        name: SYMBOLS[symbol].name,
        category: SYMBOLS[symbol].category,
        price: current,
        previousClose: prev,
        change,
        changePct,
        dayHigh,
        dayLow,
        dayRange,
        volume: quote.regularMarketVolume || 0,
        marketState: quote.marketState || 'CLOSED',
        timestamp: Date.now(),
      };

      // Track price history for sparklines (keep last 100 data points)
      if (!priceHistory[symbol]) priceHistory[symbol] = [];
      priceHistory[symbol].push({ price: current, time: Date.now() });
      if (priceHistory[symbol].length > 100) priceHistory[symbol].shift();

      // Check for 2%+ move alert
      if (Math.abs(changePct) >= 2) {
        const alertObj = {
          id: `${symbol}-${Date.now()}`,
          symbol,
          name: SYMBOLS[symbol].name,
          changePct,
          price: current,
          direction: changePct > 0 ? 'up' : 'down',
          message: `${SYMBOLS[symbol].name} moved ${changePct > 0 ? '+' : ''}${changePct.toFixed(2)}% — potential geopolitical catalyst (US-Iran / Strait of Hormuz)`,
          timestamp: Date.now(),
        };
        // Avoid duplicate alerts within 5 minutes
        const isDuplicate = alerts.some(
          (a) => a.symbol === symbol && Date.now() - a.timestamp < 300000
        );
        if (!isDuplicate) {
          alerts.unshift(alertObj);
          if (alerts.length > 50) alerts.pop();
          broadcast({ type: 'alert', data: alertObj });
        }
      }
    } catch (err) {
      console.error(`Error fetching ${symbol}:`, err.message);
    }
  }

  latestQuotes = results;
  broadcast({ type: 'quotes', data: results });
}

// Fetch historical chart data via Yahoo Finance v8 chart API
function httpsGet(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => resolve(data));
      res.on('error', reject);
    }).on('error', reject);
  });
}

async function fetchHistory(symbol, range = '5d', interval = '15m') {
  try {
    const encoded = encodeURIComponent(symbol);
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encoded}?range=${range}&interval=${interval}&includePrePost=false`;
    const raw = await httpsGet(url);
    const json = JSON.parse(raw);
    const result = json?.chart?.result?.[0];
    if (!result) return [];
    const timestamps = result.timestamp || [];
    const ohlcv = result.indicators?.quote?.[0] || {};
    return timestamps.map((t, i) => ({
      time: t * 1000,
      open: ohlcv.open?.[i],
      high: ohlcv.high?.[i],
      low: ohlcv.low?.[i],
      close: ohlcv.close?.[i],
      volume: ohlcv.volume?.[i],
    })).filter((q) => q.close != null);
  } catch (err) {
    console.error(`Error fetching history for ${symbol}:`, err.message);
  }
  return [];
}

// Calculate volatility metrics from historical data
function calcVolatility(history) {
  if (!history || history.length < 2) return { atr: 0, stdDev: 0, avgRange: 0 };
  const returns = [];
  const ranges = [];
  for (let i = 1; i < history.length; i++) {
    if (history[i].close && history[i - 1].close) {
      returns.push(Math.log(history[i].close / history[i - 1].close));
    }
    if (history[i].high && history[i].low) {
      ranges.push(history[i].high - history[i].low);
    }
  }
  const mean = returns.reduce((a, b) => a + b, 0) / returns.length;
  const variance = returns.reduce((a, b) => a + (b - mean) ** 2, 0) / returns.length;
  const stdDev = Math.sqrt(variance) * 100;
  const atr = ranges.length ? ranges.slice(-14).reduce((a, b) => a + b, 0) / Math.min(ranges.length, 14) : 0;
  const avgRange = ranges.length ? ranges.reduce((a, b) => a + b, 0) / ranges.length : 0;
  return { atr: +atr.toFixed(4), stdDev: +stdDev.toFixed(4), avgRange: +avgRange.toFixed(4) };
}

// REST endpoints
app.get('/api/quotes', (req, res) => {
  res.json(latestQuotes);
});

app.get('/api/history/:symbol', async (req, res) => {
  const symbol = decodeURIComponent(req.params.symbol);
  const range = req.query.range || '5d';
  const intervalMap = { '1d': '5m', '5d': '15m', '1mo': '1d', '3mo': '1d' };
  const interval = intervalMap[range] || '15m';
  const history = await fetchHistory(symbol, range, interval);
  const volatility = calcVolatility(history);
  res.json({ symbol, history, volatility });
});

app.get('/api/alerts', (req, res) => {
  res.json(alerts);
});

app.get('/api/sparklines', (req, res) => {
  res.json(priceHistory);
});

// Geopolitical news keywords
const GEO_KEYWORDS = [
  'Iran', 'ceasefire', 'Strait of Hormuz', 'Hormuz',
  'sanctions', 'IRGC', 'Persian Gulf', 'oil tanker',
  'Middle East tension', 'Iran nuclear', 'US Iran',
];

app.get('/api/news', async (req, res) => {
  try {
    const query = encodeURIComponent('US Iran ceasefire OR "Strait of Hormuz" OR "oil prices Iran"');
    const url = `https://news.google.com/rss/search?q=${query}&hl=en-US&gl=US&ceid=US:en`;

    const xmlData = await new Promise((resolve, reject) => {
      https.get(url, (response) => {
        let data = '';
        response.on('data', (chunk) => (data += chunk));
        response.on('end', () => resolve(data));
        response.on('error', reject);
      }).on('error', reject);
    });

    // Simple XML parsing for RSS items
    const items = [];
    const itemRegex = /<item>([\s\S]*?)<\/item>/g;
    let match;
    while ((match = itemRegex.exec(xmlData)) !== null && items.length < 15) {
      const item = match[1];
      const title = (item.match(/<title>([\s\S]*?)<\/title>/) || [])[1] || '';
      const link = (item.match(/<link>([\s\S]*?)<\/link>/) || [])[1] || '';
      const pubDate = (item.match(/<pubDate>([\s\S]*?)<\/pubDate>/) || [])[1] || '';
      const source = (item.match(/<source[^>]*>([\s\S]*?)<\/source>/) || [])[1] || '';
      // Clean CDATA
      const cleanTitle = title.replace(/<!\[CDATA\[|\]\]>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#39;/g, "'").replace(/&quot;/g, '"');
      items.push({
        title: cleanTitle,
        link: link.replace(/<!\[CDATA\[|\]\]>/g, ''),
        pubDate,
        source,
        isGeopolitical: GEO_KEYWORDS.some((kw) => cleanTitle.toLowerCase().includes(kw.toLowerCase())),
      });
    }
    res.json(items);
  } catch (err) {
    console.error('News fetch error:', err.message);
    res.json([]);
  }
});

// Initial fetch + polling
fetchQuotes();
setInterval(fetchQuotes, 30000); // every 30 seconds

app.listen(PORT, () => {
  console.log(`\n  Market Dashboard running at http://localhost:${PORT}\n`);
  console.log('  Tracking: S&P 500, Nasdaq, Dow Jones, Crude Oil, USD Index, Gold');
  console.log('  Alerts: Triggered on 2%+ moves with geopolitical context\n');
});
