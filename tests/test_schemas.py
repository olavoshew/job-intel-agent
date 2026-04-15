import pytest
from pydantic import ValidationError

from src.schemas import CVRewrite, CVScore, CVTip, JobDescription


def test_valid_job_description():
    jd = JobDescription(
        title="Backend Engineer",
        company="Acme Corp",
        required_skills=["Python", "FastAPI"],
        nice_to_haves=["Docker"],
        seniority="Senior",
        red_flags=["No visa sponsorship"],
    )
    assert jd.title == "Backend Engineer"
    assert len(jd.required_skills) == 2


def test_missing_required_field():
    with pytest.raises(ValidationError):
        JobDescription(
            title="Backend Engineer",
            required_skills=["Python"],
            nice_to_haves=[],
            seniority="Senior",
            red_flags=[],
        )


def test_valid_cv_score():
    score = CVScore(
        match_percentage=75,
        gap_list=["No Kubernetes experience"],
        talking_points=["Strong Python background"],
        pitch="Good fit overall.",
    )
    assert score.match_percentage == 75


def test_cv_score_too_high():
    with pytest.raises(ValidationError):
        CVScore(
            match_percentage=150,
            gap_list=[],
            talking_points=[],
            pitch="N/A",
        )


def test_cv_score_negative():
    with pytest.raises(ValidationError):
        CVScore(
            match_percentage=-10,
            gap_list=[],
            talking_points=[],
            pitch="N/A",
        )


def test_valid_cv_rewrite():
    rewrite = CVRewrite(
        tips=[CVTip(section="Skills", problem="Missing Redis", suggestion="Add Redis")],
        rewritten_cv="Updated CV content here.",
    )
    assert len(rewrite.tips) == 1
    assert rewrite.tips[0].section == "Skills"
    assert len(rewrite.rewritten_cv) > 0


def test_cv_rewrite_missing_field():
    with pytest.raises(ValidationError):
        CVRewrite(tips=[])
