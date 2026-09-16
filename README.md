# HRIS Platform

Multi-tenant HRIS SaaS foundation with a platform administration layer and a deployable FastAPI backend.

## Architecture

- Frontend: standalone HTML prototypes (migration-ready for React/Next.js)
- Backend: Python 3.12 + FastAPI
- Database: PostgreSQL 16
- ORM: SQLAlchemy 2
- Migrations: Alembic
- Containerization: Docker + Docker Compose
- API documentation: OpenAPI / Swagger at `/docs`

## Backend structure

```text
backend/
├── app/
│   ├── core/          # configuration and security foundations
│   ├── models/        # database models
│   ├── schemas/       # API validation schemas
│   ├── services/      # business logic
│   ├── api/           # versioned API routes
│   ├── db.py          # database session / engine
│   └── main.py        # FastAPI entry point
├── alembic/           # database migrations
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Local deployment

Requirements: Docker Desktop.

```bash
docker compose up --build
```

API: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`
Health: `http://localhost:8000/api/v1/health`

## Production notes

Set secrets through the deployment platform rather than committing `.env`. Replace the development database password and JWT secret before production. PostgreSQL should use managed storage/backups in production.

The backend is designed as the foundation for the HRIS authorization model:

```text
USER → ROLE → MODULE ACCESS → PERMISSION → ACTION + SCOPE
                 └────────────→ APPROVAL AUTHORITY
```

Tenant isolation should be enforced with `corporate_id` plus database-level access policies as the application matures.
