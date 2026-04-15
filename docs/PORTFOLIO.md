# Job Intel Agent - Portfolio Handoff

## The Story

This project went from zero to working product in under an hour across a handful of directed sessions. Not because the code is trivial, but because the tooling setup behind it (CLAUDE.md, skill files, session logging, structured prompts) has been refined over 3+ months of daily research and iteration. The speed is the point: it demonstrates what happens when you invest in your development workflow instead of just your code.

## Why It Was Built

Two reasons:

1. **Solves a real problem.** Every job seeker manually reads listings, mentally compares them to their resume, and guesses what to emphasize. This tool does that comparison in seconds and tells you exactly where the gaps are. Anyone who has applied to jobs immediately gets it.

2. **Shows AI engineering, not AI wrapping.** Most "AI projects" in portfolios are thin wrappers around ChatGPT. This one uses structured output (tool_use on Anthropic, function calling on OpenAI), strict Pydantic validation, async HTTP scraping, and multi-provider support. It demonstrates understanding of how to build with LLMs in production, not just call them.

## What Broke and Got Fixed

### pyproject.toml scripts entry
The initial `[project.scripts]` entry tried to use a shell command (`uvicorn src.main:app --reload`) as a Python entrypoint. That is not valid. setuptools requires `module:function` format for console scripts. Fixed by removing the entry entirely and just documenting the command in the README.

### Build backend path
The first attempt used `setuptools.backends._legacy:_Backend` as the build backend, which does not exist. The correct value is `setuptools.build_meta`. Caught during `pip install -e .`.

### Dead code after return
`agent.py` had a `raise RuntimeError` statement after a `return` block, making it unreachable. Discovered during the rewrite feature addition and cleaned up.

### Favicon 404
The browser kept requesting `/favicon.ico` and getting a 404. Created a simple SVG favicon (magnifying glass emoji in an SVG text element) and linked it in the HTML head. Small fix, but the kind of thing that makes a project feel finished.

### Connection refused on /analyze
After killing the server at the end of a session, the next session started with the user reporting "connection refused." Not a code bug, the server just was not running. Added `--reload` flag to the standard startup command so file changes auto-apply.

### Structured output format differences
Anthropic and OpenAI handle tool/function calling differently. Anthropic returns tool results in `content[].input`, OpenAI returns them in `tool_calls[].function.arguments` (as a JSON string that needs parsing). Both had to be normalized into the same Pydantic models. This required separate `_call_anthropic` and `_call_openai` helper functions with different response parsing logic.

### Max tokens for CV rewrite
The default 1024 max_tokens worked fine for JD extraction and CV scoring (small JSON responses), but the rewrite endpoint returns a full CV plus tips, often exceeding 1024 tokens. Bumped to 4096 for the rewrite function specifically.

## Architecture Decisions

**tool_use over JSON mode.** Anthropic recommends tool_use for structured output because the model is trained to follow tool schemas precisely. JSON mode works but is more prone to schema drift. The tool_use approach also gave a natural path to OpenAI compatibility since OpenAI has an equivalent function calling mechanism.

**Regex HTML stripping over BeautifulSoup.** The scraper strips `<script>`, `<style>`, `<nav>`, `<header>`, `<footer>` tags with regex, then removes remaining HTML tags. Not perfect for every edge case, but keeps the dependency list minimal and handles 90%+ of job listing pages adequately. Adding beautifulsoup4 later would be a one-line change.

**Demo mode as a first-class feature.** Every portfolio project needs to be instantly tryable. Making demo mode return hard-coded data (not mocked API calls) means it works with zero configuration, zero latency, and zero cost. Visitors see real output shape in under a second.

**Dual provider support.** Supporting both Anthropic and OpenAI was a mid-build addition. The benefit is twofold: portfolio visitors can use whichever API key they have, and the code demonstrates how to abstract over different LLM providers without introducing a heavy abstraction layer.

**No frontend framework.** The UI is vanilla HTML/CSS/JS. For a tool this focused, React or Vue would add build complexity with no real benefit. The dark theme with purple accents was done in pure CSS. Total JS is about 150 lines.

## What the Claude/Tooling Setup Looks Like

The speed of this build came from a system, not from rushing:

- **CLAUDE.md** in the project root contains per-phase prompts, skill file paths, and session start/end rituals. Every Claude session starts by reading the project state, spec, and relevant skill files before writing a single line of code.
- **Skill files** for FastAPI, Anthropic SDK, structured output, and Pydantic live in a shared skills directory and are loaded before relevant work. They contain patterns, not tutorials: exact code shapes that work, common pitfalls to avoid, and schema examples.
- **Session logging** in a vault file tracks what was built, what broke, and what comes next. Every session ends by updating the log. This means no session starts cold.
- **Writing rules** enforced across all output: no em dashes, no AI vocabulary (leverage, robust, seamless), no filler phrases. This carries through to the demo data, README, and any generated text.

The result is that directing the AI to build this tool feels like pair programming with a very fast junior dev who has already read the docs. The setup cost is front-loaded, but it pays off on every project after the first.

## Technical Highlights for Portfolio Display

- ~700 lines of Python across 5 source files, all under 100 lines each
- 12 passing tests with zero real API calls (fully mocked)
- 4 Pydantic models with field constraints (match_percentage 0-100, nested CVTip lists)
- Async throughout: httpx for scraping, async route handlers, async LLM calls
- 3 API tool schemas (JD extraction, CV scoring, CV rewriting) each with Anthropic and OpenAI variants
- Dark-themed UI with no CSS framework, purple/indigo accents, stripe decorations
- One-command deploy to Railway with auto-detection via nixpacks

## Files for Portfolio Integration

| File | Purpose |
|------|---------|
| `README.md` | Project overview, setup, structure |
| `docs/screenshot.png` | UI screenshot (needs capture) |
| `static/index.html` | Visual demo of the UI |
| This file | Build narrative, challenges, decisions |

## Remaining Before Ship

1. Capture a screenshot of the dark-themed UI with demo results visible, save to `docs/screenshot.png`
2. Set the live Railway URL in README once deployed
3. Push to GitHub
