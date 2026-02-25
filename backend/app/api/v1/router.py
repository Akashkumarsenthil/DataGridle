from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, categories, questions, companies, discussions, admin, assessment

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(categories.router)
api_router.include_router(questions.router)
api_router.include_router(companies.router)
api_router.include_router(discussions.router)
api_router.include_router(admin.router)
api_router.include_router(assessment.router)
