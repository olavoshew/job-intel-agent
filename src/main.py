import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.agent import extract_jd, rewrite_cv, score_cv
from src.demo import DEMO_CV, DEMO_JD, DEMO_REWRITE, DEMO_SCORE
from src.schemas import CVRewrite, CVScore
from src.scraper import fetch_jd

load_dotenv()

app = FastAPI()

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

CV_PATH = Path(__file__).resolve().parent / "cv.txt"


class AnalyzeRequest(BaseModel):
    url: Optional[str] = None
    text: Optional[str] = None
    cv_text: Optional[str] = None
    demo: Optional[bool] = False
    api_key: Optional[str] = None
    provider: Optional[str] = "anthropic"


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    if req.demo:
        return CVScore(**DEMO_SCORE)

    if not req.url and not req.text:
        raise HTTPException(status_code=400, detail="Provide a url or text field")

    if req.provider not in ("anthropic", "openai"):
        raise HTTPException(status_code=400, detail="Provider must be anthropic or openai")

    try:
        raw_text = req.text if req.text else await fetch_jd(req.url)
        jd = await extract_jd(raw_text, api_key=req.api_key, provider=req.provider)
        cv_text = req.cv_text if req.cv_text else CV_PATH.read_text(encoding="utf-8")
        result = await score_cv(jd, cv_text, api_key=req.api_key, provider=req.provider)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/rewrite")
async def rewrite(req: AnalyzeRequest):
    if req.demo:
        return CVRewrite(**DEMO_REWRITE)

    if not req.url and not req.text:
        raise HTTPException(status_code=400, detail="Provide a url or text field")

    if not req.cv_text:
        raise HTTPException(status_code=400, detail="Provide your CV text to get a rewrite")

    if req.provider not in ("anthropic", "openai"):
        raise HTTPException(status_code=400, detail="Provider must be anthropic or openai")

    try:
        raw_text = req.text if req.text else await fetch_jd(req.url)
        jd = await extract_jd(raw_text, api_key=req.api_key, provider=req.provider)
        result = await rewrite_cv(jd, req.cv_text, api_key=req.api_key, provider=req.provider)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
