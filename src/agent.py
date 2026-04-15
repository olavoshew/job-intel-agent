import json
import os

import anthropic
import openai

from src.schemas import CVRewrite, CVScore, JobDescription

JD_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "company": {"type": "string"},
        "required_skills": {"type": "array", "items": {"type": "string"}},
        "nice_to_haves": {"type": "array", "items": {"type": "string"}},
        "seniority": {"type": "string"},
        "red_flags": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "company", "required_skills", "nice_to_haves", "seniority", "red_flags"],
}

CV_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "match_percentage": {"type": "integer", "minimum": 0, "maximum": 100},
        "gap_list": {"type": "array", "items": {"type": "string"}},
        "talking_points": {"type": "array", "items": {"type": "string"}},
        "pitch": {"type": "string"},
    },
    "required": ["match_percentage", "gap_list", "talking_points", "pitch"],
}

ANTHROPIC_JD_TOOL = {
    "name": "extract_job_description",
    "description": "Extract structured fields from a job description.",
    "input_schema": JD_TOOL_SCHEMA,
}

ANTHROPIC_CV_TOOL = {
    "name": "score_cv_match",
    "description": "Score how well a CV matches a job description.",
    "input_schema": CV_TOOL_SCHEMA,
}

OPENAI_JD_TOOL = {
    "type": "function",
    "function": {
        "name": "extract_job_description",
        "description": "Extract structured fields from a job description.",
        "parameters": JD_TOOL_SCHEMA,
    },
}

OPENAI_CV_TOOL = {
    "type": "function",
    "function": {
        "name": "score_cv_match",
        "description": "Score how well a CV matches a job description.",
        "parameters": CV_TOOL_SCHEMA,
    },
}

REWRITE_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "tips": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "section": {"type": "string"},
                    "problem": {"type": "string"},
                    "suggestion": {"type": "string"},
                },
                "required": ["section", "problem", "suggestion"],
            },
        },
        "rewritten_cv": {"type": "string"},
    },
    "required": ["tips", "rewritten_cv"],
}

ANTHROPIC_REWRITE_TOOL = {
    "name": "rewrite_cv",
    "description": "Provide tips to improve a CV and a rewritten version tailored to a job description.",
    "input_schema": REWRITE_TOOL_SCHEMA,
}

OPENAI_REWRITE_TOOL = {
    "type": "function",
    "function": {
        "name": "rewrite_cv",
        "description": "Provide tips to improve a CV and a rewritten version tailored to a job description.",
        "parameters": REWRITE_TOOL_SCHEMA,
    },
}


def _resolve_key(api_key: str | None, provider: str) -> str:
    if api_key:
        return api_key
    env_var = "ANTHROPIC_API_KEY" if provider == "anthropic" else "OPENAI_API_KEY"
    key = os.environ.get(env_var)
    if not key:
        raise RuntimeError(f"No API key provided and {env_var} is not set")
    return key


def _call_anthropic(api_key: str, messages: list, tool: dict, tool_name: str, max_tokens: int = 1024) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=max_tokens,
        tools=[tool],
        tool_choice={"type": "tool", "name": tool_name},
        messages=messages,
    )
    for block in response.content:
        if block.type == "tool_use":
            return block.input
    raise RuntimeError(f"Anthropic did not return a tool_use block for {tool_name}")


def _call_openai(api_key: str, messages: list, tool: dict, tool_name: str, max_tokens: int = 1024) -> dict:
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=max_tokens,
        tools=[tool],
        tool_choice={"type": "function", "function": {"name": tool_name}},
        messages=messages,
    )
    call = response.choices[0].message.tool_calls
    if call:
        return json.loads(call[0].function.arguments)
    raise RuntimeError(f"OpenAI did not return a tool call for {tool_name}")


async def extract_jd(text: str, api_key: str | None = None, provider: str = "anthropic") -> JobDescription:
    key = _resolve_key(api_key, provider)
    prompt = f"Extract the structured job description fields from this text:\n\n{text}"

    if provider == "openai":
        data = _call_openai(key, [{"role": "user", "content": prompt}], OPENAI_JD_TOOL, "extract_job_description")
    else:
        data = _call_anthropic(key, [{"role": "user", "content": prompt}], ANTHROPIC_JD_TOOL, "extract_job_description")

    return JobDescription(**data)


async def score_cv(jd: JobDescription, cv_text: str, api_key: str | None = None, provider: str = "anthropic") -> CVScore:
    key = _resolve_key(api_key, provider)
    jd_summary = (
        f"Title: {jd.title}\nCompany: {jd.company}\n"
        f"Required: {', '.join(jd.required_skills)}\n"
        f"Nice to have: {', '.join(jd.nice_to_haves)}\n"
        f"Seniority: {jd.seniority}\n"
        f"Red flags: {', '.join(jd.red_flags)}"
    )
    prompt = (
        f"Compare this CV against the job description and score the match.\n\n"
        f"JOB DESCRIPTION:\n{jd_summary}\n\n"
        f"CV:\n{cv_text}\n\n"
        f"Be honest about gaps. The pitch should be exactly 3 sentences."
    )

    if provider == "openai":
        data = _call_openai(key, [{"role": "user", "content": prompt}], OPENAI_CV_TOOL, "score_cv_match")
    else:
        data = _call_anthropic(key, [{"role": "user", "content": prompt}], ANTHROPIC_CV_TOOL, "score_cv_match")

    return CVScore(**data)


async def rewrite_cv(jd: JobDescription, cv_text: str, api_key: str | None = None, provider: str = "anthropic") -> CVRewrite:
    key = _resolve_key(api_key, provider)
    jd_summary = (
        f"Title: {jd.title}\nCompany: {jd.company}\n"
        f"Required: {', '.join(jd.required_skills)}\n"
        f"Nice to have: {', '.join(jd.nice_to_haves)}\n"
        f"Seniority: {jd.seniority}\n"
        f"Red flags: {', '.join(jd.red_flags)}"
    )
    prompt = (
        f"You are a CV consultant. Analyze this CV against the job description.\n\n"
        f"JOB DESCRIPTION:\n{jd_summary}\n\n"
        f"CURRENT CV:\n{cv_text}\n\n"
        f"For each section of the CV that could be improved, provide a tip with the section name, "
        f"what the problem is, and a concrete suggestion.\n"
        f"Then provide a complete rewritten version of the CV tailored to this job. "
        f"Keep it honest (do not invent experience), but reorder, rephrase, and highlight "
        f"relevant skills. Use plain text formatting."
    )

    if provider == "openai":
        data = _call_openai(key, [{"role": "user", "content": prompt}], OPENAI_REWRITE_TOOL, "rewrite_cv", max_tokens=4096)
    else:
        data = _call_anthropic(key, [{"role": "user", "content": prompt}], ANTHROPIC_REWRITE_TOOL, "rewrite_cv", max_tokens=4096)

    return CVRewrite(**data)
