# ResumeIQ — AI Resume Analyzer

An AI-powered resume analyzer built with FastAPI + Google Gemini. Upload your resume, paste a job description, and get:
- Match score (0–100)
- Strengths & missing skills
- Keyword gap analysis
- Improved bullet point suggestions
- ATS optimization tips

---

## Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the server
```bash
uvicorn main:app --reload
```

### 3. Open in browser
```
http://localhost:8000
```

---

## Deploy FREE on Render

1. Push this folder to a **GitHub repo**
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Click **Deploy** — done! You'll get a live URL.

---

## Deploy FREE on Railway

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. It auto-detects the Procfile
4. Done — live in ~2 minutes.

---

## Get Gemini API Key (Free)

1. Go to https://aistudio.google.com/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Paste it in the app — it's never stored on the server.

---

## Project Structure

```
resume-analyzer/
├── main.py           # FastAPI backend
├── requirements.txt  # Python dependencies
├── Procfile          # For Render/Railway deployment
├── templates/
│   └── index.html    # Frontend UI
└── static/           # Static assets (empty)
```

---

Built by Akash Kumar Injeti
