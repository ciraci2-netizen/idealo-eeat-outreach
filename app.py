import streamlit as st
import requests
import json
import time
import csv
import io
from openai import OpenAI

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Idealo · EEAT Outreach",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PREMIUM DARK CSS — Vercel/Linear inspired
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=GeistMono:wght@400;500;600&family=Outfit:wght@300;400;500;600;700&display=swap');

:root {
    --bg:          #0f1117;
    --surface-1:   #181c27;
    --surface-2:   #1e2335;
    --surface-3:   #252c3f;
    --border:      #2e3650;
    --border-hi:   #3d4a6b;
    --text-1:      #f0f2f8;
    --text-2:      #b0b8d0;
    --text-3:      #6b7899;
    --accent:      #0070f3;
    --accent-glow: rgba(0,112,243,0.15);
    --accent-hi:   #338ef7;
    --green:       #17c964;
    --green-bg:    rgba(23,201,100,0.08);
    --amber:       #f5a623;
    --amber-bg:    rgba(245,166,35,0.08);
    --red:         #f31260;
    --red-bg:      rgba(243,18,96,0.08);
    --radius:      8px;
    --radius-lg:   12px;
}

/* ── GLOBAL RESET ── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg) !important;
    color: var(--text-1) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--surface-1) !important;
    border-right: 1px solid var(--border) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-1) !important;
    font-family: 'Outfit', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ── SLIDERS ── */
.stSlider > div > div > div > div {
    background: var(--accent) !important;
}

/* ── BUTTON ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
    padding: 0.6rem 1.6rem !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 0 20px var(--accent-glow) !important;
}
.stButton > button:hover {
    background: var(--accent-hi) !important;
    box-shadow: 0 0 30px rgba(0,112,243,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── TABS ── */
[data-testid="stTabs"] > div:first-child {
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-2) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.7rem 1.2rem !important;
    margin-right: 0 !important;
    transition: color 0.15s !important;
}
button[data-baseweb="tab"]:hover { color: var(--text-1) !important; }
button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--text-1) !important;
    border-bottom-color: var(--accent) !important;
}

/* ── PROGRESS ── */
[data-testid="stProgressBar"] > div > div {
    background: var(--accent) !important;
}

/* ── ALERT / INFO ── */
[data-testid="stAlert"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
}

/* ── MARKDOWN headers ── */
h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.03em !important;
    color: var(--text-1) !important;
}

/* ── CUSTOM COMPONENTS ── */

