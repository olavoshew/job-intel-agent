from unittest.mock import MagicMock, patch

import pytest

from src.agent import extract_jd, rewrite_cv, score_cv
from src.schemas import CVRewrite, CVScore, JobDescription


@pytest.mark.asyncio
async def test_extract_jd_anthropic():
    jd_data = {
        "title": "Backend Engineer",
        "company": "Acme Corp",
        "required_skills": ["Python", "FastAPI"],
        "nice_to_haves": ["Docker"],
        "seniority": "Senior",
        "red_flags": ["No remote"],
    }

    with patch("src.agent._call_anthropic", return_value=jd_data):
        result = await extract_jd("Some job description text", api_key="sk-test", provider="anthropic")

    assert isinstance(result, JobDescription)
    assert result.title == "Backend Engineer"
    assert result.company == "Acme Corp"
    assert "Python" in result.required_skills


@pytest.mark.asyncio
async def test_extract_jd_openai():
    jd_data = {
        "title": "Frontend Engineer",
        "company": "Beta Inc",
        "required_skills": ["React", "TypeScript"],
        "nice_to_haves": ["Next.js"],
        "seniority": "Mid",
        "red_flags": [],
    }

    with patch("src.agent._call_openai", return_value=jd_data):
        result = await extract_jd("Some job description text", api_key="sk-test", provider="openai")

    assert isinstance(result, JobDescription)
    assert result.title == "Frontend Engineer"
    assert result.company == "Beta Inc"


@pytest.mark.asyncio
async def test_score_cv_anthropic():
    score_data = {
        "match_percentage": 65,
        "gap_list": ["No Kubernetes experience"],
        "talking_points": ["Strong Python background"],
        "pitch": "Solid candidate with relevant skills. Some gaps in infrastructure. Worth interviewing.",
    }

    jd = JobDescription(
        title="Backend Engineer",
        company="Acme Corp",
        required_skills=["Python", "Kubernetes"],
        nice_to_haves=["Docker"],
        seniority="Senior",
        red_flags=[],
    )

    with patch("src.agent._call_anthropic", return_value=score_data):
        result = await score_cv(jd, "Some CV text here", api_key="sk-test", provider="anthropic")

    assert isinstance(result, CVScore)
    assert 0 <= result.match_percentage <= 100
    assert len(result.gap_list) > 0
    assert len(result.pitch) > 0


@pytest.mark.asyncio
async def test_score_cv_openai():
    score_data = {
        "match_percentage": 70,
        "gap_list": ["Missing AWS experience"],
        "talking_points": ["Good FastAPI knowledge"],
        "pitch": "Decent match for the role. A few gaps to address. Worth a conversation.",
    }

    jd = JobDescription(
        title="Backend Engineer",
        company="Acme Corp",
        required_skills=["Python"],
        nice_to_haves=[],
        seniority="Mid",
        red_flags=[],
    )

    with patch("src.agent._call_openai", return_value=score_data):
        result = await score_cv(jd, "Some CV text here", api_key="sk-test", provider="openai")

    assert isinstance(result, CVScore)
    assert result.match_percentage == 70


@pytest.mark.asyncio
async def test_rewrite_cv_anthropic():
    rewrite_data = {
        "tips": [
            {"section": "Skills", "problem": "Missing Kubernetes", "suggestion": "Add if you have any exposure"},
        ],
        "rewritten_cv": "Rewritten CV content here.",
    }

    jd = JobDescription(
        title="Backend Engineer",
        company="Acme Corp",
        required_skills=["Python"],
        nice_to_haves=[],
        seniority="Senior",
        red_flags=[],
    )

    with patch("src.agent._call_anthropic", return_value=rewrite_data):
        result = await rewrite_cv(jd, "Some CV text", api_key="sk-test", provider="anthropic")

    assert isinstance(result, CVRewrite)
    assert len(result.tips) == 1
    assert result.tips[0].section == "Skills"
    assert len(result.rewritten_cv) > 0
