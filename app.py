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
    --text-3:      #8892aa;
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
    color: var(--text-2);
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

/* Section label */
.section-label {
    font-family: 'GeistMono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--text-2);
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
    color: var(--text-2);
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
    color: var(--text-2);
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
    color: var(--text-2);
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
    color: var(--text-2);
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
    color: var(--text-2);
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
    color: var(--text-2);
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
    color: var(--text-2);
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

# Localized query terms per country
COUNTRY_TERMS = {
    "DE": {"review": "Test Erfahrung", "blog": "Blog Testbericht", "unboxing": "Unboxing Test",
           "best": "bester", "analysis": "Analyse", "journalist": "Journalist Redakteur",
           "influencer": "Influencer Creator", "creator": "Creator"},
    "IT": {"review": "recensione", "blog": "blog recensione", "unboxing": "unboxing recensione",
           "best": "migliori", "analysis": "analisi", "journalist": "giornalista redattore",
           "influencer": "influencer creator", "creator": "creator"},
    "FR": {"review": "avis test", "blog": "blog avis", "unboxing": "déballage test",
           "best": "meilleur", "analysis": "analyse", "journalist": "journaliste rédacteur",
           "influencer": "influenceur créateur", "creator": "créateur"},
    "ES": {"review": "reseña análisis", "blog": "blog reseña", "unboxing": "unboxing reseña",
           "best": "mejores", "analysis": "análisis", "journalist": "periodista redactor",
           "influencer": "influencer creador", "creator": "creador"},
    "UK": {"review": "review", "blog": "blog review", "unboxing": "unboxing review",
           "best": "best", "analysis": "analysis", "journalist": "journalist editor",
           "influencer": "influencer creator", "creator": "creator"},
    "PL": {"review": "recenzja opinia", "blog": "blog recenzja", "unboxing": "unboxing recenzja",
           "best": "najlepszy", "analysis": "analiza", "journalist": "dziennikarz redaktor",
           "influencer": "influencer twórca", "creator": "twórca"},
}

def localize_query(template, keyword, country_label):
    t = COUNTRY_TERMS.get(country_label, COUNTRY_TERMS["UK"])
    q = template
    for k, v in t.items():
        q = q.replace("{"+k+"}", v)
    q = q.replace("{keyword}", keyword).replace("{country}", country_label)
    return q

PROFILES = {
    "📝 Blogger": {
        "label": "Blogger",
        "queries": [
            'site:wordpress.com {keyword} {review} {country}',
            'site:blogspot.com {keyword} {blog} {country}',
            '{keyword} {review} blog personal {country} -nytimes.com -forbes.com -bbc.com -spiegel.de -elmundo.es',
        ]
    },
    "📰 Journalist": {
        "label": "Journalist",
        "queries": [
            'site:linkedin.com/in {keyword} {journalist} {country}',
            'site:linkedin.com/in {keyword} tecnologia {journalist} {country}',
            'site:muck-rack.com {keyword} {country}',
        ]
    },
    "🤳 TikToker / Instagram": {
        "label": "TikToker/Instagram",
        "queries": [
            'site:tiktok.com {keyword} {country}',
            'site:instagram.com {keyword} {unboxing} {country}',
            'site:tiktok.com {keyword} {unboxing}',
        ]
    },
    "▶️ YouTuber": {
        "label": "YouTuber",
        "queries": [
            'site:youtube.com {keyword} {review} {country}',
            'site:youtube.com {keyword} {unboxing} {country}',
            'site:youtube.com {keyword} {best} {country} 2024',
        ]
    },
    "💼 LinkedIn Creator": {
        "label": "LinkedIn Creator",
        "queries": [
            'site:linkedin.com/in {keyword} {influencer} {country}',
            'site:linkedin.com/pulse {keyword} {country}',
            'site:linkedin.com {keyword} "top voice" {country}',
        ]
    },
}

TOPICS = [
    "smartphones", "laptops", "headphones", "smart home",
    "tablets", "cameras", "TVs", "washing machines",
    "vacuum cleaners", "gaming peripherals",
]

DEFAULT_BLACKLIST = [
    "nytimes.com","forbes.com","bbc.com","theguardian.com","reuters.com",
    "wikipedia.org","amazon.com","amazon.de","amazon.es","amazon.it","amazon.fr",
    "elmundo.es","elpais.com","marca.com","as.com","20minutos.es",
    "lavanguardia.com","abc.es","spiegel.de","bild.de","faz.net","focus.de",
    "corriere.it","repubblica.it","gazzetta.it","lefigaro.fr","lemonde.fr",
    "rtl.de","sat1.de","pro7.de","ebay.com","ebay.de","mediamarkt.de",
    "mediaworld.it","fnac.es","pccomponentes.com","idealo.de","idealo.es",
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
        "key_cse":          "",
        "key_openai":       "OpenAI API Key",
        "search_settings":  "Search Settings",
        "results_per_q":    "Results per query",
        "delay":            "Delay between queries (s)",
        "min_eeat":         "Min EEAT score",
        "free_tier":        "Free tier · Tavily: 1,000 req/month · GPT-4o-mini: ~$0.0001/result",
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
    "ES": {
        "sidebar_title":    "Idealo EEAT",
        "sidebar_sub":      "Outreach Discovery",
        "api_config":       "Configuración API",
        "api_note":         "Las credenciales son solo de sesión — nunca almacenadas.",
        "key_google":       "Tavily API Key",
        "key_cse":          "",
        "key_openai":       "OpenAI API Key",
        "search_settings":  "Ajustes de Búsqueda",
        "results_per_q":    "Resultados por consulta",
        "delay":            "Pausa entre consultas (s)",
        "min_eeat":         "Score EEAT mínimo",
        "free_tier":        "Free tier · Tavily: 1.000 req/mes · GPT-4o-mini: ~$0.0001/resultado",
        "tab_search":       "⚡ Discovery",
        "tab_results":      "📊 Resultados",
        "tab_export":       "📤 Exportar",
        "countries":        "Países objetivo",
        "profiles":         "Perfiles de creador",
        "topics":           "Temas de producto",
        "custom_kw":        "Palabra clave personalizada (opcional)",
        "custom_ph":        "ej. robot aspirador, e-bike...",
        "kpi_countries":    "Países",
        "kpi_profiles":     "Perfiles",
        "kpi_topics":       "Temas",
        "kpi_calls":        "Llamadas API estimadas",
        "warn_quota":       "⚠ Lote grande — considera dividir la búsqueda en sesiones.",
        "run_btn":          "Iniciar Discovery →",
        "missing":          "Falta:",
        "scanning":         "Escaneando",
        "done_msg":         "Completado — {n} candidatos (EEAT ≥ {s})",
        "no_results":       "Sin resultados",
        "no_results_sub":   "Inicia una búsqueda para encontrar candidatos de outreach.",
        "filter_country":   "País",
        "filter_profile":   "Perfil",
        "filter_priority":  "Prioridad",
        "showing":          "Mostrando",
        "of":               "de",
        "candidates":       "candidatos",
        "why":              "Por qué",
        "contact":          "Contacto",
        "audience":         "Audiencia",
        "export_title":     "Exportar candidatos",
        "export_btn":       "Descargar CSV",
        "preview":          "Vista previa JSON (primeros 5)",
        "no_export":        "Sin datos para exportar.",
        "status_ok":        "configurado",
        "status_empty":     "no configurado",
    }
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def tavily_search(query, api_key, country_code, num=5):
    """Call Tavily Search API — AI-native search, free tier 1000 req/month."""
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": num,
        "include_answer": False,
        "include_raw_content": False,
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        r.raise_for_status()
        raw = r.json().get("results", [])
        # Normalize to same shape used downstream
        return [{"title": x.get("title",""), "link": x.get("url",""), "snippet": x.get("content","")} for x in raw]
    except Exception as e:
        st.warning(f"Tavily search error: {e}")
        return []

def get_youtube_stats(video_or_channel_url: str, yt_api_key: str) -> dict:
    """Fetch real view/subscriber counts from YouTube Data API v3."""
    import re
    if not yt_api_key:
        return {"yt_views": None, "yt_subscribers": None, "yt_video_count": None}
    try:
        # Channel handle or /c/ or /channel/
        ch_match = re.search(r"youtube\.com/(?:@|c/|channel/)([\w\-]+)", video_or_channel_url)
        vid_match = re.search(r"(?:v=|youtu\.be/)([\w\-]{11})", video_or_channel_url)
        base = "https://www.googleapis.com/youtube/v3"

        if ch_match:
            handle = ch_match.group(1)
            # Try forHandle first, fallback to search
            r = requests.get(f"{base}/channels", params={
                "key": yt_api_key, "forHandle": handle,
                "part": "statistics", "maxResults": 1
            }, timeout=8)
            items = r.json().get("items", [])
            if not items:
                r2 = requests.get(f"{base}/search", params={
                    "key": yt_api_key, "q": handle,
                    "type": "channel", "part": "snippet", "maxResults": 1
                }, timeout=8)
                ch_id = r2.json().get("items", [{}])[0].get("id", {}).get("channelId","")
                if ch_id:
                    r3 = requests.get(f"{base}/channels", params={
                        "key": yt_api_key, "id": ch_id, "part": "statistics"
                    }, timeout=8)
                    items = r3.json().get("items", [])
            if items:
                stats = items[0].get("statistics", {})
                return {
                    "yt_views":       int(stats.get("viewCount", 0)),
                    "yt_subscribers": int(stats.get("subscriberCount", 0)),
                    "yt_video_count": int(stats.get("videoCount", 0)),
                }

        elif vid_match:
            vid_id = vid_match.group(1)
            r = requests.get(f"{base}/videos", params={
                "key": yt_api_key, "id": vid_id,
                "part": "statistics,snippet", "maxResults": 1
            }, timeout=8)
            items = r.json().get("items", [])
            if items:
                stats = items[0].get("statistics", {})
                return {
                    "yt_views":       int(stats.get("viewCount", 0)),
                    "yt_subscribers": None,
                    "yt_video_count": None,
                }
    except Exception:
        pass
    return {"yt_views": None, "yt_subscribers": None, "yt_video_count": None}


def audience_to_num(audience_str: str) -> int:
    """Convert GPT audience estimate like '10k-50k' to a sortable integer (lower bound)."""
    if not audience_str or audience_str.lower() in ("unknown", "?", ""):
        return 0
    import re
    s = audience_str.lower().replace(",", "").replace(".", "")
    nums = re.findall(r"(\d+)(k|m)?", s)
    if not nums:
        return 0
    n, unit = nums[0]
    val = int(n)
    if unit == "k": val *= 1_000
    if unit == "m": val *= 1_000_000
    return val




def score_with_gpt(client, result, profile, country, keyword):
    system_prompt = (
        "You are an EEAT outreach analyst for Idealo, Europe's leading price comparison platform. "
        "Evaluate web results to identify high-quality outreach candidates. "
        "Respond ONLY with valid JSON — no markdown, no explanation."
    )
    url_val = result.get('link','')
    is_generic_media = any(d in url_val for d in [
        'nytimes.com','forbes.com','bbc.com','theguardian.com','reuters.com',
        'wikipedia.org','amazon.com','elmundo.es','elpais.com','marca.com',
        'as.com','20minutos.es','lavanguardia.com','abc.es'
    ])
    penalty_note = " IMPORTANT: This URL is from a major news outlet or generic site — score eeat_score MAX 15 and outreach_priority LOW." if is_generic_media else ""
    user_prompt = f"""You are evaluating outreach candidates for Idealo (price comparison). 
We want INDIVIDUAL creators: bloggers with personal sites, YouTubers with channels, TikTokers, Instagram creators, LinkedIn influencers.
We do NOT want: news outlets, corporate sites, Wikipedia, aggregators, e-commerce sites.{penalty_note}

Profile: {profile} | Country: {country} | Topic: {keyword}
Title: {result.get('title','')}
URL: {url_val}
Snippet: {result.get('snippet','')}

Return JSON only:
eeat_score (0-100), relevance_score (0-100),
outreach_priority ("HIGH"|"MEDIUM"|"LOW"),
contact_hint (string), why (one sentence max),
estimated_audience (string like "5k-20k"), content_type (string)"""
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
    return localize_query(template, keyword, country_label)


def generate_outreach_email(client, result: dict, lang: str) -> str:
    lang_instruction = "Write in Spanish." if lang == "ES" else "Write in English."
    prompt = f"""{lang_instruction}
Write a short, personalized outreach email from Idealo (Europe's leading price comparison platform) to this creator/journalist.
Be concise, friendly, professional. Max 120 words. No subject line needed here — just the email body.

Creator profile: {result.get('profile','')}
Country: {result.get('country','')}
Topic: {result.get('keyword','')}
Their site/channel: {result.get('url','')}
Title: {result.get('title','')}
Estimated audience: {result.get('estimated_audience','')}
Why good fit: {result.get('why','')}

Focus on: mutual value, their audience relevance to Idealo, specific collaboration idea (sponsored post, product review, affiliate link, etc)."""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.7, max_tokens=200,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating email: {e}"



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
if "speed" not in st.session_state:
    st.session_state.speed = "Normal"
if "blacklist" not in st.session_state:
    st.session_state.blacklist = list(DEFAULT_BLACKLIST)
if "seen_urls" not in st.session_state:
    st.session_state.seen_urls = set()
if "generated_emails" not in st.session_state:
    st.session_state.generated_emails = {}


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
        if st.button("🇪🇸 ES", use_container_width=True):
            st.session_state.lang = "ES"

    L = I18N.get(st.session_state.lang, I18N["EN"])

    # ── Load from Streamlit secrets if available ──
    _secret_google = st.secrets.get("TAVILY_API_KEY", "") if hasattr(st, "secrets") else ""
    _secret_cse    = ""  # not used with Tavily
    _secret_openai = st.secrets.get("OPENAI_API_KEY", "") if hasattr(st, "secrets") else ""
    _secret_yt     = st.secrets.get("YOUTUBE_API_KEY", "") if hasattr(st, "secrets") else ""

    st.markdown(f'<div class="section-label">{L["api_config"]}</div>', unsafe_allow_html=True)

    # Show note only if secrets are NOT already loaded
    if not (_secret_google and _secret_cse and _secret_openai):
        st.caption(L["api_note"])

    # If secret exists → show locked status, no input needed
    # If not → show text input for manual entry
    if _secret_google:
        google_api_key = _secret_google
        st.markdown(f'<div class="api-status"><div class="dot-ok"></div>Tavily Key · via Secrets · {L["status_ok"]}</div>', unsafe_allow_html=True)
    else:
        google_api_key = st.text_input(L["key_google"], type="password", placeholder="AIza...", label_visibility="collapsed")
        st.markdown(f'<div class="api-status"><div class="{"dot-ok" if google_api_key else "dot-off"}"></div>Tavily Key · {L["status_ok"] if google_api_key else L["status_empty"]}</div>', unsafe_allow_html=True)

    google_cse_id = ""  # Tavily does not need CSE ID

    if _secret_openai:
        openai_api_key = _secret_openai
        st.markdown(f'<div class="api-status"><div class="dot-ok"></div>OpenAI Key · via Secrets · {L["status_ok"]}</div>', unsafe_allow_html=True)
    else:
        openai_api_key = st.text_input(L["key_openai"], type="password", placeholder="sk-...", label_visibility="collapsed")
        st.markdown(f'<div class="api-status"><div class="{"dot-ok" if openai_api_key else "dot-off"}"></div>OpenAI Key · {L["status_ok"] if openai_api_key else L["status_empty"]}</div>', unsafe_allow_html=True)

    if _secret_yt:
        yt_api_key = _secret_yt
        st.markdown(f'<div class="api-status"><div class="dot-ok"></div>YouTube API · via Secrets · {L["status_ok"]}</div>', unsafe_allow_html=True)
    else:
        yt_api_key = st.text_input("YouTube Data API Key (optional)", type="password", placeholder="AIza...", label_visibility="collapsed")
        st.markdown(f'<div class="api-status"><div class="{"dot-ok" if yt_api_key else "dot-off"}"></div>YouTube API · {"real stats" if yt_api_key else "GPT estimate only"}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-label">{L["search_settings"]}</div>', unsafe_allow_html=True)

    speed_label = {"EN": ["⚡ Fast", "⚖ Normal", "🔍 Deep"], "ES": ["⚡ Rápido", "⚖ Normal", "🔍 Profundo"]}.get(st.session_state.lang, ["⚡ Fast", "⚖ Normal", "🔍 Deep"])
    speed = st.radio("Speed", speed_label, index=1, horizontal=True, label_visibility="collapsed")
    SPEED_PRESETS = {
        speed_label[0]: {"results_per_query": 3,  "delay": 0.5, "min_eeat": 40},
        speed_label[1]: {"results_per_query": 5,  "delay": 1.0, "min_eeat": 30},
        speed_label[2]: {"results_per_query": 10, "delay": 1.5, "min_eeat": 20},
    }
    preset = SPEED_PRESETS.get(speed, SPEED_PRESETS[speed_label[1]])
    results_per_query     = preset["results_per_query"]
    delay_between_queries = preset["delay"]
    min_eeat_score        = preset["min_eeat"]

    speed_desc = {
        speed_label[0]: "3 results · 0.5s delay · EEAT ≥ 40",
        speed_label[1]: "5 results · 1.0s delay · EEAT ≥ 30",
        speed_label[2]: "10 results · 1.5s delay · EEAT ≥ 20",
    }
    st.markdown(f'<div style="font-family:GeistMono,monospace;font-size:0.68rem;color:var(--text-2);padding:4px 0 8px">{speed_desc[speed]}</div>', unsafe_allow_html=True)
    min_eeat_score = st.slider(L["min_eeat"], 0, 80, min_eeat_score)

    st.markdown(f'<div class="vdivider"></div><div style="font-family:GeistMono,monospace;font-size:0.65rem;color:var(--text-3);line-height:1.8">{L["free_tier"]}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
L = I18N.get(st.session_state.lang, I18N["EN"])

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
    <span class="header-badge active">Tavily Search</span>
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
            default=["🇪🇸 Spain"],
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
    over_quota    = total_queries > 200

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
        <div class="kpi-sub">{"⚠ > 200 recommended" if over_quota else "✓ within free tier"}</div>
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
        if not google_api_key: missing.append("Tavily API Key")
        if not openai_api_key: missing.append("OpenAI API Key")
        if not selected_countries: missing.append("country")
        if not selected_profiles:  missing.append("profile")
        if not all_topics:         missing.append("topic")

        if missing:
            st.error(f"{L['missing']} {', '.join(missing)}")
        else:
            client     = OpenAI(api_key=openai_api_key)
            new_results = []
            seen_urls   = set()  # deduplication within this run
            blacklist   = st.session_state.blacklist
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

                    items = tavily_search(query, google_api_key, ci["code"], num=results_per_query)

                    for item in items:
                        item_url_raw = item.get("link","").split("?")[0].rstrip("/")
                        # Skip duplicates
                        if item_url_raw in seen_urls:
                            continue
                        seen_urls.add(item_url_raw)
                        # Skip blacklisted domains
                        item_domain = item_url_raw.replace("https://","").replace("http://","").split("/")[0].replace("www.","")
                        if any(bl in item_domain for bl in blacklist):
                            continue
                        ai = score_with_gpt(client, item, pi["label"], ci["label"], topic)
                        if ai.get("eeat_score", 0) >= min_eeat_score:
                            item_url = item_url_raw
                            yt_stats = {}
                            if "youtube.com" in item_url and yt_api_key:
                                yt_stats = get_youtube_stats(item_url, yt_api_key)
                            audience_num = yt_stats.get("yt_subscribers") or yt_stats.get("yt_views") or audience_to_num(ai.get("estimated_audience",""))
                            new_results.append({
                                "title":        item.get("title",""),
                                "url":          item_url,
                                "snippet":      item.get("snippet",""),
                                "profile":      pi["label"],
                                "country":      ci["label"],
                                "keyword":      topic,
                                "audience_num": audience_num,
                                **yt_stats,
                                **ai,
                            })
                    time.sleep(delay_between_queries)

                progress_bar.progress((idx + 1) / len(combos))

            st.session_state.all_results = new_results
            st.session_state.generated_emails = {}
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

        # Audience filter
        aud_col1, aud_col2 = st.columns([2,1])
        with aud_col1:
            AUDIENCE_TIERS = {
                "Any": 0,
                "Micro (1k+)": 1_000,
                "Small (10k+)": 10_000,
                "Medium (50k+)": 50_000,
                "Large (100k+)": 100_000,
                "Mega (500k+)": 500_000,
            }
            aud_filter_label = st.select_slider(
                "Min audience / subscribers",
                options=list(AUDIENCE_TIERS.keys()),
                value="Any",
            )
        with aud_col2:
            sort_by = st.selectbox("Sort by", ["EEAT score", "Audience", "Relevance"], label_visibility="visible")

        min_audience = AUDIENCE_TIERS[aud_filter_label]

        filtered = results
        if filter_country:  filtered = [r for r in filtered if r["country"] in filter_country]
        if filter_profile:  filtered = [r for r in filtered if r["profile"] in filter_profile]
        if filter_priority: filtered = [r for r in filtered if r["outreach_priority"] in filter_priority]
        if min_audience > 0:
            filtered = [r for r in filtered if r.get("audience_num", 0) >= min_audience]
        sort_key = {"EEAT score": "eeat_score", "Audience": "audience_num", "Relevance": "relevance_score"}[sort_by]
        filtered = sorted(filtered, key=lambda x: x.get(sort_key, 0), reverse=True)

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
      <strong>{L["audience"]}:</strong> {"▶ {:,} subs · {:,} views".format(r["yt_subscribers"], r["yt_views"]) if r.get("yt_subscribers") else r.get("estimated_audience","?")}
    </div>{
  ('<div class="rcard-footer-item"><span class="dot">🎬</span><strong>Videos:</strong> {:,}</div>'.format(r["yt_video_count"]) if r.get("yt_video_count") else "")
}  </div>
</div>
""", unsafe_allow_html=True)
            # Email generator button
            card_id = r.get("url","")
            col_btn, col_spacer = st.columns([1, 3])
            with col_btn:
                if st.button(f"✉ Generate outreach email", key=f"email_{card_id}"):
                    with st.spinner("Writing email..."):
                        _client_mail = OpenAI(api_key=openai_api_key)
                        email_text = generate_outreach_email(_client_mail, r, st.session_state.lang)
                        st.session_state.generated_emails[card_id] = email_text
            if card_id in st.session_state.generated_emails:
                st.markdown(f"""
<div style="background:var(--surface-2);border:1px solid var(--border);border-left:3px solid var(--accent);
border-radius:6px;padding:1rem 1.2rem;margin:0.3rem 0 0.8rem;
font-family:Outfit,sans-serif;font-size:0.84rem;color:var(--text-2);line-height:1.6;white-space:pre-wrap">{st.session_state.generated_emails[card_id]}</div>
""", unsafe_allow_html=True)
                st.code(st.session_state.generated_emails[card_id], language=None)


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
