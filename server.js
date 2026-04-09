const express = require('express');
const http = require('http');
const { WebSocketServer } = require('ws');
const path = require('path');

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

app.use(express.static(path.join(__dirname, 'public')));

// ── Symbol configuration ───────────────────────────────────────────────
const SYMBOLS = {
  '^GSPC':    { name: 'S&P 500',        category: 'index' },
  '^IXIC':    { name: 'Nasdaq Composite', category: 'index' },
  '^DJI':     { name: 'Dow Jones',       category: 'index' },
  'CL=F':     { name: 'WTI Crude Oil',   category: 'commodity' },
  'DX-Y.NYB': { name: 'US Dollar Index', category: 'currency' },
  'GC=F':     { name: 'Gold',            category: 'commodity' },
};

const ALERT_THRESHOLD = 0.02; // 2%
const POLL_INTERVAL = 30_000; // 30 seconds
const NEWS_POLL_INTERVAL = 300_000; // 5 minutes

// ── In-memory stores ───────────────────────────────────────────────────
const priceHistory = {};   // symbol → [{time, price}]
const latestQuotes = {};   // symbol → quote object
const alertLog = [];       // [{time, symbol, pctChange, msg}]
const newsItems = [];       // [{time, title, source, snippet}]

for (const sym of Object.keys(SYMBOLS)) {
  priceHistory[sym] = [];
}

// ── Yahoo Finance fetcher ──────────────────────────────────────────────
async function fetchQuotes() {
  const symbols = Object.keys(SYMBOLS).join(',');
  const url = `https://query1.finance.yahoo.com/v7/finance/quote?symbols=${encodeURIComponent(symbols)}`;
  try {
    const res = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    if (!res.ok) throw new Error(`Yahoo API ${res.status}`);
    const data = await res.json();
    const results = data?.quoteResponse?.result || [];
    const now = Date.now();

    for (const q of results) {
      const sym = q.symbol;
      if (!SYMBOLS[sym]) continue;

      const price = q.regularMarketPrice ?? q.price ?? null;
      const prevClose = q.regularMarketPreviousClose ?? q.previousClose ?? null;
      const change = q.regularMarketChange ?? null;
      const changePct = q.regularMarketChangePercent ?? null;
      const volume = q.regularMarketVolume ?? null;
      const dayHigh = q.regularMarketDayHigh ?? null;
      const dayLow = q.regularMarketDayLow ?? null;
      const open = q.regularMarketOpen ?? null;

      const quote = {
        symbol: sym,
        name: SYMBOLS[sym].name,
        category: SYMBOLS[sym].category,
        price,
        prevClose,
        change,
        changePct,
        volume,
        dayHigh,
        dayLow,
        open,
        time: now,
        marketState: q.marketState || 'UNKNOWN',
      };

      latestQuotes[sym] = quote;

      // Store price history (keep last 500 points per symbol)
      if (price != null) {
        priceHistory[sym].push({ time: now, price });
        if (priceHistory[sym].length > 500) {
          priceHistory[sym] = priceHistory[sym].slice(-500);
        }
      }

      // Check alert threshold
      if (changePct != null && Math.abs(changePct) >= ALERT_THRESHOLD * 100) {
        const alert = {
          time: now,
          symbol: sym,
          name: SYMBOLS[sym].name,
          pctChange: changePct,
          price,
          msg: `${SYMBOLS[sym].name} moved ${changePct > 0 ? '+' : ''}${changePct.toFixed(2)}% — now at ${price?.toLocaleString()}`,
        };
        // Avoid duplicate alerts within 5 minutes
        const isDuplicate = alertLog.some(
          a => a.symbol === sym && Math.abs(a.time - now) < 300_000
        );
        if (!isDuplicate) {
          alertLog.push(alert);
          if (alertLog.length > 200) alertLog.splice(0, alertLog.length - 200);
        }
      }
    }
  } catch (err) {
    console.error('[fetchQuotes]', err.message);
  }
}

// ── Volatility calculator ──────────────────────────────────────────────
function computeVolatility(sym) {
  const hist = priceHistory[sym];
  if (!hist || hist.length < 2) return null;

  // Use log returns for volatility
  const returns = [];
  for (let i = 1; i < hist.length; i++) {
    if (hist[i].price > 0 && hist[i - 1].price > 0) {
      returns.push(Math.log(hist[i].price / hist[i - 1].price));
    }
  }
  if (returns.length < 2) return null;

  const mean = returns.reduce((s, r) => s + r, 0) / returns.length;
  const variance = returns.reduce((s, r) => s + (r - mean) ** 2, 0) / (returns.length - 1);
  const stdDev = Math.sqrt(variance);

  // Annualize (assuming ~30s intervals → ~780 intervals per 6.5hr trading day → ~195,000/yr)
  // But for display we just show the raw session volatility
  return {
    stdDev: stdDev * 100, // as percentage
    sampleSize: returns.length,
    annualized: stdDev * Math.sqrt(252 * 780) * 100, // rough annualization
  };
}

