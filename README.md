# Idealo EEAT Outreach Discovery

Find high-quality, EEAT-optimized outreach candidates (bloggers, journalists, micro-influencers, YouTubers) using AI-powered research.

## Stack

- **Tavily Search API** (semantic search, optimized for AI research)
- **OpenAI GPT-4o-mini** (EEAT scoring & analysis)
- **Streamlit** (UI)
- **Streamlit Cloud** (deployment)

## Quick Start (Local)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up secrets

Create `.streamlit/secrets.toml`:

```toml
TAVILY_API_KEY = "your_tavily_api_key"
OPENAI_API_KEY = "your_openai_api_key"
```

Get keys from:
- **Tavily**: https://tavily.com (free tier: 1000/month)
- **OpenAI**: https://platform.openai.com (free credits or paid)

### 3. Run locally

```bash
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## Deploy to Streamlit Cloud

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/idealo-eeat-outreach.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **New app**
3. Select your GitHub repo
4. Select branch: `main`
5. Select file path: `app.py`
6. Click **Deploy**

### 3. Add Secrets

After deployment:
1. Go to **⋮** (top right) → **Settings**
2. Go to **Secrets** tab
3. Paste your `.streamlit/secrets.toml` content
4. Save

---

## Cost & Limits

| Service | Free Tier | Cost per Query |
|---------|-----------|----------------|
| Tavily  | 1000/month | Free (API calls) |
| OpenAI  | Free credits | ~$0.00015/request (GPT-4o-mini) |

**Example run:**
- 2 countries × 2 profiles × 3 topics × 3 queries = **36 searches**
- 36 searches × ~5 results = **180 GPT evaluations**
- **Total cost: ~$0.03 per run**

---

## Features

✅ Multi-country / multi-profile search  
✅ EEAT scoring (0-100)  
✅ Outreach priority classification (HIGH / MEDIUM / LOW)  
✅ Contact hint detection  
✅ Audience estimation  
✅ Content type classification  
✅ CSV export  
✅ Real-time progress tracking  
✅ Semantic filtering  

---

## How It Works

1. **Search**: Tavily finds relevant articles/pages for each profile-country-topic combo
2. **Score**: GPT-4o-mini evaluates EEAT (Expertise, Authority, Trust) + relevance
3. **Filter**: Display high-priority candidates with contact hints
4. **Export**: Download CSV for outreach campaigns

---

## API Keys

### Tavily

1. Go to https://tavily.com
2. Sign up (free)
3. Go to **Dashboard** → **API Keys**
4. Copy your API key

### OpenAI

1. Go to https://platform.openai.com/account/api-keys
2. Create new API key
3. Copy it

---

## Customize

**Add countries**: Edit `COUNTRIES` dict in `app.py`  
**Add profiles**: Edit `PROFILES` dict with custom search queries  
**Change topics**: Edit `TOPICS` list  
**Adjust scoring**: Modify `score_with_gpt()` system prompt  

---

## Troubleshooting

**"Missing API keys"** → Fill them in sidebar or `.streamlit/secrets.toml`  
**"Tavily API error"** → Check API key validity on tavily.com  
**"OpenAI error"** → Check API key has credits/limits  
**No results** → Try different keywords or expand search scope  

---

## License

MIT
