# PROJECT.md — Job Intel Agent

## Concept
Paste a job URL. Get back a structured report: what the role wants, how your CV scores against it, missing keywords, and suggested talking points.

## Target User / Problem
Developers who apply to 10+ roles per week and waste time manually comparing job descriptions to their resume. Also: the story lands instantly with any recruiter who hears the pitch.

## Key Features
- Input: job posting URL or raw text
- Claude API extracts structured data: required skills, nice-to-haves, red flags, seniority signals
- CV scoring: match percentage + ranked gap list
- Output: markdown report with score, gaps, talking points, and a suggested 3-sentence pitch
- Demo mode: hard-coded example JD + CV so visitors can try without an API key

## Tech Stack
- Python 3.11+
- Anthropic SDK (`anthropic`)
- FastAPI (API endpoint + simple HTML UI)
- Pydantic (structured output validation)
- httpx (fetch JD from URL)
- Railway (deploy target)

## File Structure
```
src/
  main.py          FastAPI app + routes
  agent.py         Claude API calls + prompt templates
  schemas.py       Pydantic models for JD extraction + scoring
  scraper.py       URL fetcher + HTML text extraction
  demo.py          Hard-coded demo JD + CV for zero-key testing
tests/
  test_agent.py
  test_schemas.py
docs/
  SETUP.md
```

## Environment Variables
```
ANTHROPIC_API_KEY=
PORT=8000
```

## Deploy Target
Railway — connect GitHub repo, set env vars, auto-deploy on push.

## Definition of Done
- [ ] Local: `uvicorn src.main:app` runs, demo mode works with no API key
- [ ] API: POST `/analyze` accepts `{url: "..."}`, returns structured JSON report
- [ ] UI: single HTML page with textarea + submit, renders the report
- [ ] Tests: schema validation tests pass
- [ ] Deployed: live URL on Railway, demo accessible without login
- [ ] README: demo link in first line, 3-sentence explainer

## Why This Impresses Recruiters
Solves a problem every job applicant has. Uses Claude API in production with structured output. Story is immediately relatable. Shows AI engineering instincts, not just UI wrapping.

## Stand Out Further
Add a side-by-side comparison mode: same CV against a weak-match vs. strong-match JD to show the contrast.
