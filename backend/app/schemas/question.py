from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class QuestionCreate(BaseModel):
    topic_id: int
    category_id: int
    title: str
    description: str
    question_type: str
    difficulty: str
    starter_code: str | None = None
    test_cases: dict | None = None
    expected_output: dict | None = None
    solution: str | None = None
    explanation: str | None = None
    dataset_id: int | None = None
    interview_year: int | None = None
    company_ids: list[int] | None = None


class QuestionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    difficulty: str | None = None
    starter_code: str | None = None
    test_cases: dict | None = None
    expected_output: dict | None = None
    solution: str | None = None
    explanation: str | None = None
    status: str | None = None


class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    category_id: int
    creator_id: UUID
    title: str
    description: str
    question_type: str
    difficulty: str
    starter_code: str | None
    status: str
    interview_year: int | None
    frequency_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class QuestionDetailResponse(QuestionResponse):
    test_cases: dict | None
    expected_output: dict | None
    explanation: str | None


class SubmissionCreate(BaseModel):
    submitted_code: str
    language: str


class SubmissionResponse(BaseModel):
    id: int
    question_id: int
    submitted_code: str
    language: str
    result: str
    execution_time_ms: int | None
    score: float | None
    submitted_at: datetime

    model_config = {"from_attributes": True}