/* Sidebar logo block */
.sidebar-logo {
    padding: 1.4rem 1.2rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
}
.sidebar-logo-mark {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.5rem;
}
.logo-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
}
.logo-text {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text-1);
    letter-spacing: -0.01em;
}
.logo-sub {
    font-family: 'GeistMono', monospace;
    font-size: 0.65rem;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* Section label */
.section-label {
    font-family: 'GeistMono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-3);
    margin: 1.4rem 0 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Header */
.app-header {
    padding: 2rem 0 1.8rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -60px; left: -40px;
    width: 300px; height: 200px;
    background: radial-gradient(ellipse, rgba(0,112,243,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.header-eyebrow {
    font-family: 'GeistMono', monospace;
    font-size: 0.7rem;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 0.5rem;
}
.header-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--text-1);
    line-height: 1.1;
    margin-bottom: 0.4rem;
}
.header-title span { color: var(--accent); }
.header-sub {
    font-family: 'Outfit', sans-serif;
    font-size: 0.88rem;
    color: var(--text-2);
    font-weight: 400;
}
.header-badges {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.header-badge {
    font-family: 'GeistMono', monospace;
    font-size: 0.7rem;
    padding: 3px 9px;
    border-radius: 4px;
    border: 1px solid var(--border);
    color: var(--text-3);
    background: var(--surface-2);
    letter-spacing: 0.04em;
}
.header-badge.active {
    border-color: rgba(0,112,243,0.4);
    color: var(--accent-hi);
    background: var(--accent-glow);
}

/* KPI cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 1.4rem 0;
}
.kpi-card {
    background: var(--surface-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.1rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: var(--border-hi); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
    opacity: 0.6;
}
.kpi-card.warn::before { background: linear-gradient(90deg, var(--red), transparent); }
.kpi-label {
    font-family: 'GeistMono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-3);
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--text-1);
    line-height: 1;
}
.kpi-value.warn { color: var(--red); }
.kpi-sub {
    font-family: 'GeistMono', monospace;
    font-size: 0.65rem;
    color: var(--text-3);
    margin-top: 0.3rem;
}

/* Result card */
.rcard {
    background: var(--surface-1);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    margin-bottom: 10px;
    transition: border-color 0.15s, background 0.15s;
    position: relative;
    overflow: hidden;
}
.rcard:hover {
    border-color: var(--border-hi);
    background: var(--surface-2);
}
.rcard-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 0.8rem;
}
.rcard-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-1);
    text-decoration: none;
    line-height: 1.3;
    display: block;
    margin-bottom: 2px;
}
.rcard-title:hover { color: var(--accent-hi); }
.rcard-url {
    font-family: 'GeistMono', monospace;
    font-size: 0.7rem;
    color: var(--text-3);
}
.rcard-scores {
    display: flex;
    gap: 6px;
    flex-shrink: 0;
    align-items: center;
}
.score-pill {
    font-family: 'GeistMono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 5px;
    white-space: nowrap;
}
.score-pill.hi  { background: var(--green-bg);  color: var(--green);  border: 1px solid rgba(23,201,100,0.2); }
.score-pill.mid { background: var(--amber-bg);  color: var(--amber);  border: 1px solid rgba(245,166,35,0.2); }
.score-pill.lo  { background: var(--red-bg);    color: var(--red);    border: 1px solid rgba(243,18,96,0.2); }
.prio-pill {
    font-family: 'GeistMono', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 5px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.prio-HIGH   { background: var(--green-bg); color: var(--green); border: 1px solid rgba(23,201,100,0.25); }
.prio-MEDIUM { background: var(--amber-bg); color: var(--amber); border: 1px solid rgba(245,166,35,0.25); }
.prio-LOW    { background: var(--red-bg);   color: var(--red);   border: 1px solid rgba(243,18,96,0.25); }

.rcard-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 0.7rem;
    align-items: center;
}
.tag {
    font-family: 'GeistMono', monospace;
    font-size: 0.67rem;
    padding: 2px 7px;
    border-radius: 4px;
    background: var(--surface-3);
    border: 1px solid var(--border);
    color: var(--text-2);
    letter-spacing: 0.03em;
}
.tag.profile { color: var(--accent-hi); border-color: rgba(0,112,243,0.2); background: var(--accent-glow); }
.tag.country { color: #a78bfa; border-color: rgba(167,139,250,0.2); background: rgba(167,139,250,0.06); }

.rcard-snippet {
    font-size: 0.83rem;
    color: var(--text-2);
    line-height: 1.5;
    margin-bottom: 0.7rem;
}
.rcard-footer {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    padding-top: 0.7rem;
    border-top: 1px solid var(--border);
}
.rcard-footer-item {
    font-size: 0.78rem;
    color: var(--text-3);
    display: flex;
    align-items: center;
    gap: 5px;
}
.rcard-footer-item strong { color: var(--text-2); font-weight: 500; }
.rcard-footer-item .dot { color: var(--accent); }

/* Sidebar API section */
.api-status {
    display: flex;
    align-items: center;
    gap: 7px;
    font-family: 'GeistMono', monospace;
    font-size: 0.7rem;
    padding: 6px 10px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: var(--surface-2);
    margin-bottom: 5px;
    color: var(--text-3);
}
.api-status .dot-ok  { width:6px;height:6px;border-radius:50%;background:var(--green);flex-shrink:0; }
.api-status .dot-err { width:6px;height:6px;border-radius:50%;background:var(--red);flex-shrink:0; }
.api-status .dot-off { width:6px;height:6px;border-radius:50%;background:var(--text-3);flex-shrink:0; }

/* divider */
.vdivider { width:100%; height:1px; background:var(--border); margin:1rem 0; }

/* warning banner */
.warn-banner {
    background: rgba(243,18,96,0.06);
    border: 1px solid rgba(243,18,96,0.2);
    border-radius: var(--radius);
    padding: 0.7rem 1rem;
    font-size: 0.82rem;
    color: var(--red);
    font-family: 'GeistMono', monospace;
    margin-top: 0.5rem;
}

/* empty state */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: var(--text-3);
}
.empty-state-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.empty-state-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-2);
    margin-bottom: 0.4rem;
}
.empty-state-sub { font-size: 0.83rem; }

