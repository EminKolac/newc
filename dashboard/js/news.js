/**
 * Geopolitical News Feed
 * Simulates a real-time news feed focused on US-Iran tensions,
 * Strait of Hormuz developments, and ceasefire negotiations.
 * In production, replace with real news API (Reuters, Bloomberg, etc.)
 */

const NewsFeed = (() => {
    const newsItems = [];
    const MAX_NEWS = 30;
    let nextEventTime = 0;
    let eventIndex = 0;

    // Curated news scenarios for US-Iran / Strait of Hormuz
    const scenarios = [
        {
            priority: 'breaking',
            source: 'Reuters',
            headline: 'Iran signals willingness to resume ceasefire talks with US through Omani intermediaries',
            summary: 'Senior Iranian diplomatic sources confirm back-channel communications have resumed after a 3-week hiatus.',
            impacts: ['Oil -2.1%', 'Gold -0.8%', 'Equities +1.2%'],
            tags: ['CEASEFIRE', 'DIPLOMACY'],
            shockMagnitude: -0.5 // Positive for markets
        },
        {
            priority: 'urgent',
            source: 'AP News',
            headline: 'US Navy increases carrier group presence near Strait of Hormuz amid shipping concerns',
            summary: 'USS Eisenhower strike group repositioned closer to the strait following reports of IRGC naval exercises.',
            impacts: ['Oil +3.2%', 'Gold +1.5%', 'DXY +0.3%'],
            tags: ['HORMUZ', 'MILITARY'],
            shockMagnitude: 1.5
        },
        {
            priority: 'normal',
            source: 'Bloomberg',
            headline: 'Crude oil tanker insurance premiums rise 15% on Hormuz transit risk reassessment',
            summary: 'Major insurers Lloyd\'s and Swiss Re updating war risk premiums for vessels transiting the strait.',
            impacts: ['Oil +1.8%', 'Shipping +2.1%'],
            tags: ['HORMUZ', 'OIL'],
            shockMagnitude: 0.8
        },
        {
            priority: 'breaking',
            source: 'WSJ',
            headline: 'Iran\'s IRGC conducts live-fire naval exercise near Strait of Hormuz shipping lanes',
            summary: 'Exercise involves fast-attack craft and anti-ship missiles. US Central Command monitoring closely.',
            impacts: ['Oil +4.5%', 'Gold +2.2%', 'SPX -1.8%'],
            tags: ['HORMUZ', 'MILITARY', 'ESCALATION'],
            shockMagnitude: 2.5
        },
        {
            priority: 'normal',
            source: 'FT',
            headline: 'European allies push for renewed JCPOA framework as basis for ceasefire negotiations',
            summary: 'France and Germany propose modified nuclear deal framework that could unlock diplomatic progress.',
            impacts: ['Oil -1.2%', 'EUR/USD +0.3%'],
            tags: ['CEASEFIRE', 'DIPLOMACY'],
            shockMagnitude: -0.3
        },
        {
            priority: 'urgent',
            source: 'CNBC',
            headline: 'Oil prices spike as Iran threatens to restrict Strait of Hormuz traffic in response to new sanctions',
            summary: 'Iranian foreign ministry spokesperson warns of "proportional response" to latest US sanctions package.',
            impacts: ['Oil +5.1%', 'Gold +1.8%', 'DOW -2.3%'],
            tags: ['HORMUZ', 'SANCTIONS', 'OIL'],
            shockMagnitude: 2.0
        },
        {
            priority: 'normal',
            source: 'Al Jazeera',
            headline: 'Oman hosts secret US-Iran preliminary talks on de-escalation framework',
            summary: 'Sources confirm two rounds of indirect talks have taken place in Muscat over the past week.',
            impacts: ['Oil -0.8%', 'Risk sentiment improving'],
            tags: ['CEASEFIRE', 'DIPLOMACY'],
            shockMagnitude: -0.4
        },
        {
            priority: 'breaking',
            source: 'Reuters',
            headline: 'Commercial vessel reports drone sighting near Strait of Hormuz; US Navy investigating',
            summary: 'Greek-flagged tanker "Athena Star" reported unmanned aerial vehicle flying at low altitude near its position.',
            impacts: ['Oil +2.8%', 'Gold +1.1%', 'VIX +3.2'],
            tags: ['HORMUZ', 'SECURITY'],
            shockMagnitude: 1.8
        },
        {
            priority: 'urgent',
            source: 'BBC',
            headline: 'UN Security Council emergency session called over Strait of Hormuz maritime security',
            summary: 'Russia and China expected to oppose any resolution authorizing expanded naval operations.',
            impacts: ['Gold +0.9%', 'DXY +0.2%'],
            tags: ['HORMUZ', 'DIPLOMACY'],
            shockMagnitude: 0.5
        },
        {
            priority: 'normal',
            source: 'Bloomberg',
            headline: 'Saudi Arabia offers to mediate US-Iran ceasefire as Crown Prince meets both envoys',
            summary: 'MBS reportedly proposed a phased de-escalation plan including partial sanctions relief.',
            impacts: ['Oil -1.5%', 'Equities +0.8%'],
            tags: ['CEASEFIRE', 'DIPLOMACY'],
            shockMagnitude: -0.6
        },
        {
            priority: 'breaking',
            source: 'CNN',
            headline: 'Pentagon confirms Iranian fast boats approached US destroyer in Strait of Hormuz',
            summary: 'USS Mason fired warning flares after IRGC vessels came within 300 yards in "unsafe and unprofessional" encounter.',
            impacts: ['Oil +3.8%', 'Gold +2.0%', 'NASDAQ -2.1%'],
            tags: ['HORMUZ', 'MILITARY', 'ESCALATION'],
            shockMagnitude: 2.8
        },
        {
            priority: 'normal',
            source: 'Reuters',
            headline: 'OPEC+ emergency meeting possible if Hormuz tensions disrupt oil supply',
            summary: 'Saudi Energy Minister says group is prepared to act to stabilize markets if necessary.',
            impacts: ['Oil -0.5%', 'OPEC +signal'],
            tags: ['OIL', 'OPEC'],
            shockMagnitude: -0.2
        },
        {
            priority: 'urgent',
            source: 'FT',
            headline: 'Gold hits session highs as traders seek safe haven amid Gulf escalation fears',
            summary: 'Spot gold breaches key resistance level as institutional flows shift to precious metals and treasuries.',
            impacts: ['Gold +1.4%', 'UST 10Y -8bps'],
            tags: ['GOLD', 'SAFE HAVEN'],
            shockMagnitude: 0.3
        },
        {
            priority: 'breaking',
            source: 'WSJ',
            headline: 'US and Iran agree to 72-hour cooling-off period in Strait of Hormuz',
            summary: 'Both sides commit to no military exercises in shipping lanes for 3 days as diplomatic window opens.',
            impacts: ['Oil -3.2%', 'SPX +1.8%', 'Gold -1.5%'],
            tags: ['CEASEFIRE', 'DE-ESCALATION'],
            shockMagnitude: -1.5
        },
        {
            priority: 'urgent',
            source: 'Bloomberg',
            headline: 'VIX surges past 25 as geopolitical risk premium reprices across asset classes',
            summary: 'Options markets showing elevated demand for downside protection. Skew at 6-month highs.',
            impacts: ['VIX +18%', 'SPX -1.2%'],
            tags: ['VOLATILITY', 'RISK'],
            shockMagnitude: 1.0
        },
        {
            priority: 'normal',
            source: 'CNBC',
            headline: 'Energy sector leads S&P 500 gains as oil supply concerns dominate trading',
            summary: 'XLE up 2.8% with Exxon, Chevron, and ConocoPhillips among top performers.',
            impacts: ['XLE +2.8%', 'Oil +1.5%'],
            tags: ['ENERGY', 'OIL'],
            shockMagnitude: 0.4
        }
    ];

    function init() {
        // Schedule first event
        scheduleNext();
        // Add a few initial items
        addNewsItem(scenarios[0]);
        addNewsItem(scenarios[4]);
        addNewsItem(scenarios[11]);
    }

    function scheduleNext() {
        // Random interval between 8-25 seconds
        nextEventTime = Date.now() + (8000 + Math.random() * 17000);
    }

    function tick() {
        if (Date.now() >= nextEventTime) {
            // Pick next scenario (cycle through with some randomness)
            const idx = Math.floor(Math.random() * scenarios.length);
            const scenario = scenarios[idx];
            addNewsItem(scenario);
            scheduleNext();

            // Trigger market shock if significant
            if (Math.abs(scenario.shockMagnitude) > 0.5) {
                MarketData.triggerGeoShock(scenario.shockMagnitude);
            }

            return scenario;
        }
        return null;
    }

    function addNewsItem(scenario) {
        const item = {
            id: Date.now() + Math.random(),
            time: new Date(),
            ...scenario
        };
        newsItems.unshift(item);
        if (newsItems.length > MAX_NEWS) {
            newsItems.pop();
        }
    }

    function render() {
        const container = document.getElementById('news-feed');
        if (!container) return;

        container.innerHTML = newsItems.map(item => {
            const timeStr = item.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            const priorityClass = item.priority === 'breaking' ? 'breaking' : item.priority === 'urgent' ? 'urgent' : '';
            const tagHtml = item.priority !== 'normal'
                ? `<span class="news-tag ${item.priority}">${item.priority.toUpperCase()}</span>`
                : '';

            return `
                <div class="news-item ${priorityClass}">
                    <div class="news-meta">
                        <span class="news-source">${item.source}${tagHtml}</span>
                        <span class="news-time">${timeStr}</span>
                    </div>
                    <div class="news-headline">${item.headline}</div>
                    <div class="news-summary">${item.summary}</div>
                    <div class="news-impact">
                        ${item.tags.map(t => `<span class="impact-tag">${t}</span>`).join('')}
                        ${item.impacts.map(i => `<span class="impact-tag">${i}</span>`).join('')}
                    </div>
                </div>
            `;
        }).join('');
    }

    function getItems() {
        return newsItems;
    }

    return {
        init,
        tick,
        render,
        getItems
    };
})();
