from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.company import CompanyTag
from app.models.question import QuestionCompanyMap, Question, QuestionStatus
from app.schemas.company import CompanyResponse
from app.schemas.question import QuestionResponse

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.get("/", response_model=list[CompanyResponse])
async def list_companies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CompanyTag).order_by(CompanyTag.company_name))
    return result.scalars().all()


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CompanyTag).where(CompanyTag.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("/{company_id}/questions", response_model=list[QuestionResponse])
async def get_company_questions(company_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Question)
        .join(QuestionCompanyMap, QuestionCompanyMap.question_id == Question.id)
        .where(
            QuestionCompanyMap.company_id == company_id,
            Question.status == QuestionStatus.APPROVED,
        )
    )
    return result.scalars().all()