/* results summary bar */
.results-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
}
.results-count {
    font-family: 'GeistMono', monospace;
    font-size: 0.75rem;
    color: var(--text-2);
}
.results-count span { color: var(--text-1); font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
COUNTRIES = {
    "🇩🇪 Germany":  {"code": "de", "lang": "de", "label": "DE"},
    "🇮🇹 Italy":    {"code": "it", "lang": "it", "label": "IT"},
    "🇫🇷 France":   {"code": "fr", "lang": "fr", "label": "FR"},
    "🇪🇸 Spain":    {"code": "es", "lang": "es", "label": "ES"},
    "🇬🇧 UK":       {"code": "uk", "lang": "en", "label": "UK"},
    "🇵🇱 Poland":   {"code": "pl", "lang": "pl", "label": "PL"},
}

PROFILES = {
    "📝 Blogger": {
        "label": "Blogger",
        "queries": [
            '{keyword} blog {country}',
            'best {keyword} {country} blog review',
            '{keyword} recommendations blogger site:wordpress.com OR site:blogspot.com',
        ]
    },
    "📰 Journalist": {
        "label": "Journalist",
        "queries": [
            '{keyword} journalist {country}',
            '{keyword} article review journalist {country}',
            'site:linkedin.com {keyword} journalist {country}',
        ]
    },
    "🤳 Micro-influencer": {
        "label": "Micro-influencer",
        "queries": [
            '{keyword} influencer {country} site:instagram.com OR site:tiktok.com',
            '{keyword} micro influencer {country}',
            '{keyword} creator {country} collaboration',
        ]
    },
    "▶️ YouTuber": {
        "label": "YouTuber",
        "queries": [
            '{keyword} review {country} site:youtube.com',
            '{keyword} youtube channel {country}',
            '{keyword} youtuber {country} comparison',
        ]
    },
}

TOPICS = [
    "smartphones", "laptops", "headphones", "smart home",
    "tablets", "cameras", "TVs", "washing machines",
    "vacuum cleaners", "gaming peripherals",
]

# ─────────────────────────────────────────────
# I18N — bilingual EN/IT
# ─────────────────────────────────────────────
I18N = {
    "EN": {
        "sidebar_title":    "Idealo EEAT",
        "sidebar_sub":      "Outreach Discovery",
        "api_config":       "API Configuration",
        "api_note":         "Credentials are session-only — never stored.",
        "key_google":       "Google Custom Search API Key",
        "key_cse":          "Google CSE ID",
        "key_openai":       "OpenAI API Key",
        "search_settings":  "Search Settings",
        "results_per_q":    "Results per query",
        "delay":            "Delay between queries (s)",
        "min_eeat":         "Min EEAT score",
        "free_tier":        "Free tier · Google CSE: 100 req/day · GPT-4o-mini: ~$0.0001/result",
        "tab_search":       "⚡ Discovery",
        "tab_results":      "📊 Results",
        "tab_export":       "📤 Export",
        "countries":        "Target Countries",
        "profiles":         "Creator Profiles",
        "topics":           "Product Topics",
        "custom_kw":        "Custom keyword (optional)",
        "custom_ph":        "e.g. robot vacuum, e-bike...",
        "kpi_countries":    "Countries",
        "kpi_profiles":     "Profiles",
        "kpi_topics":       "Topics",
        "kpi_calls":        "Est. API calls",
        "warn_quota":       "⚠ Exceeds free tier (100/day) — reduce scope or split across days.",
        "run_btn":          "Run Discovery →",
        "missing":          "Missing:",
        "scanning":         "Scanning",
        "done_msg":         "Done — {n} candidates (EEAT ≥ {s})",
        "no_results":       "No results yet",
        "no_results_sub":   "Run a discovery search to find outreach candidates.",
        "filter_country":   "Country",
        "filter_profile":   "Profile",
        "filter_priority":  "Priority",
        "showing":          "Showing",
        "of":               "of",
        "candidates":       "candidates",
        "why":              "Why",
        "contact":          "Contact",
        "audience":         "Audience",
        "export_title":     "Export candidates",
        "export_btn":       "Download CSV",
        "preview":          "JSON preview (first 5)",
        "no_export":        "No data to export yet.",
        "status_ok":        "configured",
        "status_empty":     "not set",
    },
    "IT": {
        "sidebar_title":    "Idealo EEAT",
        "sidebar_sub":      "Outreach Discovery",
        "api_config":       "Configurazione API",
        "api_note":         "Le credenziali sono solo di sessione — mai salvate.",
        "key_google":       "Google Custom Search API Key",
        "key_cse":          "Google CSE ID",
        "key_openai":       "OpenAI API Key",
        "search_settings":  "Impostazioni Ricerca",
        "results_per_q":    "Risultati per query",
        "delay":            "Ritardo tra query (s)",
        "min_eeat":         "Score EEAT minimo",
        "free_tier":        "Free tier · Google CSE: 100 req/giorno · GPT-4o-mini: ~$0.0001/risultato",
        "tab_search":       "⚡ Discovery",
        "tab_results":      "📊 Risultati",
        "tab_export":       "📤 Esporta",
        "countries":        "Paesi Target",
        "profiles":         "Profili Creator",
        "topics":           "Topic di Prodotto",
        "custom_kw":        "Keyword personalizzata (opzionale)",
        "custom_ph":        "es. robot aspirapolvere, e-bike...",
        "kpi_countries":    "Paesi",
        "kpi_profiles":     "Profili",
        "kpi_topics":       "Topic",
        "kpi_calls":        "Stima chiamate API",
        "warn_quota":       "⚠ Supera il free tier (100/giorno) — riduci o suddividi su più giorni.",
        "run_btn":          "Avvia Discovery →",
        "missing":          "Mancante:",
        "scanning":         "Scansione",
        "done_msg":         "Completato — {n} candidati (EEAT ≥ {s})",
        "no_results":       "Nessun risultato",
        "no_results_sub":   "Avvia una ricerca per trovare candidati all'outreach.",
        "filter_country":   "Paese",
        "filter_profile":   "Profilo",
        "filter_priority":  "Priorità",
        "showing":          "Mostrati",
        "of":               "di",
        "candidates":       "candidati",
        "why":              "Motivazione",
        "contact":          "Contatto",
        "audience":         "Audience",
        "export_title":     "Esporta candidati",
        "export_btn":       "Scarica CSV",
        "preview":          "Anteprima JSON (primi 5)",
        "no_export":        "Nessun dato da esportare.",
        "status_ok":        "configurato",
        "status_empty":     "non impostato",
    }
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def google_search(query, api_key, cse_id, gl, hl, num=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "cx": cse_id, "q": query, "gl": gl, "hl": hl, "num": num}
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("items", [])
    except Exception as e:
        st.warning(f"Search error: {e}")
        return []


def score_with_gpt(client, result, profile, country, keyword):
    system_prompt = (
        "You are an EEAT outreach analyst for Idealo, Europe's leading price comparison platform. "
        "Evaluate web results to identify high-quality outreach candidates. "
        "Respond ONLY with valid JSON — no markdown, no explanation."
    )
    user_prompt = f"""Evaluate for outreach potential:
Profile: {profile} | Country: {country} | Topic: {keyword}
Title: {result.get('title','')}
URL: {result.get('link','')}
Snippet: {result.get('snippet','')}

Return JSON with keys:
eeat_score (0-100), relevance_score (0-100),
outreach_priority ("HIGH"|"MEDIUM"|"LOW"),
contact_hint (string), why (one sentence),
estimated_audience (string), content_type (string)"""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
            temperature=0.3, max_tokens=300,
        )
        raw = resp.choices[0].message.content.strip().replace("```json","").replace("```","").strip()
        return json.loads(raw)
    except Exception as e:
        return {"eeat_score":0,"relevance_score":0,"outreach_priority":"LOW",
                "contact_hint":"unknown","why":f"Error: {e}","estimated_audience":"unknown","content_type":"unknown"}


def build_query(template, keyword, country_label):
    return template.replace("{keyword}", keyword).replace("{country}", country_label)


def pill_class(score):
    if score >= 70: return "hi"
    if score >= 40: return "mid"
    return "lo"


def results_to_csv(results):
    if not results: return ""
    keys = ["title","url","snippet","profile","country","keyword",
            "eeat_score","relevance_score","outreach_priority",
            "contact_hint","estimated_audience","content_type","why"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=keys, extrasaction="ignore")
    w.writeheader(); w.writerows(results)
    return buf.getvalue()


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "all_results" not in st.session_state:
    st.session_state.all_results = []
if "lang" not in st.session_state:
    st.session_state.lang = "EN"


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # — Logo block —
    st.markdown("""
    <div class="sidebar-logo">
      <div class="sidebar-logo-mark">
        <div class="logo-dot"></div>
        <div class="logo-text">Idealo EEAT</div>
      </div>
      <div class="logo-sub">Outreach Discovery · v2</div>
    </div>
    """, unsafe_allow_html=True)

    # — Language toggle —
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        if st.button("🇬🇧 EN", use_container_width=True):
            st.session_state.lang = "EN"
    with lang_col2:
        if st.button("🇮🇹 IT", use_container_width=True):
            st.session_state.lang = "IT"

    L = I18N[st.session_state.lang]

    # ── Load from Streamlit secrets if available ──
    _secret_google = st.secrets.get("GOOGLE_API_KEY", "") if hasattr(st, "secrets") else ""
    _secret_cse    = st.secrets.get("GOOGLE_CSE_ID",  "") if hasattr(st, "secrets") else ""
    _secret_openai = st.secrets.get("OPENAI_API_KEY", "") if hasattr(st, "secrets") else ""

    st.markdown(f'<div class="section-label">{L["api_config"]}</div>', unsafe_allow_html=True)

    # Show note only if secrets are NOT already loaded
    if not (_secret_google and _secret_cse and _secret_openai):
        st.caption(L["api_note"])

    # If secret exists → show locked status, no input needed
    # If not → show text input for manual entry
    if _secret_google:
        google_api_key = _secret_google
        st.markdown(f'<div class="api-status"><div class="dot-ok"></div>Google CSE Key · via Secrets · {L["status_ok"]}</div>', unsafe_allow_html=True)
    else:
        google_api_key = st.text_input(L["key_google"], type="password", placeholder="AIza...", label_visibility="collapsed")
        st.markdown(f'<div class="api-status"><div class="{"dot-ok" if google_api_key else "dot-off"}"></div>Google CSE Key · {L["status_ok"] if google_api_key else L["status_empty"]}</div>', unsafe_allow_html=True)

    if _secret_cse:
        google_cse_id = _secret_cse
        st.markdown(f'<div class="api-status"><div class="dot-ok"></div>CSE ID · via Secrets · {L["status_ok"]}</div>', unsafe_allow_html=True)
    else:
        google_cse_id = st.text_input(L["key_cse"], placeholder="123:abc...", label_visibility="collapsed")
        st.markdown(f'<div class="api-status"><div class="{"dot-ok" if google_cse_id else "dot-off"}"></div>CSE ID · {L["status_ok"] if google_cse_id else L["status_empty"]}</div>', unsafe_allow_html=True)

    if _secret_openai:
        openai_api_key = _secret_openai
        st.markdown(f'<div class="api-status"><div class="dot-ok"></div>OpenAI Key · via Secrets · {L["status_ok"]}</div>', unsafe_allow_html=True)
    else:
        openai_api_key = st.text_input(L["key_openai"], type="password", placeholder="sk-...", label_visibility="collapsed")
        st.markdown(f'<div class="api-status"><div class="{"dot-ok" if openai_api_key else "dot-off"}"></div>OpenAI Key · {L["status_ok"] if openai_api_key else L["status_empty"]}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-label">{L["search_settings"]}</div>', unsafe_allow_html=True)

    results_per_query     = st.slider(L["results_per_q"],    1, 10,  5)
    delay_between_queries = st.slider(L["delay"],         0.5, 3.0, 1.0, 0.5)
    min_eeat_score        = st.slider(L["min_eeat"],        0,  80, 30)

    st.markdown(f'<div class="vdivider"></div><div style="font-family:GeistMono,monospace;font-size:0.65rem;color:var(--text-3);line-height:1.8">{L["free_tier"]}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
L = I18N[st.session_state.lang]

# Header
st.markdown(f"""
<div class="app-header">
  <div class="header-eyebrow">Idealo · EEAT Intelligence</div>
  <div class="header-title"><span>Outreach</span> Discovery</div>
  <div class="header-sub">AI-powered creator &amp; journalist discovery for link building — DE · IT · FR · ES · UK · PL</div>
  <div class="header-badges">
    <span class="header-badge">Blogger</span>
    <span class="header-badge">Journalist</span>
    <span class="header-badge">Micro-influencer</span>
    <span class="header-badge">YouTuber</span>
    <span class="header-badge">DE · IT · FR · ES · UK · PL</span>
  </div>
  <div class="header-badges" style="margin-top:6px">
    <span class="header-badge active">Powered by GPT-4o-mini</span>
    <span class="header-badge active">Google Custom Search</span>
    <span class="header-badge active">Budget zero</span>
  </div>
</div>
""", unsafe_allow_html=True)

tab_search, tab_results, tab_export = st.tabs([L["tab_search"], L["tab_results"], L["tab_export"]])

# ─────────────────────────────────────────────
# TAB 1 — DISCOVERY
# ─────────────────────────────────────────────
with tab_search:
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(f'<div class="section-label">{L["countries"]}</div>', unsafe_allow_html=True)
        selected_countries = st.multiselect(
            L["countries"], list(COUNTRIES.keys()),
            default=["🇩🇪 Germany", "🇮🇹 Italy"],
            label_visibility="collapsed",
        )
        st.markdown(f'<div class="section-label">{L["profiles"]}</div>', unsafe_allow_html=True)
        selected_profiles = st.multiselect(
            L["profiles"], list(PROFILES.keys()),
            default=["📝 Blogger", "▶️ YouTuber"],
            label_visibility="collapsed",
        )

    with col_right:
        st.markdown(f'<div class="section-label">{L["topics"]}</div>', unsafe_allow_html=True)
        selected_topics = st.multiselect(
            L["topics"], TOPICS,
            default=["smartphones", "laptops"],
            label_visibility="collapsed",
        )
        st.markdown(f'<div class="section-label">{L["custom_kw"]}</div>', unsafe_allow_html=True)
        custom_kw = st.text_input(L["custom_kw"], placeholder=L["custom_ph"], label_visibility="collapsed")

    all_topics    = selected_topics + ([custom_kw.strip()] if custom_kw.strip() else [])
    total_queries = len(selected_countries) * len(selected_profiles) * len(all_topics) * 3
    over_quota    = total_queries > 100

    # KPI grid
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">{L["kpi_countries"]}</div>
        <div class="kpi-value">{len(selected_countries)}</div>
        <div class="kpi-sub">{"·".join([COUNTRIES[c]["label"] for c in selected_countries]) or "—"}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">{L["kpi_profiles"]}</div>
        <div class="kpi-value">{len(selected_profiles)}</div>
        <div class="kpi-sub">{", ".join([PROFILES[p]["label"] for p in selected_profiles]) or "—"}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">{L["kpi_topics"]}</div>
        <div class="kpi-value">{len(all_topics)}</div>
        <div class="kpi-sub">{", ".join(all_topics[:3]) + ("…" if len(all_topics)>3 else "") if all_topics else "—"}</div>
      </div>
      <div class="kpi-card {'warn' if over_quota else ''}">
        <div class="kpi-label">{L["kpi_calls"]}</div>
        <div class="kpi-value {'warn' if over_quota else ''}">{total_queries}</div>
        <div class="kpi-sub">{"⚠ > 100 free/day" if over_quota else "✓ within free tier"}</div>
      </div>
    </div>
    {"<div class='warn-banner'>" + L['warn_quota'] + "</div>" if over_quota else ""}
    """, unsafe_allow_html=True)

    st.markdown("")
    run_col, _ = st.columns([1, 3])
    with run_col:
        run_search = st.button(L["run_btn"], use_container_width=True)

    # ── RUN ──
    if run_search:
        missing = []
        if not google_api_key: missing.append("Google API Key")
        if not google_cse_id:  missing.append("Google CSE ID")
        if not openai_api_key: missing.append("OpenAI API Key")
        if not selected_countries: missing.append("country")
        if not selected_profiles:  missing.append("profile")
        if not all_topics:         missing.append("topic")

        if missing:
            st.error(f"{L['missing']} {', '.join(missing)}")
        else:
            client     = OpenAI(api_key=openai_api_key)
            new_results = []
            progress_bar = st.progress(0)
            status_box   = st.empty()

            combos = [(c, p, t)
                      for c in selected_countries
                      for p in selected_profiles
                      for t in all_topics]

            for idx, (cn, pn, topic) in enumerate(combos):
                ci = COUNTRIES[cn]
                pi = PROFILES[pn]

                for q_tmpl in pi["queries"]:
                    query = build_query(q_tmpl, topic, ci["label"])
                    status_box.markdown(
                        f'<div style="font-family:GeistMono,monospace;font-size:0.75rem;'
                        f'color:var(--text-3);padding:0.4rem 0">'
                        f'<span style="color:var(--accent)">→</span> {L["scanning"]} · {query}</div>',
                        unsafe_allow_html=True
                    )

                    items = google_search(query, google_api_key, google_cse_id,
                                          gl=ci["code"], hl=ci["lang"], num=results_per_query)

                    for item in items:
                        ai = score_with_gpt(client, item, pi["label"], ci["label"], topic)
                        if ai.get("eeat_score", 0) >= min_eeat_score:
                            new_results.append({
                                "title":   item.get("title",""),
                                "url":     item.get("link",""),
                                "snippet": item.get("snippet",""),
                                "profile": pi["label"],
                                "country": ci["label"],
                                "keyword": topic,
                                **ai,
                            })
                    time.sleep(delay_between_queries)

                progress_bar.progress((idx + 1) / len(combos))

            st.session_state.all_results = new_results
            msg = L["done_msg"].format(n=len(new_results), s=min_eeat_score)
            status_box.success(f"✅ {msg}")
            st.balloons()


# ─────────────────────────────────────────────
# TAB 2 — RESULTS
# ─────────────────────────────────────────────
with tab_results:
    results = st.session_state.all_results

    if not results:
        st.markdown(f"""
        <div class="empty-state">
          <div class="empty-state-icon">⚡</div>
          <div class="empty-state-title">{L["no_results"]}</div>
          <div class="empty-state-sub">{L["no_results_sub"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Filter bar
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            filter_country  = st.multiselect(L["filter_country"],  sorted({r["country"] for r in results}))
        with fc2:
            filter_profile  = st.multiselect(L["filter_profile"],  sorted({r["profile"] for r in results}))
        with fc3:
            filter_priority = st.multiselect(L["filter_priority"], ["HIGH","MEDIUM","LOW"])

        filtered = results
        if filter_country:  filtered = [r for r in filtered if r["country"] in filter_country]
        if filter_profile:  filtered = [r for r in filtered if r["profile"] in filter_profile]
        if filter_priority: filtered = [r for r in filtered if r["outreach_priority"] in filter_priority]
        filtered = sorted(filtered, key=lambda x: x.get("eeat_score",0), reverse=True)

        # Summary + mini KPIs
        n_high = sum(1 for r in filtered if r.get("outreach_priority")=="HIGH")
        n_mid  = sum(1 for r in filtered if r.get("outreach_priority")=="MEDIUM")
        avg_eeat = round(sum(r.get("eeat_score",0) for r in filtered) / len(filtered)) if filtered else 0

        st.markdown(f"""
        <div class="kpi-grid" style="grid-template-columns:repeat(4,1fr)">
          <div class="kpi-card">
            <div class="kpi-label">Total</div>
            <div class="kpi-value" style="font-size:1.6rem">{len(filtered)}</div>
            <div class="kpi-sub">{L["candidates"]}</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">HIGH priority</div>
            <div class="kpi-value" style="font-size:1.6rem;color:var(--green)">{n_high}</div>
            <div class="kpi-sub">immediate outreach</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">MEDIUM priority</div>
            <div class="kpi-value" style="font-size:1.6rem;color:var(--amber)">{n_mid}</div>
            <div class="kpi-sub">secondary outreach</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-label">Avg EEAT Score</div>
            <div class="kpi-value" style="font-size:1.6rem">{avg_eeat}</div>
            <div class="kpi-sub">out of 100</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="results-bar">
          <div class="results-count">
            {L["showing"]} <span>{len(filtered)}</span> {L["of"]} {len(results)} {L["candidates"]}
          </div>
          <div style="font-family:GeistMono,monospace;font-size:0.68rem;color:var(--text-3)">
            sorted by EEAT ↓
          </div>
        </div>
        """, unsafe_allow_html=True)

        for r in filtered:
            eeat = r.get("eeat_score", 0)
            rel  = r.get("relevance_score", 0)
            prio = r.get("outreach_priority", "LOW")
            url  = r.get("url","")
            snippet = r.get("snippet","")

            st.markdown(f"""
<div class="rcard">
  <div class="rcard-top">
    <div style="min-width:0">
      <a class="rcard-title" href="{url}" target="_blank">{r.get('title','—')}</a>
      <div class="rcard-url">{url[:90]}{'…' if len(url)>90 else ''}</div>
    </div>
    <div class="rcard-scores">
      <span class="score-pill {pill_class(eeat)}">EEAT {eeat}</span>
      <span class="score-pill {pill_class(rel)}">REL {rel}</span>
      <span class="prio-pill prio-{prio}">{prio}</span>
    </div>
  </div>
  <div class="rcard-meta">
    <span class="tag profile">{r.get('profile','')}</span>
    <span class="tag country">{r.get('country','')}</span>
    <span class="tag">{r.get('keyword','')}</span>
    <span class="tag">{r.get('content_type','')}</span>
  </div>
  <div class="rcard-snippet">{snippet[:200]}{'…' if len(snippet)>200 else ''}</div>
  <div class="rcard-footer">
    <div class="rcard-footer-item">
      <span class="dot">💬</span>
      <strong>{L["why"]}:</strong> {r.get('why','')}
    </div>
    <div class="rcard-footer-item">
      <span class="dot">📨</span>
      <strong>{L["contact"]}:</strong> {r.get('contact_hint','')}
    </div>
    <div class="rcard-footer-item">
      <span class="dot">👥</span>
      <strong>{L["audience"]}:</strong> {r.get('estimated_audience','?')}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TAB 3 — EXPORT
# ─────────────────────────────────────────────
with tab_export:
    results = st.session_state.all_results

    if not results:
        st.markdown(f"""
        <div class="empty-state">
          <div class="empty-state-icon">📤</div>
          <div class="empty-state-title">{L["no_export"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="section-label">{L["export_title"]} · {len(results)} rows</div>', unsafe_allow_html=True)

        csv_data = results_to_csv(results)
        st.download_button(
            label=f"⬇ {L['export_btn']}",
            data=csv_data,
            file_name="idealo_eeat_outreach.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown(f'<div class="section-label" style="margin-top:1.5rem">{L["preview"]}</div>', unsafe_allow_html=True)
        st.json(results[:5])
