/* ═══════════════════════════════════════════════════════════════════════════
   MarketPulse – Dashboard Client
   Handles data polling, chart rendering, alerts, and news.
   ═══════════════════════════════════════════════════════════════════════════ */

(() => {
  "use strict";

  // ── State ───────────────────────────────────────────────────────────────
  let priceChart = null;
  let volumeChart = null;
  let rollingVolChart = null;
  let currentSymbol = "^GSPC";
  let currentPeriod = "1mo";
  let previousPrices = {};           // for flash-on-change
  let alertSoundEnabled = true;

  const REFRESH_MS  = 30_000;        // poll every 30 s
  const INSTRUMENTS = {
    "^GSPC":     "S&P 500",
    "^IXIC":     "Nasdaq",
    "^DJI":      "Dow Jones",
    "CL=F":      "WTI Crude Oil",
    "DX-Y.NYB":  "US Dollar Index",
    "GC=F":      "Gold",
  };
  const CATEGORY_ICON = {
    index: "📊",
    commodity: "🛢️",
    currency: "💵",
  };

  // ── Helpers ─────────────────────────────────────────────────────────────
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => document.querySelectorAll(sel);
  const fmt = (n) =>
    n == null ? "—" : n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function changeClass(pct) {
    if (pct > 0) return "up";
    if (pct < 0) return "down";
    return "flat";
  }

  function playAlertSound() {
    if (!alertSoundEnabled) return;
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = "sine";
      osc.frequency.setValueAtTime(880, ctx.currentTime);
      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 0.5);
    } catch (_) { /* silent fallback */ }
  }

  // ── Ticker Strip ────────────────────────────────────────────────────────
  function renderTickerStrip(data) {
    const strip = $("#ticker-strip");
    if (!strip) return;
    strip.innerHTML = "";

    for (const [name, info] of Object.entries(data)) {
      if (info.error) continue;
      const sym = info.symbol;
      const cls = changeClass(info.change_pct);
      const arrow = info.change_pct > 0 ? "▲" : info.change_pct < 0 ? "▼" : "–";
      const active = sym === currentSymbol ? " active" : "";

      // Flash detection
      const prev = previousPrices[sym];
      let flash = "";
      if (prev !== undefined && prev !== info.price) {
        flash = info.price > prev ? " flash-green" : " flash-red";
      }
      previousPrices[sym] = info.price;

      const card = document.createElement("div");
      card.className = `ticker-card${active}${flash}`;
      card.dataset.symbol = sym;
      card.innerHTML = `
        <div class="ticker-name">${name}</div>
        <div class="ticker-price">${fmt(info.price)}</div>
        <div class="ticker-change ${cls}">
          ${arrow} ${fmt(Math.abs(info.change))}
          <span class="ticker-pct">(${info.change_pct > 0 ? "+" : ""}${info.change_pct.toFixed(2)}%)</span>
        </div>`;
      card.addEventListener("click", () => {
        currentSymbol = sym;
        $("#chart-instrument").value = sym;
        loadChart();
        renderTickerStrip(lastMarketData);   // update active state
      });
      strip.appendChild(card);
    }

    // Remove flash class after animation
    setTimeout(() => {
      $$(".flash-green, .flash-red").forEach((el) => {
        el.classList.remove("flash-green", "flash-red");
      });
    }, 600);
  }

  // ── Charts ──────────────────────────────────────────────────────────────
  const CHART_COLORS = {
    line:     "rgba(59,130,246,1)",
    fill:     "rgba(59,130,246,.08)",
    grid:     "rgba(45,53,72,.5)",
    volUp:    "rgba(34,197,94,.6)",
    volDown:  "rgba(239,68,68,.6)",
    rolling:  "rgba(251,191,36,.8)",
  };

  function createPriceChart(labels, closes, highs, lows) {
    const ctx = $("#price-chart").getContext("2d");
    if (priceChart) priceChart.destroy();

    priceChart = new Chart(ctx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: INSTRUMENTS[currentSymbol] || currentSymbol,
            data: closes,
            borderColor: CHART_COLORS.line,
            backgroundColor: CHART_COLORS.fill,
            borderWidth: 2,
            fill: true,
            tension: 0.3,
            pointRadius: 0,
            pointHoverRadius: 4,
          },
          {
            label: "High",
            data: highs,
            borderColor: "rgba(34,197,94,.3)",
            borderWidth: 1,
            borderDash: [4, 4],
            fill: false,
            pointRadius: 0,
            tension: 0.3,
          },
          {
            label: "Low",
            data: lows,
            borderColor: "rgba(239,68,68,.3)",
            borderWidth: 1,
            borderDash: [4, 4],
            fill: false,
            pointRadius: 0,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { display: true, labels: { color: "#94a3b8", font: { size: 11 } } },
          tooltip: {
            backgroundColor: "#1a1f2e",
            titleColor: "#e2e8f0",
            bodyColor: "#94a3b8",
            borderColor: "#2d3548",
            borderWidth: 1,
          },
        },
        scales: {
          x: {
            grid: { color: CHART_COLORS.grid },
            ticks: { color: "#64748b", maxTicksLimit: 12, font: { size: 10 } },
          },
          y: {
            position: "right",
            grid: { color: CHART_COLORS.grid },
            ticks: { color: "#64748b", font: { size: 10 } },
          },
        },
      },
    });
  }

  function createVolumeChart(labels, volumes, closes) {
    const ctx = $("#volume-chart").getContext("2d");
    if (volumeChart) volumeChart.destroy();

    // Color bars by price change
    const colors = volumes.map((_, i) => {
      if (i === 0) return CHART_COLORS.volUp;
      return closes[i] >= closes[i - 1] ? CHART_COLORS.volUp : CHART_COLORS.volDown;
    });

    volumeChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "Volume",
          data: volumes,
          backgroundColor: colors,
          borderWidth: 0,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { display: false },
          y: {
            position: "right",
            grid: { color: CHART_COLORS.grid },
            ticks: {
              color: "#64748b", font: { size: 9 },
              callback: (v) => v >= 1e9 ? (v / 1e9).toFixed(1) + "B"
                             : v >= 1e6 ? (v / 1e6).toFixed(1) + "M"
                             : v >= 1e3 ? (v / 1e3).toFixed(0) + "K"
                             : v,
            },
          },
        },
      },
    });
  }

  async function loadChart() {
    try {
      const res = await fetch(`/api/historical/${encodeURIComponent(currentSymbol)}?period=${currentPeriod}`);
      const d = await res.json();
      if (d.error) { console.warn("Chart error:", d.error); return; }

      // Shorten date labels
      const labels = d.dates.map((dt) => {
        if (currentPeriod === "1d") return dt.split(" ")[1];
        return dt.split(" ")[0].slice(5);
      });
      createPriceChart(labels, d.close, d.high, d.low);
      createVolumeChart(labels, d.volume, d.close);
    } catch (err) {
      console.error("Chart fetch failed:", err);
    }
  }

  // ── Rolling Volatility Chart ────────────────────────────────────────────
  function createRollingVolChart(dates, values, label) {
    const ctx = $("#rolling-vol-chart").getContext("2d");
    if (rollingVolChart) rollingVolChart.destroy();

    rollingVolChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: dates.map((d) => d.slice(5)),
        datasets: [{
          label: `${label} – 20d Rolling Vol (ann.)`,
          data: values,
          borderColor: CHART_COLORS.rolling,
          backgroundColor: "rgba(251,191,36,.08)",
          borderWidth: 1.5,
          fill: true,
          tension: 0.3,
          pointRadius: 0,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: true, labels: { color: "#94a3b8", font: { size: 10 } } },
        },
        scales: {
          x: { display: false },
          y: {
            position: "right",
            grid: { color: CHART_COLORS.grid },
            ticks: { color: "#64748b", font: { size: 9 }, callback: (v) => v + "%" },
          },
        },
      },
    });
  }

  // ── Volatility Table ────────────────────────────────────────────────────
  async function loadVolatility() {
    try {
      const res = await fetch("/api/volatility");
      const data = await res.json();
      const tbody = $("#vol-tbody");
      tbody.innerHTML = "";

      let firstRolling = null;
      let firstName = "";

      for (const [name, vol] of Object.entries(data)) {
        if (vol.error) {
          tbody.innerHTML += `<tr><td>${name}</td><td colspan="4" class="text-muted">${vol.error}</td></tr>`;
          continue;
        }
        const ddClass = vol.max_drawdown < -10 ? "text-red" : vol.max_drawdown < -5 ? "text-gold" : "";
        tbody.innerHTML += `
          <tr>
            <td>${name}</td>
            <td>${vol.daily_volatility}%</td>
            <td>${vol.annualized_volatility}%</td>
            <td class="${ddClass}">${vol.max_drawdown}%</td>
            <td>${vol.atr_20}</td>
          </tr>`;

        if (!firstRolling && vol.rolling_vol) {
          firstRolling = vol.rolling_vol;
          firstName = name;
        }
      }

      // Show rolling vol chart for currently selected instrument or first available
      const selectedName = INSTRUMENTS[currentSymbol];
      if (data[selectedName] && data[selectedName].rolling_vol) {
        createRollingVolChart(data[selectedName].rolling_vol.dates, data[selectedName].rolling_vol.values, selectedName);
      } else if (firstRolling) {
        createRollingVolChart(firstRolling.dates, firstRolling.values, firstName);
      }
    } catch (err) {
      console.error("Volatility fetch failed:", err);
    }
  }

  // ── Alerts ──────────────────────────────────────────────────────────────
  let lastAlertCount = 0;

  function renderAlerts(alerts) {
    const list = $("#alerts-list");
    const badge = $("#alert-count");

    badge.textContent = alerts.length;
    badge.className = alerts.length > 0 ? "badge active" : "badge";

    if (alerts.length === 0) {
      list.innerHTML = '<li class="no-alerts">No significant moves detected</li>';
      return;
    }

    list.innerHTML = alerts.map((a) => {
      const cls = a.direction === "UP" ? "alert-item-up" : "alert-item-down";
      const arrow = a.direction === "UP" ? "▲" : "▼";
      return `
        <li class="${cls}">
          <span class="alert-instrument">${arrow} ${a.instrument}</span>
          ${a.direction} ${Math.abs(a.change_pct).toFixed(2)}% → ${fmt(a.price)}
          <span class="alert-time">${a.timestamp}</span>
        </li>`;
    }).join("");

    // Show banner + sound for new alerts
    if (alerts.length > lastAlertCount) {
      const newest = alerts[0];
      showAlertBanner(newest);
      playAlertSound();
    }
    lastAlertCount = alerts.length;
  }

  function showAlertBanner(alert) {
    const banner = $("#alert-banner");
    const text = $("#alert-banner-text");
    banner.classList.remove("hidden", "positive");
    if (alert.direction === "UP") banner.classList.add("positive");
    text.textContent = `⚠ ALERT: ${alert.message}`;
    // Auto-hide after 10 s
    setTimeout(() => banner.classList.add("hidden"), 10_000);
  }

  // ── News Feed ───────────────────────────────────────────────────────────
  function renderNews(items) {
    const list = $("#news-list");
    if (!items.length) {
      list.innerHTML = '<li class="loading-cell">No recent news found</li>';
      return;
    }
    list.innerHTML = items.map((n) => `
      <li class="news-item">
        <div class="news-title"><a href="${n.link}" target="_blank" rel="noopener">${n.title}</a></div>
        <div class="news-meta">
          <span class="news-tag">${n.query}</span>
          <span>${n.source}</span>
          <span>${n.published || ""}</span>
        </div>
      </li>`).join("");
  }

  // ── Market Status ───────────────────────────────────────────────────────
  function updateMarketStatus() {
    const now = new Date();
    const et = new Date(now.toLocaleString("en-US", { timeZone: "America/New_York" }));
    const day = et.getDay();
    const h = et.getHours();
    const m = et.getMinutes();
    const mins = h * 60 + m;
    const el = $("#market-status");

    if (day >= 1 && day <= 5 && mins >= 570 && mins < 960) {
      el.textContent = "Market Open";
      el.className = "market-status open";
    } else {
      el.textContent = "Market Closed";
      el.className = "market-status closed";
    }
  }

  // ── Data Polling ────────────────────────────────────────────────────────
  let lastMarketData = {};

  async function pollMarketData() {
    try {
      const res = await fetch("/api/market-data");
      const json = await res.json();
      lastMarketData = json.data || {};
      renderTickerStrip(lastMarketData);
      if (json.last_update) {
        $("#last-update").textContent = `Last update: ${json.last_update}`;
      }
    } catch (err) {
      console.error("Market data poll failed:", err);
    }
  }

  async function pollAlerts() {
    try {
      const res = await fetch("/api/alerts");
      const alerts = await res.json();
      renderAlerts(alerts);
    } catch (err) {
      console.error("Alerts poll failed:", err);
    }
  }

  async function pollNews() {
    try {
      const res = await fetch("/api/news");
      const items = await res.json();
      renderNews(items);
    } catch (err) {
      console.error("News poll failed:", err);
    }
  }

  async function refreshAll() {
    await Promise.all([pollMarketData(), pollAlerts(), pollNews()]);
    loadChart();
    updateMarketStatus();
  }

  // ── Event Listeners ─────────────────────────────────────────────────────
  function init() {
    // Chart instrument selector
    $("#chart-instrument").addEventListener("change", (e) => {
      currentSymbol = e.target.value;
      loadChart();
      renderTickerStrip(lastMarketData);
    });

    // Period buttons
    $$("#period-buttons .period-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        $$("#period-buttons .period-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        currentPeriod = btn.dataset.period;
        loadChart();
      });
    });

    // Alert dismiss
    $("#alert-dismiss").addEventListener("click", () => {
      $("#alert-banner").classList.add("hidden");
    });

    // Refresh volatility
    $("#refresh-vol").addEventListener("click", loadVolatility);

    // Initial load
    refreshAll();
    loadVolatility();

    // Polling intervals
    setInterval(() => {
      pollMarketData();
      pollAlerts();
      loadChart();
      updateMarketStatus();
    }, REFRESH_MS);

    // News refreshes less often (every 2 min)
    setInterval(pollNews, 120_000);

    // Volatility refreshes every 5 min
    setInterval(loadVolatility, 300_000);
  }

  // ── Flash animation (injected via CSS) ──────────────────────────────────
  const style = document.createElement("style");
  style.textContent = `
    @keyframes flashGreen { 0% { background: rgba(34,197,94,.2); } 100% { background: transparent; } }
    @keyframes flashRed   { 0% { background: rgba(239,68,68,.2); } 100% { background: transparent; } }
    .flash-green { animation: flashGreen .6s ease; }
    .flash-red   { animation: flashRed   .6s ease; }
  `;
  document.head.appendChild(style);

  // ── Boot ────────────────────────────────────────────────────────────────
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
