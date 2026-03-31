# Scheduled Analyst Report Prompt (for Claude Code Scheduled Runs)

## How to keep it working

1. **First time (or when token expires):** Open an interactive Claude Code session on this project and run this prompt manually. Complete the OAuth flow in your browser. The token gets cached.
2. **Scheduled runs:** The cached token is reused automatically — no browser needed.
3. **When token expires:** The fallback below sends you an email alert so you know to re-auth.

---

## Prompt (copy this into your scheduled task)

```
STEP 0 - AUTH CHECK:
First, try calling any evofin tool (e.g. dokumanlarda_ara with a simple query). 
If you get an OAuth/authentication URL instead of real results, do NOT proceed with the main task.
Instead, send this notification email and STOP:

curl -X POST 'https://api.resend.com/emails' \
  -H 'Authorization: Bearer re_WMKkt8xM_CWwF3ck7Gz5JCcx5ozY5B3Nc' \
  -H 'Content-Type: application/json' \
  -d '{"from":"Analist Rapor Botu <onboarding@resend.dev>","to":["mehmetemin.kolac@tvf.com.tr"],"subject":"[AKSIYON GEREKLI] Evofin Token Suresi Doldu","html":"<h2>Evofin MCP token suresi doldu</h2><p>Zamanlanmis analist rapor taramas\u0131 calistirilamadi. Lutfen asagidaki adimlari izleyin:</p><ol><li>Claude Code interaktif oturum acin</li><li>Evofin MCP aracini kullanin ve tarayicida OAuth onayini tamamlayin</li><li>Token otomatik olarak onbelleğe alinacaktir</li></ol>"}'

Then print: "AUTH EXPIRED - Notification email sent. Please re-authenticate interactively."
And STOP. Do not continue.

STEP 1 - SEARCH REPORTS:
For EACH of these tickers: TURSG, TCELL, TTKOM, HALKB, TRENJ, TRMET, TRALT, THYAO, VAKBN, KRDMD, KAYSE
- Use dokumanlarda_ara with:
  - filter: dokuman_tipi = "araci_kurum_raporu" AND iliskili_semboller = "<TICKER>"
  - sirala: yayinlanma_tarihi_utc:desc
  - sayfa_basi: 5
- Check if any result has yayinlanma_tarihi_utc within the last 24 hours from now.

STEP 2 - EXTRACT DETAILS:
For each NEW report found (last 24h), use dokuman_chunk_yukle to load the first 2 chunks and extract:
- Hisse (ticker)
- Araci Kurum (brokerage name from document_title)
- Tarih (publication date)
- Hedef Fiyat (target price if mentioned)
- Tavsiye (recommendation: AL/TUT/SAT if mentioned)
- Ozet (1-2 sentence summary)
- Rapor URL (dokuman_orijinal_url)

STEP 3 - SEND EMAIL (only if new reports exist):
If there are ANY new reports, send an email using this exact bash curl command:

curl -X POST 'https://api.resend.com/emails' \
  -H 'Authorization: Bearer re_WMKkt8xM_CWwF3ck7Gz5JCcx5ozY5B3Nc' \
  -H 'Content-Type: application/json' \
  -d '{
    "from": "Analist Rapor Botu <onboarding@resend.dev>",
    "to": ["mehmetemin.kolac@tvf.com.tr"],
    "subject": "Gunluk Analist Raporu Ozeti - <TODAY_DATE>",
    "html": "<HTML_CONTENT>"
  }'

The HTML content should be a professional email with:
- A header: "Gunluk Analist Rapor Ozeti - <TODAY_DATE>"
- A styled HTML table with columns: Hisse, Araci Kurum, Tarih, Hedef Fiyat, Tavsiye, Ozet
- Each report's Rapor URL as a clickable link in an extra column
- Clean styling: border-collapse, padding 8px, light gray header background, alternating row colors
- IMPORTANT: Escape all double quotes in the HTML as \" for the JSON payload
- Replace <TODAY_DATE> with today's actual date
- Replace <HTML_CONTENT> with the actual generated HTML

If NO new reports found, just print "No new analyst reports in the last 24 hours." and do NOT send email.

Do NOT skip any ticker. Check all 11 tickers.
```
