from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class DiscussionCreate(BaseModel):
    category: str
    title: str
    body: str


class DiscussionResponse(BaseModel):
    id: int
    author_id: UUID
    category: str
    title: str
    body: str
    upvotes: int
    downvotes: int
    is_locked: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    body: str
    parent_comment_id: int | None = None


class CommentResponse(BaseModel):
    id: int
    discussion_id: int
    author_id: UUID
    parent_comment_id: int | None
    body: str
    upvotes: int
    downvotes: int
    created_at: datetime

    model_config = {"from_attributes": True}
