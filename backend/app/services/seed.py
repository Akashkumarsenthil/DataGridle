"""Seed the database with initial categories, topics, and sample questions."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category
from app.models.topic import Topic
from app.models.company import CompanyTag
from app.models.user import User, UserRole
from app.core.security import hash_password


CATEGORIES = [
    {"name": "Data Engineering", "slug": "data-engineering", "description": "SQL, ETL, data modeling, Spark, Airflow, and pipeline design"},
    {"name": "Data Science", "slug": "data-science", "description": "Statistics, pandas, hypothesis testing, A/B tests, and EDA"},
    {"name": "Machine Learning", "slug": "machine-learning", "description": "Model training, evaluation, feature engineering, NLP, and deep learning"},
    {"name": "Data Analytics", "slug": "data-analytics", "description": "Business metrics, dashboards, product analytics, and SQL"},
]

DE_TOPICS = [
    {"name": "SQL Basics", "difficulty_level": "easy", "order_index": 1},
    {"name": "SQL Joins", "difficulty_level": "easy", "order_index": 2},
    {"name": "Aggregations & GROUP BY", "difficulty_level": "easy", "order_index": 3},
    {"name": "Subqueries", "difficulty_level": "medium", "order_index": 4},
    {"name": "Window Functions", "difficulty_level": "medium", "order_index": 5},
    {"name": "CTEs & Recursive Queries", "difficulty_level": "medium", "order_index": 6},
    {"name": "Data Modeling", "difficulty_level": "hard", "order_index": 7},
    {"name": "ETL Pipelines", "difficulty_level": "hard", "order_index": 8},
    {"name": "Performance Optimization", "difficulty_level": "hard", "order_index": 9},
    {"name": "System Design", "difficulty_level": "very_hard", "order_index": 10},
]

COMPANIES = [
    {"company_name": "Google", "industry": "Technology"},
    {"company_name": "Amazon", "industry": "E-commerce / Cloud"},
    {"company_name": "Meta", "industry": "Social Media"},
    {"company_name": "Apple", "industry": "Technology"},
    {"company_name": "Netflix", "industry": "Streaming"},
    {"company_name": "Microsoft", "industry": "Technology"},
    {"company_name": "Uber", "industry": "Transportation"},
    {"company_name": "Stripe", "industry": "Fintech"},
    {"company_name": "Spotify", "industry": "Music / Streaming"},
    {"company_name": "Airbnb", "industry": "Travel / Hospitality"},
    {"company_name": "LinkedIn", "industry": "Social / Professional"},
    {"company_name": "Databricks", "industry": "Data / AI"},
    {"company_name": "Snowflake", "industry": "Data / Cloud"},
]


async def seed_database(db: AsyncSession):
    existing = await db.execute(select(Category).limit(1))
    if existing.scalar_one_or_none():
        return

    for cat_data in CATEGORIES:
        cat = Category(**cat_data)
        db.add(cat)
    await db.flush()

    de_cat = await db.execute(select(Category).where(Category.slug == "data-engineering"))
    de_category = de_cat.scalar_one()

    for topic_data in DE_TOPICS:
        topic = Topic(category_id=de_category.id, **topic_data)
        db.add(topic)

    for company_data in COMPANIES:
        company = CompanyTag(**company_data)
        db.add(company)

    admin = User(
        username="admin",
        email="admin@datagridle.com",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN,
        is_verified=True,
    )
    db.add(admin)

    await db.commit()
