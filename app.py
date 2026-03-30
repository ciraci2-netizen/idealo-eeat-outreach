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
    page_title="Idealo EEAT Outreach Discovery",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg: #0d0d0d;
    --surface: #161616;
    --border: #2a2a2a;
    --accent: #ff6b2b;
    --accent2: #ffb347;
    --text: #e8e8e8;
    --muted: #666;
    --green: #22c55e;
    --blue: #3b82f6;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; letter-spacing: -0.02em; }

.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important;
    padding: 0.6rem 1.4rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--accent2) !important;
    transform: translateY(-1px) !important;
}

.stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 6px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.result-card:hover { border-left-color: var(--accent2); }

.profile-tag {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 2px 8px;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--accent);
    margin-right: 6px;
    margin-bottom: 4px;
}

.country-tag {
    display: inline-block;
    background: #0a1628;
    border: 1px solid #1e3a5f;
    border-radius: 3px;
    padding: 2px 8px;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--blue);
    margin-right: 6px;
}

.score-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 3px;
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    font-weight: 500;
}
.score-high { background: #052e16; color: var(--green); border: 1px solid #166534; }
.score-mid  { background: #1c1307; color: var(--accent2); border: 1px solid #92400e; }
.score-low  { background: #1a0a0a; color: #ef4444; border: 1px solid #7f1d1d; }

.mono { font-family: 'DM Mono', monospace; font-size: 0.85rem; color: var(--muted); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────
COUNTRIES = {
    "🇩🇪 Germany (DE)": {"code": "de", "lang": "de", "label": "DE"},
    "🇮🇹 Italy (IT)":   {"code": "it", "lang": "it", "label": "IT"},
    "🇫🇷 France (FR)":  {"code": "fr", "lang": "fr", "label": "FR"},
    "🇪🇸 Spain (ES)":   {"code": "es", "lang": "es", "label": "ES"},
    "🇬🇧 UK (UK)":      {"code": "uk", "lang": "en", "label": "UK"},
    "🇵🇱 Poland (PL)":  {"code": "pl", "lang": "pl", "label": "PL"},
}

PROFILES = {
    "📝 Blogger": {
        "label": "Blogger",
        "queries": [
            '{keyword} blog {country}',
            'best {keyword} {country} blog review',
            '{keyword} recommendations blogger review',
        ]
    },
    "📰 Journalist": {
        "label": "Journalist",
        "queries": [
            '{keyword} journalist {country}',
            '{keyword} article review {country}',
            '{keyword} journalist news {country}',
        ]
    },
    "🤳 Micro-influencer": {
        "label": "Micro-influencer",
        "queries": [
            '{keyword} influencer {country}',
            '{keyword} micro influencer',
            '{keyword} creator collaboration',
        ]
    },
    "▶️ YouTuber": {
        "label": "YouTuber",
        "queries": [
            '{keyword} review youtube',
            '{keyword} youtube channel',
            '{keyword} youtuber comparison',
        ]
    },
}

TOPICS = [
    "smartphones",
    "laptops",
    "headphones",
    "smart home",
    "tablets",
    "cameras",
    "TVs",
    "washing machines",
    "vacuum cleaners",
    "gaming peripherals",
]

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def tavily_search(query: str, api_key: str, num: int = 5) -> list:
    """Call Tavily Search API."""
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "max_results": num,
            "include_answer": True,
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = []
        for result in data.get("results", []):
            results.append({
                "title": result.get("title", ""),
                "link": result.get("url", ""),
                "snippet": result.get("content", ""),
            })
        return results
    except Exception as e:
        st.warning(f"Tavily search error: {e}")
        return []


def score_with_gpt(
    client: OpenAI,
    result: dict,
    profile: str,
    country: str,
    keyword: str,
) -> dict:
    """Use GPT-4o-mini to score & enrich a search result for EEAT outreach."""
    system_prompt = """You are an EEAT outreach analyst for Idealo, Europe's leading price comparison platform.
Evaluate web results to identify high-quality outreach candidates (bloggers, journalists, micro-influencers, YouTubers).

Respond ONLY with valid JSON — no markdown, no explanation."""

    user_prompt = f"""Evaluate this result for outreach potential:

Profile type: {profile}
Target country: {country}
Keyword topic: {keyword}

Result:
- Title: {result.get('title', '')}
- URL: {result.get('link', '')}
- Snippet: {result.get('snippet', '')}

Return JSON with these exact keys:
{{
  "eeat_score": <integer 0-100>,
  "relevance_score": <integer 0-100>,
  "outreach_priority": "HIGH" | "MEDIUM" | "LOW",
  "contact_hint": "<guessed contact method or page>",
  "why": "<one sentence why this is good/bad>",
  "estimated_audience": "<e.g. '10k-50k', 'unknown', '1M+'>",
  "content_type": "<e.g. 'review blog', 'news article', 'YouTube channel'>"
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=300,
        )
        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except Exception as e:
        return {
            "eeat_score": 0,
            "relevance_score": 0,
            "outreach_priority": "LOW",
            "contact_hint": "unknown",
            "why": f"Parsing error: {e}",
            "estimated_audience": "unknown",
            "content_type": "unknown",
        }


# ─────────────────────────────────────────────
# SIDEBAR — CONFIG
# ─────────────────────────────────────────────
st.sidebar.title("⚙️ Configuration")

# API Keys
st.sidebar.subheader("🔑 API Keys")
tavily_key = st.sidebar.text_input(
    "Tavily API Key",
    value=st.secrets.get("TAVILY_API_KEY", ""),
    type="password",
    help="Get from tavily.com"
)

openai_key = st.sidebar.text_input(
    "OpenAI API Key",
    value=st.secrets.get("OPENAI_API_KEY", ""),
    type="password",
    help="Get from platform.openai.com"
)

if not tavily_key or not openai_key:
    st.sidebar.warning("⚠️ Missing API keys! Fill them in to proceed.")
    st.stop()

# Search Config
st.sidebar.subheader("🎯 Search Config")
selected_countries = st.sidebar.multiselect(
    "Countries",
    list(COUNTRIES.keys()),
    default=list(COUNTRIES.keys())[:2],
)

selected_profiles = st.sidebar.multiselect(
    "Profiles",
    list(PROFILES.keys()),
    default=list(PROFILES.keys())[:2],
)

selected_topics = st.sidebar.multiselect(
    "Topics",
    TOPICS,
    default=TOPICS[:3],
)

# Speed Mode
st.sidebar.subheader("⚡ Speed")
speed_mode = st.sidebar.radio(
    "Search Mode",
    ["🚀 Fast (1-2 min)", "⚙️ Normal (5-10 min)", "🔬 Thorough (15+ min)"],
    index=0,
)

# Set parameters based on speed
if "Fast" in speed_mode:
    queries_per_combo = 1
    results_per_query = 3
elif "Normal" in speed_mode:
    queries_per_combo = 3
    results_per_query = 5
else:  # Thorough
    queries_per_combo = 3
    results_per_query = 10

# ─────────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────────
st.title("🔍 Idealo EEAT Outreach Discovery")
st.markdown("Find high-quality, EEAT-optimized outreach candidates")

# Query Estimation
num_countries = len(selected_countries)
num_profiles = len(selected_profiles)
num_topics = len(selected_topics)
total_queries = num_countries * num_profiles * num_topics * queries_per_combo

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Countries", num_countries)
with col2:
    st.metric("Profiles", num_profiles)
with col3:
    st.metric("Est. Queries", total_queries)

if total_queries > 100:
    st.warning(f"⚠️ This will use ~{total_queries} Tavily credits (free tier: 1000/month)")

# ─────────────────────────────────────────────
# EXECUTE SEARCH
# ─────────────────────────────────────────────
if st.button("🚀 Start Discovery", type="primary"):
    results_data = []
    progress_bar = st.progress(0)
    status = st.status("Running discovery...", expanded=True)
    
    client = OpenAI(api_key=openai_key)
    
    total_steps = num_countries * num_profiles * num_topics * queries_per_combo
    step = 0
    
    for country_name in selected_countries:
        for profile_name in selected_profiles:
            for topic in selected_topics:
                profile_obj = PROFILES[profile_name]
                country_obj = COUNTRIES[country_name]
                
                for query_template in profile_obj["queries"][:queries_per_combo]:
                    step += 1
                    progress_pct = step / total_steps
                    progress_bar.progress(progress_pct)
                    
                    # Build query
                    query = query_template.format(
                        keyword=topic,
                        country=country_obj["label"]
                    )
                    
                    status.write(f"🔍 {country_name} → {profile_name} → {topic}")
                    status.write(f"Query: *{query}*")
                    
                    # Search
                    search_results = tavily_search(query, tavily_key, num=results_per_query)
                    
                    # Score each result
                    for i, result in enumerate(search_results):
                        score = score_with_gpt(
                            client, result, profile_name, country_obj["label"], topic
                        )
                        
                        results_data.append({
                            "country": country_obj["label"],
                            "profile": profile_name,
                            "topic": topic,
                            "title": result["title"],
                            "url": result["link"],
                            "snippet": result["snippet"],
                            "eeat_score": score["eeat_score"],
                            "relevance_score": score["relevance_score"],
                            "priority": score["outreach_priority"],
                            "contact_hint": score["contact_hint"],
                            "content_type": score["content_type"],
                            "estimated_audience": score["estimated_audience"],
                            "why": score["why"],
                        })
                    
                    time.sleep(0.5)  # Rate limit
    
    status.update(label="✅ Complete!", state="complete")
    progress_bar.progress(1.0)
    
    # Store in session
    st.session_state.results = results_data
    st.success(f"✅ Found {len(results_data)} candidates!")

# ─────────────────────────────────────────────
# DISPLAY RESULTS
# ─────────────────────────────────────────────
if "results" in st.session_state and st.session_state.results:
    st.divider()
    st.subheader("📊 Results")
    
    results = st.session_state.results
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_priority = st.multiselect(
            "Priority",
            ["HIGH", "MEDIUM", "LOW"],
            default=["HIGH", "MEDIUM"],
            key="filter_priority"
        )
    with col2:
        filter_country = st.multiselect(
            "Country",
            [r["country"] for r in results],
            key="filter_country"
        )
    with col3:
        filter_profile = st.multiselect(
            "Profile",
            [r["profile"] for r in results],
            key="filter_profile"
        )
    with col4:
        min_score = st.slider("Min EEAT Score", 0, 100, 30, key="min_score")
    
    # Apply filters
    filtered = results
    if filter_priority:
        filtered = [r for r in filtered if r["priority"] in filter_priority]
    if filter_country:
        filtered = [r for r in filtered if r["country"] in filter_country]
    if filter_profile:
        filtered = [r for r in filtered if r["profile"] in filter_profile]
    filtered = [r for r in filtered if r["eeat_score"] >= min_score]
    
    # Sort by EEAT score
    filtered = sorted(filtered, key=lambda x: x["eeat_score"], reverse=True)
    
    # Display
    st.markdown(f"**Showing {len(filtered)} of {len(results)} results**")
    
    for idx, result in enumerate(filtered, 1):
        # Score badge
        if result["eeat_score"] >= 70:
            score_class = "score-high"
        elif result["eeat_score"] >= 50:
            score_class = "score-mid"
        else:
            score_class = "score-low"
        
        with st.container():
            st.markdown(f"""
            <div class="result-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="flex: 1;">
                    <h4>{result['title']}</h4>
                    <p style="color: var(--muted); margin: 0.5rem 0;">{result['url']}</p>
                    <p>{result['snippet']}</p>
                    <div style="margin-top: 0.5rem;">
                        <span class="profile-tag">{result['profile']}</span>
                        <span class="country-tag">{result['country']}</span>
                        <span class="mono">{result['topic']}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="score-badge {score_class}">EEAT {result['eeat_score']}</span>
                    <div style="font-size: 0.75rem; color: var(--muted); margin-top: 0.5rem;">
                        <strong>Priority:</strong> {result['priority']}<br>
                        <strong>Audience:</strong> {result['estimated_audience']}<br>
                        <strong>Type:</strong> {result['content_type']}<br>
                        <strong>Contact:</strong> {result['contact_hint']}
                    </div>
                </div>
            </div>
            <p style="font-size: 0.85rem; color: var(--muted); margin-top: 0.5rem; border-top: 1px solid var(--border); padding-top: 0.5rem;">
                💡 {result['why']}
            </p>
            </div>
            """, unsafe_allow_html=True)
    
    # Export
    st.divider()
    if st.button("📥 Export to CSV"):
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=filtered[0].keys())
        writer.writeheader()
        writer.writerows(filtered)
        csv_data = csv_buffer.getvalue()
        
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="idealo_eeat_outreach.csv",
            mime="text/csv"
        )