// ── News fetcher (geopolitical headlines) ──────────────────────────────
async function fetchGeopoliticalNews() {
  // Use Google News RSS as a free source for relevant headlines
  const queries = [
    'US+Iran+ceasefire',
    'Strait+of+Hormuz',
    'Iran+oil+sanctions',
  ];

  for (const q of queries) {
    try {
      const url = `https://news.google.com/rss/search?q=${q}&hl=en-US&gl=US&ceid=US:en`;
      const res = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0' }
      });
      if (!res.ok) continue;
      const xml = await res.text();

      // Simple XML parsing for RSS items
      const itemRegex = /<item>([\s\S]*?)<\/item>/g;
      let match;
      while ((match = itemRegex.exec(xml)) !== null) {
        const itemXml = match[1];
        const title = (itemXml.match(/<title>([\s\S]*?)<\/title>/) || [])[1] || '';
        const pubDate = (itemXml.match(/<pubDate>([\s\S]*?)<\/pubDate>/) || [])[1] || '';
        const source = (itemXml.match(/<source[^>]*>([\s\S]*?)<\/source>/) || [])[1] || '';
        const link = (itemXml.match(/<link>([\s\S]*?)<\/link>/) || [])[1] || '';

        const cleanTitle = title.replace(/<!\[CDATA\[|\]\]>/g, '').trim();
        if (!cleanTitle) continue;

        // Deduplicate by title
        const exists = newsItems.some(n => n.title === cleanTitle);
        if (!exists) {
          newsItems.push({
            time: pubDate ? new Date(pubDate).getTime() : Date.now(),
            title: cleanTitle,
            source: source.replace(/<!\[CDATA\[|\]\]>/g, '').trim(),
            link: link.trim(),
            query: q.replace(/\+/g, ' '),
          });
        }
      }

      // Keep latest 100 news items, sorted by time
      newsItems.sort((a, b) => b.time - a.time);
      if (newsItems.length > 100) newsItems.length = 100;
    } catch (err) {
      console.error('[fetchNews]', err.message);
    }
  }
}

// ── Build snapshot for clients ─────────────────────────────────────────
function buildSnapshot() {
  const volatility = {};
  for (const sym of Object.keys(SYMBOLS)) {
    volatility[sym] = computeVolatility(sym);
  }

  return {
    type: 'snapshot',
    quotes: latestQuotes,
    history: priceHistory,
    volatility,
    alerts: alertLog.slice(-50),
    news: newsItems.slice(0, 30),
    timestamp: Date.now(),
  };
}

// ── WebSocket management ───────────────────────────────────────────────
wss.on('connection', (ws) => {
  console.log('[ws] client connected');
  // Send initial snapshot
  ws.send(JSON.stringify(buildSnapshot()));

  ws.on('close', () => console.log('[ws] client disconnected'));
});

function broadcast() {
  const payload = JSON.stringify(buildSnapshot());
  for (const ws of wss.clients) {
    if (ws.readyState === 1) ws.send(payload);
  }
}

// ── REST API fallback ──────────────────────────────────────────────────
app.get('/api/snapshot', (_req, res) => {
  res.json(buildSnapshot());
});

app.get('/api/quotes', (_req, res) => {
  res.json(latestQuotes);
});

app.get('/api/alerts', (_req, res) => {
  res.json(alertLog.slice(-50));
});

app.get('/api/news', (_req, res) => {
  res.json(newsItems.slice(0, 30));
});

// ── Polling loops ──────────────────────────────────────────────────────
async function startPolling() {
  // Initial fetches
  await fetchQuotes();
  await fetchGeopoliticalNews();
  broadcast();

  // Market data every 30s
  setInterval(async () => {
    await fetchQuotes();
    broadcast();
  }, POLL_INTERVAL);

  // News every 5 minutes
  setInterval(async () => {
    await fetchGeopoliticalNews();
    broadcast();
  }, NEWS_POLL_INTERVAL);
}

// ── Start ──────────────────────────────────────────────────────────────
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`\n  Market Dashboard running at http://localhost:${PORT}\n`);
  startPolling();
});
