<div align="center">

# DataGridle

### Master Data Interviews. Structured. Practical. Community-Driven.

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](#tech-stack)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](#tech-stack)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](#tech-stack)
[![DuckDB](https://img.shields.io/badge/SQL%20Sandbox-DuckDB--WASM-FFC107?style=for-the-badge)](#sql-sandbox)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](#license)

**A LeetCode-style interview preparation platform built specifically for Data Science, Data Engineering, Machine Learning, and Analytics roles.**

[Getting Started](#getting-started) · [Architecture](#architecture) · [Tech Stack](#tech-stack) · [API Reference](#api-reference) · [Contributing](#contributing)

</div>

---

## Product Vision

A structured, community-driven learning and interview preparation platform for **Data Science**, **Machine Learning**, **Data Engineering**, and **Analytics** — combining learning, practice, and discussion in one ecosystem.

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 14, React 18, TailwindCSS, Monaco Editor |
| **Backend** | FastAPI, SQLAlchemy 2.0 (async), Pydantic v2 |
| **Auth** | JWT (access + refresh tokens), OAuth2 |
| **Database** | PostgreSQL 16, Alembic migrations |
| **Cache** | Redis 7 |
| **SQL Sandbox** | DuckDB-WASM (in-browser, zero server cost) |
| **Deployment** | Docker Compose, GitHub Actions CI |

## Architecture

```
Frontend (Next.js :3000)
    │
    │  REST API
    ▼
Backend (FastAPI :8000)
    │
    ├── PostgreSQL (:5432)  — primary data
    ├── Redis (:6379)       — cache & sessions
    └── DuckDB-WASM         — SQL sandbox (runs in browser)
```

## Project Structure

```
DataGridle/
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # React components
│   │   ├── lib/             # API client, utilities
│   │   ├── hooks/           # Custom React hooks
│   │   └── types/           # TypeScript types
│   └── package.json
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/v1/         # API route handlers
│   │   ├── core/           # Config, database, security
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic & seed data
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── docker-compose.yml
├── .github/workflows/       # CI pipeline
└── .env.example
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### Quick Start (Docker)

```bash
git clone https://github.com/yourusername/DataGridle.git
cd DataGridle
cp .env.example .env
docker-compose up --build
```

Then visit:
- **Frontend:** http://localhost:3000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Default Admin Account

After seeding, log in with:
- **Email:** admin@datagridle.com
- **Password:** admin123

## API Reference

All endpoints are prefixed with `/api/v1`. Full interactive docs at `/docs` (Swagger UI).

| Module | Endpoints |
|---|---|
| **Auth** | `POST /auth/register`, `/auth/login`, `/auth/refresh-token`, `GET /auth/me` |
| **Users** | `GET /users/{id}/profile`, `PUT /users/{id}/profile`, `GET /users/leaderboard` |
| **Categories** | `GET /categories/`, `/categories/{id}/topics`, `/categories/{id}/daily-question` |
| **Questions** | `GET /questions/`, `POST /questions/`, `POST /questions/{id}/submit` |
| **Companies** | `GET /companies/`, `/companies/{id}/questions` |
| **Discussions** | `GET /discussions/`, `POST /discussions/`, comments, upvote/downvote |
| **Admin** | Pending creators/questions, approve/reject, analytics |

## Database Schema

Core entities: Users, Categories, Topics, Questions, Submissions, Companies, Discussions, Badges, Progress tracking. See `backend/app/models/` for full SQLAlchemy model definitions.

## Pages

| Route | Description |
|---|---|
| `/` | Landing page with category preview |
| `/auth/login` | Login |
| `/auth/register` | Registration |
| `/dashboard` | User dashboard with progress & streaks |
| `/questions` | Filterable question list |
| `/question/{id}` | Question detail + Monaco SQL editor |
| `/companies` | Company list |
| `/discuss` | Discussion forum |
| `/profile/{username}` | Public profile |
| `/admin/dashboard` | Admin panel |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.
