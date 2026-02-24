from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.discussion import Discussion, DiscussionComment
from app.schemas.discussion import (
    DiscussionCreate,
    DiscussionResponse,
    CommentCreate,
    CommentResponse,
)

router = APIRouter(prefix="/discussions", tags=["Discussions"])


@router.get("/", response_model=list[DiscussionResponse])
async def list_discussions(
    db: AsyncSession = Depends(get_db),
    category: str | None = None,
    limit: int = Query(default=50, le=100),
    offset: int = 0,
):
    query = select(Discussion)
    if category:
        query = query.where(Discussion.category == category)
    query = query.order_by(Discussion.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=DiscussionResponse, status_code=status.HTTP_201_CREATED)
async def create_discussion(
    data: DiscussionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    discussion = Discussion(
        author_id=current_user.id,
        **data.model_dump(),
    )
    db.add(discussion)
    await db.flush()
    await db.refresh(discussion)
    return discussion


@router.get("/{discussion_id}", response_model=DiscussionResponse)
async def get_discussion(discussion_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Discussion).where(Discussion.id == discussion_id))
    discussion = result.scalar_one_or_none()
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    return discussion


@router.get("/{discussion_id}/comments", response_model=list[CommentResponse])
async def get_comments(discussion_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DiscussionComment)
        .where(DiscussionComment.discussion_id == discussion_id)
        .order_by(DiscussionComment.created_at.asc())
    )
    return result.scalars().all()


@router.post("/{discussion_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    discussion_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Discussion).where(Discussion.id == discussion_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Discussion not found")

    comment = DiscussionComment(
        discussion_id=discussion_id,
        author_id=current_user.id,
        body=data.body,
        parent_comment_id=data.parent_comment_id,
    )
    db.add(comment)
    await db.flush()
    await db.refresh(comment)
    return comment


@router.post("/{discussion_id}/upvote")
async def upvote_discussion(
    discussion_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Discussion).where(Discussion.id == discussion_id))
    discussion = result.scalar_one_or_none()
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    discussion.upvotes += 1
    return {"upvotes": discussion.upvotes}


@router.post("/{discussion_id}/downvote")
async def downvote_discussion(
    discussion_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Discussion).where(Discussion.id == discussion_id))
    discussion = result.scalar_one_or_none()
    if not discussion:
        raise HTTPException(status_code=404, detail="Discussion not found")
    discussion.downvotes += 1
    return {"downvotes": discussion.downvotes}
