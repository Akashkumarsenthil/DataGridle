from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.database import engine, Base
from app.api.v1.router import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.database import async_session
    from app.services.seed import seed_database
    from sqlalchemy import text

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Add new columns to existing tables (idempotent for existing DBs)
        try:
            await conn.execute(text("""
                ALTER TABLE users ADD COLUMN IF NOT EXISTS assessment_completed_at TIMESTAMP WITH TIME ZONE
            """))
        except Exception:
            pass

    async with async_session() as session:
        await seed_database(session)

    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A LeetCode-style interview preparation platform for Data roles",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
