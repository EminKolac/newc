/* ========================================
   Geopolitical News Feed
   Simulated news stream for US-Iran/Hormuz events
   ======================================== */

const NewsService = (() => {
    let newsItems = [];
    let currentFilter = 'all';
    let newsInterval = null;

    // Curated news templates reflecting real-world scenarios
    const NEWS_TEMPLATES = {
        iran: [
            { headline: 'US and Iran resume indirect talks in Oman on ceasefire framework', severity: 'medium', tags: ['iran', 'ceasefire'] },
            { headline: 'Iranian Foreign Minister: "Progress made on key ceasefire conditions"', severity: 'medium', tags: ['iran', 'ceasefire'] },
            { headline: 'White House confirms back-channel diplomatic engagement with Tehran', severity: 'medium', tags: ['iran', 'ceasefire'] },
            { headline: 'Iran IRGC announces naval exercises near Strait of Hormuz', severity: 'high', tags: ['iran', 'hormuz'] },
            { headline: 'US deploys additional carrier strike group to Persian Gulf', severity: 'high', tags: ['iran', 'hormuz'] },
            { headline: 'UN Security Council calls emergency session on Iran tensions', severity: 'high', tags: ['iran'] },
            { headline: 'Iran threatens to close Strait of Hormuz if sanctions intensified', severity: 'high', tags: ['iran', 'hormuz', 'oil'] },
            { headline: 'US State Department: Ceasefire talks "constructive but incomplete"', severity: 'medium', tags: ['iran', 'ceasefire'] },
            { headline: 'Iran signals willingness to discuss shipping lane guarantees', severity: 'medium', tags: ['iran', 'hormuz', 'ceasefire'] },
            { headline: 'Pentagon spokesperson denies reports of military escalation near Iran', severity: 'low', tags: ['iran'] },
            { headline: 'European allies urge restraint as US-Iran tensions fluctuate', severity: 'low', tags: ['iran', 'ceasefire'] },
            { headline: 'Iranian president addresses nation: "We seek peace but are prepared for defense"', severity: 'medium', tags: ['iran'] },
            { headline: 'US sanctions waiver extended for humanitarian goods to Iran', severity: 'low', tags: ['iran', 'ceasefire'] },
        ],
        hormuz: [
            { headline: 'Tanker traffic through Strait of Hormuz falls 15% amid naval tensions', severity: 'high', tags: ['hormuz', 'oil'] },
            { headline: 'Commercial vessel reports being approached by Iranian patrol boats near Hormuz', severity: 'high', tags: ['hormuz', 'iran'] },
            { headline: 'Lloyd\'s of London raises insurance premiums for Persian Gulf shipping', severity: 'medium', tags: ['hormuz', 'oil'] },
            { headline: 'US Fifth Fleet increases patrols in Strait of Hormuz corridor', severity: 'medium', tags: ['hormuz', 'iran'] },
            { headline: 'Satellite imagery shows Iranian fast-attack craft repositioning near Hormuz', severity: 'high', tags: ['hormuz', 'iran'] },
            { headline: 'International Maritime Organization issues advisory for Strait of Hormuz transit', severity: 'medium', tags: ['hormuz'] },
            { headline: 'Japan and South Korea express concern over Hormuz shipping disruption risks', severity: 'low', tags: ['hormuz', 'oil'] },
            { headline: 'Strait of Hormuz traffic normalizing after diplomatic de-escalation signals', severity: 'low', tags: ['hormuz', 'ceasefire'] },
        ],
        oil: [
            { headline: 'Brent crude surges as Hormuz passage concerns intensify', severity: 'high', tags: ['oil', 'hormuz'] },
            { headline: 'OPEC+ emergency meeting called to discuss supply disruption contingencies', severity: 'high', tags: ['oil'] },
            { headline: 'Saudi Arabia pledges to use spare capacity if supply disrupted', severity: 'medium', tags: ['oil'] },
            { headline: 'US Strategic Petroleum Reserve release authorized amid price spike', severity: 'medium', tags: ['oil'] },
            { headline: 'Oil traders pricing in $10-15 "geopolitical risk premium" on crude', severity: 'medium', tags: ['oil', 'iran'] },
            { headline: 'IEA warns of potential 3-5 million bpd supply disruption in worst case', severity: 'high', tags: ['oil', 'hormuz'] },
            { headline: 'Goldman Sachs raises oil price target citing Iran tensions', severity: 'medium', tags: ['oil', 'iran'] },
            { headline: 'US shale producers report accelerating drilling activity', severity: 'low', tags: ['oil'] },
            { headline: 'Global oil inventories at lowest level since 2017 as tensions persist', severity: 'medium', tags: ['oil'] },
        ],
        ceasefire: [
            { headline: 'BREAKING: Draft ceasefire framework leaked, includes Hormuz navigation guarantees', severity: 'high', tags: ['ceasefire', 'hormuz', 'iran'] },
            { headline: 'Ceasefire negotiations stall over sanctions relief timeline', severity: 'medium', tags: ['ceasefire', 'iran'] },
            { headline: 'Qatar mediators report "significant narrowing of differences"', severity: 'medium', tags: ['ceasefire', 'iran'] },
            { headline: 'US Congress members briefed on ceasefire progress, reactions mixed', severity: 'low', tags: ['ceasefire', 'iran'] },
            { headline: 'Iran\'s Supreme Leader sets conditions for ceasefire acceptance', severity: 'high', tags: ['ceasefire', 'iran'] },
            { headline: 'Oil markets rally on rumors of imminent ceasefire announcement', severity: 'high', tags: ['ceasefire', 'oil'] },
            { headline: 'Ceasefire monitoring mechanism being designed by international coalition', severity: 'low', tags: ['ceasefire'] },
            { headline: 'Markets volatile as ceasefire deadline passes without agreement', severity: 'high', tags: ['ceasefire', 'oil', 'iran'] },
            { headline: 'Both sides agree to 72-hour extension of ceasefire talks', severity: 'medium', tags: ['ceasefire', 'iran'] },
        ]
    };

    // Crisis-specific news
    const CRISIS_NEWS = [
        { headline: 'BREAKING: Reports of naval incident near Strait of Hormuz - details emerging', severity: 'high', tags: ['hormuz', 'iran'] },
        { headline: 'BREAKING: Iran suspends ceasefire negotiations citing "hostile US actions"', severity: 'high', tags: ['ceasefire', 'iran'] },
        { headline: 'ALERT: Oil prices spike over 5% on Hormuz disruption fears', severity: 'high', tags: ['oil', 'hormuz'] },
        { headline: 'FLASH: Pentagon raises threat level for Persian Gulf operations', severity: 'high', tags: ['iran', 'hormuz'] },
        { headline: 'URGENT: Multiple tankers rerouting to avoid Strait of Hormuz', severity: 'high', tags: ['hormuz', 'oil'] },
        { headline: 'BREAKING: Iran announces temporary closure of Hormuz shipping lanes for exercises', severity: 'high', tags: ['hormuz', 'iran', 'oil'] },
        { headline: 'ALERT: US evacuates non-essential personnel from Gulf diplomatic posts', severity: 'high', tags: ['iran'] },
        { headline: 'FLASH: Safe-haven assets surge as Iran crisis escalates', severity: 'high', tags: ['iran', 'oil'] },
    ];

    function init() {
        setupFilterListeners();
        // Seed initial news
        seedInitialNews();
        // Start periodic news generation
        newsInterval = setInterval(generateRandomNews, 15000 + Math.random() * 20000);
    }

    function seedInitialNews() {
        const allTemplates = getAllTemplates();
        // Pick 8 random initial items
        for (let i = 0; i < 8; i++) {
            const template = allTemplates[Math.floor(Math.random() * allTemplates.length)];
            const minutesAgo = (8 - i) * 5 + Math.floor(Math.random() * 5);
            addNewsItem({
                ...template,
                time: Date.now() - minutesAgo * 60000,
                isNew: false
            });
        }
        renderNews();
    }

    function getAllTemplates() {
        return [
            ...NEWS_TEMPLATES.iran,
            ...NEWS_TEMPLATES.hormuz,
            ...NEWS_TEMPLATES.oil,
            ...NEWS_TEMPLATES.ceasefire
        ];
    }

    function generateRandomNews() {
        const categories = Object.keys(NEWS_TEMPLATES);
        const cat = categories[Math.floor(Math.random() * categories.length)];
        const templates = NEWS_TEMPLATES[cat];
        const template = templates[Math.floor(Math.random() * templates.length)];

        addNewsItem({
            ...template,
            time: Date.now(),
            isNew: true
        });

        renderNews();
    }

    function triggerCrisisEvent(intensity) {
        // Generate 1-3 crisis news items
        const count = Math.min(3, Math.floor(intensity) + 1);
        const used = new Set();

        for (let i = 0; i < count; i++) {
            let idx;
            do {
                idx = Math.floor(Math.random() * CRISIS_NEWS.length);
            } while (used.has(idx) && used.size < CRISIS_NEWS.length);
            used.add(idx);

            setTimeout(() => {
                addNewsItem({
                    ...CRISIS_NEWS[idx],
                    time: Date.now(),
                    isNew: true
                });
                renderNews();
            }, i * 3000); // Stagger crisis news
        }
    }

    function addNewsItem(item) {
        newsItems.unshift(item);
        if (newsItems.length > 50) newsItems.pop();
    }

    function renderNews() {
        const container = document.getElementById('news-feed');
        const filtered = currentFilter === 'all'
            ? newsItems
            : newsItems.filter(item => item.tags.includes(currentFilter));

        container.innerHTML = filtered.map(item => {
            const timeStr = new Date(item.time).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
            const severityClass = `severity-${item.severity}`;
            const newClass = item.isNew ? 'new-item' : '';

            const tagsHtml = item.tags.map(tag =>
                `<span class="news-tag tag-${tag}">${tag.toUpperCase()}</span>`
            ).join('');

            // Clear new flag after render
            item.isNew = false;

            return `
                <div class="news-item ${severityClass} ${newClass}">
                    <div class="news-time">${timeStr}</div>
                    <div class="news-headline">${item.headline}</div>
                    <div class="news-tags">${tagsHtml}</div>
                </div>
            `;
        }).join('');
    }

    function setupFilterListeners() {
        document.querySelectorAll('.news-filter').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.news-filter').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.filter;
                renderNews();
            });
        });
    }

    return { init, triggerCrisisEvent, renderNews };
})();
