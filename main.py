from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import json
import os
import io
import re
import httpx

app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

async def analyze_with_gemini(resume_text: str, job_description: str, api_key: str) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    prompt = f"""
You are an expert ATS resume analyzer and career coach. Analyze the resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Respond ONLY with a valid JSON object (no markdown, no backticks) with this exact structure:
{{
  "match_score": <integer 0-100>,
  "summary": "<2-3 sentence overall assessment>",
  "strengths": ["<strength 1>", "<strength 2>", "<strength 3>"],
  "missing_skills": ["<skill 1>", "<skill 2>", "<skill 3>"],
  "keyword_matches": ["<keyword 1>", "<keyword 2>", "<keyword 3>", "<keyword 4>", "<keyword 5>"],
  "missing_keywords": ["<keyword 1>", "<keyword 2>", "<keyword 3>"],
  "improved_bullets": [
    {{"original": "<original bullet>", "improved": "<rewritten bullet tailored to JD>"}},
    {{"original": "<original bullet>", "improved": "<rewritten bullet tailored to JD>"}}
  ],
  "ats_tips": ["<tip 1>", "<tip 2>", "<tip 3>"],
  "verdict": "<one of: Strong Match, Good Match, Partial Match, Weak Match>"
}}
"""

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Gemini API error: {response.text}")
        data = response.json()

    raw = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    return json.loads(raw)


@app.get("/", response_class=HTMLResponse)
async def root():
    with open("templates/index.html") as f:
        return f.read()


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    api_key: str = Form(...)
):
    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    if len(job_description.strip()) < 50:
        raise HTTPException(status_code=400, detail="Job description too short.")

    file_bytes = await resume.read()
    resume_text = extract_text_from_pdf(file_bytes)

    if len(resume_text) < 100:
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")

    try:
        result = await analyze_with_gemini(resume_text, job_description, api_key)
        return JSONResponse(content=result)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI response parsing failed. Try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))