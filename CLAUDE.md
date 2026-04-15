# CLAUDE.md — Job Intel Agent

<!-- .claude-governance-start -->
## .claude Governance (Mandatory)

**Do NOT start coding until this boot sequence is complete.**

1. Read `c:\Code\.claude\GOVERNANCE.md` -- rules, skill resolution, boundaries
2. Read `c:\Code\.claude\skills-registry.md` -- per-project skill mappings
3. Read `c:\Code\.claude\vault\CHANGELOG.md` -- what evolved since last session

For first session on this project, also read:
4. `c:\Code\.claude\vault\04-projects\01-job-intel-agent.md` -- current phase, session log
5. Each SKILL.md listed below
6. `c:\Code\.claude\vault\03-patterns\` -- reusable patterns from earlier projects

All rules, skill resolution, evolution protocol, and session end protocol are in GOVERNANCE.md.
<!-- .claude-governance-end -->

## Skills to Read Before Starting
```
c:\Code\Skills\antigravity-awesome-skills\skills\python-fastapi\SKILL.md
c:\Code\Skills\antigravity-awesome-skills\skills\anthropic-sdk\SKILL.md
c:\Code\Skills\antigravity-awesome-skills\skills\structured-output\SKILL.md
c:\Code\Skills\antigravity-awesome-skills\skills\pydantic\SKILL.md
```

## Phase 1 — Setup (~2hr)

**Goal:** Working skeleton. Nothing broken. `uvicorn src.main:app` runs.

**Prompt (copy-paste to start a Claude session):**
```
I'm building a Job Intel Agent — a tool that accepts a job URL and returns a structured CV scoring report using the Claude API. I need to set up the project skeleton before any logic.

Working directory: c:\Code\Portfolio\01-job-intel-agent\

Create the following:
1. `pyproject.toml` — Python 3.11+, dependencies: fastapi, uvicorn[standard], anthropic, pydantic, httpx. Add a [project.scripts] entry for `uvicorn src.main:app --reload`.
2. `.env.example` — two variables: ANTHROPIC_API_KEY and PORT=8000
3. `src/__init__.py` (empty)
4. `src/main.py` — FastAPI app, one route GET / returns {"status": "ok"}, loads .env with python-dotenv
5. `src/schemas.py` — Pydantic models: JobDescription (title, company, required_skills: list[str], nice_to_haves: list[str], seniority: str, red_flags: list[str]), CVScore (match_percentage: int, gap_list: list[str], talking_points: list[str], pitch: str)
6. `src/demo.py` — hard-coded DEMO_JD and DEMO_CV strings for zero-key testing (use a realistic software engineering JD)

Rules: no comments, no docstrings, no em dashes in any text. Keep each file under 100 lines.

After creating files, tell me what command to run to verify the server starts.
```

## Phase 2 — Core Logic (~3hr)

**Goal:** Claude API extracts structured data from a real job description URL. CV is scored.

**Prompt:**
```
Continue the Job Intel Agent. The skeleton exists (FastAPI boots, schemas defined, demo.py has sample data).

Working directory: c:\Code\Portfolio\01-job-intel-agent\

Create or update:
1. `src/scraper.py` — async function `fetch_jd(url: str) -> str` using httpx. Fetches the URL, extracts visible text from HTML (strip scripts/styles/nav with basic regex or BeautifulSoup if needed), returns clean text. Raise a clear ValueError if the page returns non-200 or text is under 200 chars.
2. `src/agent.py` — two async functions:
   - `extract_jd(text: str) -> JobDescription` — calls Claude API, uses structured output (tool_use or JSON mode) to extract JobDescription fields from raw JD text
   - `score_cv(jd: JobDescription, cv_text: str) -> CVScore` — calls Claude API, compares JD to CV text, returns CVScore with match_percentage, gap_list, talking_points, 3-sentence pitch
   Both functions load ANTHROPIC_API_KEY from env. Use claude-3-5-haiku for speed.

Read `c:\Code\Skills\antigravity-awesome-skills\skills\structured-output\SKILL.md` before writing agent.py.

Rules: no comments, no docstrings, no em dashes. Handle API errors with a clear exception message.
```

## Phase 3 — API + UI (~2hr)

**Goal:** End-to-end flow works in a browser. Demo mode works with no API key.

**Prompt:**
```
Continue the Job Intel Agent. Scraper and agent logic are complete.

Working directory: c:\Code\Portfolio\01-job-intel-agent\

Create or update:
1. `src/main.py` — add route POST /analyze:
   - Body: {"url": str} OR {"text": str, "demo": bool}
   - If demo=true: use DEMO_JD from demo.py and DEMO_CV from demo.py, skip scraper, skip API call, return hard-coded CVScore
   - Otherwise: call scraper.fetch_jd(url), then agent.extract_jd(), then agent.score_cv() with CV loaded from a local cv.txt file
   - Return the CVScore as JSON
2. `src/cv.txt` — paste a 200-word summary of Olavo's background (Python developer, Unity/C#, automation, creative technologist, student visa 48hrs/fortnight)
3. `static/index.html` — single HTML file, no framework:
   - Textarea for JD URL or paste text
   - Checkbox "Try demo (no API key needed)"
   - Submit button
   - Results section: shows match %, gap list, talking points, pitch
   - Fetches POST /analyze, renders JSON response inline
   Mount static files in FastAPI.

Rules: no comments, no docstrings, no em dashes, no inline `<script>` over 50 lines.
```

## Phase 4 — Test + Deploy (~2hr)

**Goal:** Tests pass. Live URL on Railway. README leads with the live URL.

**Prompt:**
```
Finish the Job Intel Agent for deployment.

Working directory: c:\Code\Portfolio\01-job-intel-agent\

1. `tests/test_schemas.py` — pytest tests: valid JobDescription parses correctly, missing required field raises ValidationError, CVScore with out-of-range match_percentage raises ValidationError
2. `tests/test_agent.py` — mock the Anthropic client, verify extract_jd returns a JobDescription, verify score_cv returns a CVScore with reasonable fields. Do not make real API calls in tests.
3. `Procfile` — `web: uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. `railway.json` — minimal Railway config with build and deploy commands
5. `README.md` — structure:
   - Line 1: "**Live demo:** [URL]" (placeholder for now)
   - 3-sentence explainer: what it does, how it works, who it is for
   - Local setup instructions (pip install, env vars, uvicorn command)
   - Demo mode instructions (no API key needed)
   - Screenshot placeholder

After creating files, give me the exact Railway deploy steps.

Rules: no em dashes, no AI vocabulary (leverage, robust, seamless, etc.), no filler phrases.
```
