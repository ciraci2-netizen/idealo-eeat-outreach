import streamlit as st
import requests
import json
import time
import csv
import io
from openai import OpenAI

st.set_page_config(
    page_title="Idealo EEAT Outreach Discovery",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# PREMIUM CSS DESIGN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
    --primary: #FF6B35;
    --primary-dark: #D94717;
    --secondary: #004E89;
    --accent: #F7B801;
    --bg-dark: #0F1419;
    --bg-darker: #0A0E14;
    --surface: #1A1F2E;
    --surface-light: #2A3142;
    --text-primary: #FFFFFF;
    --text-secondary: #B0B8C8;
    --text-muted: #7A8292;
    --success: #06D6A0;
    --warning: #FFD60A;
    --danger: #EF476F;
    --border: #2A3142;
}

* { font-family: 'Poppins', sans-serif !important; }

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, var(--bg-dark) 0%, var(--bg-darker) 100%) !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] {
    background: rgba(26, 31, 46, 0.95) !important;
    border-right: 1px solid var(--border) !important;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 700 !important;
    letter-spacing: -0.5px !important;
    color: var(--text-primary) !important;
}

h1 { font-size: 2.5rem !important; }
h2 { font-size: 1.75rem !important; }

.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.3s !important;
    box-shadow: 0 8px 24px rgba(255, 107, 53, 0.2) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 32px rgba(255, 107, 53, 0.35) !important;
}

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    padding: 0.75rem 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
}

[data-testid="stMetric"] {
    background: rgba(26, 31, 46, 0.6) !important;
    padding: 1.5rem !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-weight: 700 !important;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%) !important;
    border-radius: 10px !important;
}

[data-testid="stAlert"] {
    background: rgba(255, 107, 53, 0.1) !important;
    border-left: 4px solid var(--primary) !important;
    border-radius: 10px !important;
}

.result-card {
    background: linear-gradient(135deg, rgba(26, 31, 46, 0.8) 0%, rgba(42, 49, 66, 0.4) 100%) !important;
    border: 1px solid var(--border) !important;
    border-left: 4px solid var(--primary) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
    margin-bottom: 1.25rem !important;
}

.result-card:hover {
    border-left-color: var(--accent) !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3) !important;
}

.badge {
    display: inline-block;
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
    text-transform: uppercase;
}

.profile-tag {
    background: rgba(255, 107, 53, 0.15) !important;
    border: 1px solid rgba(255, 107, 53, 0.3) !important;
    color: var(--primary) !important;
}

.country-tag {
    background: rgba(0, 78, 137, 0.15) !important;
    border: 1px solid rgba(0, 78, 137, 0.3) !important;
    color: #5DADE2 !important;
}

.score-badge {
    padding: 0.5rem 1.2rem !important;
    border-radius: 10px !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
}

.score-high {
    background: rgba(6, 214, 160, 0.15) !important;
    color: var(--success) !important;
    border: 1px solid rgba(6, 214, 160, 0.3) !important;
}

.score-mid {
    background: rgba(247, 184, 1, 0.15) !important;
    color: var(--warning) !important;
    border: 1px solid rgba(247, 184, 1, 0.3) !important;
}

.score-low {
    background: rgba(239, 71, 111, 0.15) !important;
    color: var(--danger) !important;
    border: 1px solid rgba(239, 71, 111, 0.3) !important;
}

