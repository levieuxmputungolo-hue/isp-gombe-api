from pydantic import BaseModel
from typing import Optional


class SearchRequest(BaseModel):
    full_name: str
    promotion: str
    level: str
    option: str = ""
    section: str = ""


class ResultOut(BaseModel):
    course_name: str
    semester: str
    score: float
    grade: str
    credits: int

    class Config:
        from_attributes = True


class StudentOut(BaseModel):
    full_name: str
    promotion: str
    level: str
    option: str = ""
    section: str = ""
    university: Optional[str] = None
    results: list[ResultOut] = []

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
