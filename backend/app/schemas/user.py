from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    experience_level: str | None = None
    target_role: str | None = None
    # requested platform role; only 'user' gets immediate full access.
    # 'creator' accounts require admin approval via is_verified flag.
    role: str = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    role: str
    is_verified: bool
    experience_level: str | None
    target_role: str | None
    avatar_url: str | None
    streak_count: int
    assessment_completed_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserProfileUpdate(BaseModel):
    username: str | None = None
    experience_level: str | None = None
    target_role: str | None = None
    target_companies: list[str] | None = None
    avatar_url: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class DomainPreferenceResponse(BaseModel):
    duration_weeks: int


class DomainPreferenceUpdate(BaseModel):
    duration_weeks: int
