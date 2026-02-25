from pydantic import BaseModel


class AssessmentQuestionResponse(BaseModel):
    id: int
    topic_id: int
    category_id: int
    question_text: str
    question_type: str
    options: dict | None
    scale_max: int | None
    order_index: int

    model_config = {"from_attributes": True}


class AssessmentAnswerSubmit(BaseModel):
    question_id: int
    answer_value: str


class AssessmentSubmitRequest(BaseModel):
    answers: list[AssessmentAnswerSubmit]


class TopicStrengthResponse(BaseModel):
    topic_id: int
    topic_name: str
    category_id: int
    category_slug: str
    category_name: str
    score: float
    strength_label: str


class UserProfileWithStrengthsResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    is_verified: bool
    experience_level: str | None
    target_role: str | None
    avatar_url: str | None
    streak_count: int
    assessment_completed_at: str | None
    topic_strengths: list[TopicStrengthResponse]
    created_at: str
