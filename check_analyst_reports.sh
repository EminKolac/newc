#!/bin/bash
# BIST Analyst Report Checker
# Checks evofin MCP for new analyst reports and sends email via Resend
# Schedule with cron: 0 8 * * 1-5 /path/to/check_analyst_reports.sh
#
# Requirements: claude CLI must be available in PATH

RESEND_API_KEY="re_WMKkt8xM_CWwF3ck7Gz5JCcx5ozY5B3Nc"
EMAIL_TO="mehmetemin.kolac@tvf.com.tr"
TODAY=$(date +%Y-%m-%d)

PROMPT=$(cat <<PROMPT_EOF
You have access to the evofin MCP tools. Do the following:

1. For EACH of these tickers: TURSG, TCELL, TTKOM, HALKB, TRENJ, TRMET, TRALT, THYAO, VAKBN, KRDMD, KAYSE
   - Use dokumanlarda_ara with:
     - filter: dokuman_tipi = "araci_kurum_raporu" AND iliskili_semboller = "<TICKER>"
     - sirala: yayinlanma_tarihi_utc:desc
     - sayfa_basi: 5
   - Check if any result has yayinlanma_tarihi_utc within the last 24 hours from now.

2. For each NEW report found (last 24h), use dokuman_chunk_yukle to load the first 2 chunks and extract:
   - Hisse (ticker)
   - Araci Kurum (brokerage name from document_title)
   - Tarih (publication date)
   - Hedef Fiyat (target price if mentioned)
   - Tavsiye (recommendation: AL/TUT/SAT if mentioned)
   - Ozet (1-2 sentence summary)
   - Rapor URL (dokuman_orijinal_url)

3. If there are ANY new reports, send an email using this exact bash curl command:

curl -X POST 'https://api.resend.com/emails' \\
  -H 'Authorization: Bearer ${RESEND_API_KEY}' \\
  -H 'Content-Type: application/json' \\
  -d '{
    "from": "Analist Rapor Botu <onboarding@resend.dev>",
    "to": ["${EMAIL_TO}"],
    "subject": "Gunluk Analist Raporu Ozeti - ${TODAY}",
    "html": "<HTML_CONTENT>"
  }'

The HTML content should be a professional email with:
- A header: "Gunluk Analist Rapor Ozeti - ${TODAY}"
- A styled HTML table with columns: Hisse, Araci Kurum, Tarih, Hedef Fiyat, Tavsiye, Ozet
- Each report's Rapor URL as a clickable link in an extra column
- Clean styling: border-collapse, padding 8px, light gray header background, alternating row colors
- IMPORTANT: Escape all double quotes in the HTML as \\" for the JSON payload

4. If NO new reports found, just print "No new analyst reports in the last 24 hours." and do NOT send email.

Do NOT skip any ticker. Check all 11 tickers.
PROMPT_EOF
)

cd /home/user/newc

echo "[$(date)] Checking for new analyst reports..."
claude --print "$PROMPT" 2>&1
echo "[$(date)] Done."
