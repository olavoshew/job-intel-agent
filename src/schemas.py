from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    title: str
    company: str
    required_skills: list[str]
    nice_to_haves: list[str]
    seniority: str
    red_flags: list[str]


class CVScore(BaseModel):
    match_percentage: int = Field(ge=0, le=100)
    gap_list: list[str]
    talking_points: list[str]
    pitch: str


class CVTip(BaseModel):
    section: str
    problem: str
    suggestion: str


class CVRewrite(BaseModel):
    tips: list[CVTip]
    rewritten_cv: str