hr {
    border-color: var(--border) !important;
    margin: 2rem 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
COUNTRIES = {
    "🇩🇪 Germany (DE)": {"code": "de", "lang": "de", "label": "DE"},
    "🇮🇹 Italy (IT)": {"code": "it", "lang": "it", "label": "IT"},
    "🇫🇷 France (FR)": {"code": "fr", "lang": "fr", "label": "FR"},
    "🇪🇸 Spain (ES)": {"code": "es", "lang": "es", "label": "ES"},
    "🇬🇧 UK (UK)": {"code": "uk", "lang": "en", "label": "UK"},
    "🇵🇱 Poland (PL)": {"code": "pl", "lang": "pl", "label": "PL"},
}

PROFILES = {
    "📝 Blogger": {"label": "Blogger", "queries": ['{keyword} blog {country}', 'best {keyword} {country} blog review', '{keyword} recommendations blogger review']},
    "📰 Journalist": {"label": "Journalist", "queries": ['{keyword} journalist {country}', '{keyword} article review {country}', '{keyword} journalist news {country}']},
    "🤳 Micro-influencer": {"label": "Micro-influencer", "queries": ['{keyword} influencer {country}', '{keyword} micro influencer', '{keyword} creator collaboration']},
    "▶️ YouTuber": {"label": "YouTuber", "queries": ['{keyword} review youtube', '{keyword} youtube channel', '{keyword} youtuber comparison']},
}

TOPICS = ["smartphones", "laptops", "headphones", "smart home", "tablets", "cameras", "TVs", "washing machines", "vacuum cleaners", "gaming peripherals"]

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def tavily_search(query: str, api_key: str, num: int = 5) -> list:
    """Call Tavily Search API."""
    try:
        url = "https://api.tavily.com/search"
        payload = {"api_key": api_key, "query": query, "max_results": num, "include_answer": True}
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = []
        for result in data.get("results", []):
            results.append({"title": result.get("title", ""), "link": result.get("url", ""), "snippet": result.get("content", "")})
        return results
    except Exception as e:
        st.warning(f"Tavily search error: {e}")
        return []

def score_with_gpt(client: OpenAI, result: dict, profile: str, country: str, keyword: str) -> dict:
    """Use GPT-4o-mini to score & enrich a search result."""
    system_prompt = "You are an EEAT outreach analyst for Idealo. Evaluate web results to identify high-quality outreach candidates. Respond ONLY with valid JSON."
    
    user_prompt = f"""Evaluate this result for outreach potential:
Profile type: {profile}
Target country: {country}
Keyword topic: {keyword}

Result:
- Title: {result.get('title', '')}
- URL: {result.get('link', '')}
- Snippet: {result.get('snippet', '')}

Return JSON with: eeat_score (0-100), relevance_score (0-100), outreach_priority (HIGH/MEDIUM/LOW), contact_hint, why, estimated_audience, content_type"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.3,
            max_tokens=300,
        )
        raw = response.choices[0].message.content.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except:
        return {"eeat_score": 0, "relevance_score": 0, "outreach_priority": "LOW", "contact_hint": "unknown", "why": "Parsing error", "estimated_audience": "unknown", "content_type": "unknown"}

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    tavily_key = st.text_input("Tavily API Key", value=st.secrets.get("TAVILY_API_KEY", ""), type="password")
    openai_key = st.text_input("OpenAI API Key", value=st.secrets.get("OPENAI_API_KEY", ""), type="password")
    
    if not tavily_key or not openai_key:
        st.warning("⚠️ Missing API keys!")
        st.stop()
    
    st.divider()
    st.markdown("## 🎯 Search Config")
    
    selected_countries = st.multiselect("Countries", list(COUNTRIES.keys()), default=list(COUNTRIES.keys())[:2])
    selected_profiles = st.multiselect("Profiles", list(PROFILES.keys()), default=list(PROFILES.keys())[:2])
    selected_topics = st.multiselect("Topics", TOPICS, default=TOPICS[:3])
    
    st.divider()
    st.markdown("## ⚡ Speed Mode")
    speed_mode = st.radio("Mode", ["🚀 Fast (1-2 min)", "⚙️ Normal (5-10 min)", "🔬 Thorough (15+ min)"], index=0)
    
    if "Fast" in speed_mode:
        queries_per_combo, results_per_query = 1, 3
    elif "Normal" in speed_mode:
        queries_per_combo, results_per_query = 3, 5
    else:
        queries_per_combo, results_per_query = 3, 10

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <div style='font-size: 3rem; margin-bottom: 0.5rem;'>🔍</div>
    <h1>Idealo EEAT Outreach Discovery</h1>
    <p style='color: #B0B8C8; font-size: 1.1rem;'>Find high-quality, EEAT-optimized outreach candidates</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Stats
col1, col2, col3, col4 = st.columns(4)
num_countries = len(selected_countries)
num_profiles = len(selected_profiles)
num_topics = len(selected_topics)
total_queries = num_countries * num_profiles * num_topics * queries_per_combo

with col1:
    st.metric("🌍 Countries", num_countries)
with col2:
    st.metric("👥 Profiles", num_profiles)
with col3:
    st.metric("📌 Topics", num_topics)
with col4:
    st.metric("📊 Est. Queries", total_queries)

if total_queries > 100:
    st.warning(f"⚠️ This will use ~{total_queries} Tavily credits (free: 1000/month)")

if st.button("🚀 START DISCOVERY", type="primary", use_container_width=True):
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
                    progress_bar.progress(step / total_steps)
                    
                    query = query_template.format(keyword=topic, country=country_obj["label"])
                    status.write(f"🔍 {country_name} → {profile_name} → {topic}")
                    
                    search_results = tavily_search(query, tavily_key, num=results_per_query)
                    
                    for result in search_results:
                        score = score_with_gpt(client, result, profile_name, country_obj["label"], topic)
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
                            "contact": score["contact_hint"],
                            "content_type": score["content_type"],
                            "audience": score["estimated_audience"],
                            "why": score["why"],
                        })
                    
                    time.sleep(0.5)
    
    status.update(label="✅ Complete!", state="complete")
    progress_bar.progress(1.0)
    st.session_state.results = results_data
    st.success(f"✅ Found {len(results_data)} candidates!")

# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════════════════════════════════════
if "results" in st.session_state and st.session_state.results:
    st.divider()
    st.markdown("## 📊 Results")
    
    results = st.session_state.results
    
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        filter_priority = st.multiselect("Priority", ["HIGH", "MEDIUM", "LOW"], default=["HIGH", "MEDIUM"], key="p")
    with f_col2:
        filter_country = st.multiselect("Country", sorted(set(r["country"] for r in results)), key="c")
    with f_col3:
        min_score = st.slider("Min EEAT Score", 0, 100, 30, key="s")
    
    filtered = [r for r in results if r["priority"] in filter_priority and r["eeat_score"] >= min_score]
    if filter_country:
        filtered = [r for r in filtered if r["country"] in filter_country]
    
    filtered = sorted(filtered, key=lambda x: x["eeat_score"], reverse=True)
    
    st.markdown(f"**Showing {len(filtered)} of {len(results)} results**\n")
    
    for result in filtered:
        score_class = "score-high" if result["eeat_score"] >= 70 else ("score-mid" if result["eeat_score"] >= 50 else "score-low")
        
        st.markdown(f"""
        <div class="result-card">
            <div style="display: flex; justify-content: space-between;gap: 2rem;">
                <div style="flex: 1;">
                    <h4 style="margin: 0 0 0.5rem 0;">{result['title']}</h4>
                    <p style="color: #B0B8C8; margin: 0.5rem 0; font-size: 0.9rem;">{result['url'][:60]}...</p>
                    <p style="margin: 1rem 0; line-height: 1.6; color: #B0B8C8;">{result['snippet'][:150]}...</p>
                    <div style="margin-top: 1rem;">
                        <span class="badge profile-tag">{result['profile']}</span>
                        <span class="badge country-tag">{result['country']}</span>
                        <span class="badge country-tag">{result['topic']}</span>
                    </div>
                </div>
                <div style="text-align: right; flex: 0 0 160px;">
                    <span class="score-badge {score_class}">EEAT {result['eeat_score']}</span>
                    <div style="font-size: 0.8rem; color: #B0B8C8; margin-top: 1rem; line-height: 2;">
                        <strong>Priority:</strong> {result['priority']}<br>
                        <strong>Audience:</strong> {result['audience']}<br>
                        <strong>Type:</strong> {result['content_type']}<br>
                        <strong>Contact:</strong> {result['contact']}
                    </div>
                </div>
            </div>
            <div style="border-top: 1px solid #2A3142; padding-top: 1rem; margin-top: 1rem;">
                <p style="font-size: 0.85rem; color: #7A8292; margin: 0;">💡 {result['why']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=filtered[0].keys())
    writer.writeheader()
    writer.writerows(filtered)
    
    st.download_button("📥 Export CSV", csv_buffer.getvalue(), "idealo_outreach.csv", "text/csv", use_container_width=True)
