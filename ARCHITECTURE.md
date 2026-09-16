# HRIS Platform Architecture

## 1. System Overview

```text
HRIS PLATFORM
│
├── PRESENTATION LAYER
│   ├── Super Admin Web App
│   ├── Platform Admin CRM Web App
│   ├── Platform Admin Finance Web App
│   └── Corporate HRIS Web App
│
├── API / APPLICATION LAYER
│   └── FastAPI
│       ├── Authentication
│       ├── Authorization / RBAC
│       ├── Corporate Management
│       ├── User Management
│       ├── Module Management
│       ├── Approval Engine
│       ├── HRIS Services
│       ├── CRM Services
│       ├── Finance Services
│       ├── Notification Service
│       └── Audit Service
│
├── DOMAIN LAYER
│   ├── Organization
│   ├── People
│   ├── Attendance
│   ├── Leave
│   ├── Performance
│   ├── Payroll
│   ├── Recruitment
│   ├── CRM
│   └── Finance
│
├── DATA LAYER
│   ├── PostgreSQL
│   ├── SQLAlchemy ORM
│   ├── Alembic Migrations
│   └── Redis (optional)
│
└── INFRASTRUCTURE
    ├── Docker
    ├── Docker Compose
    ├── CI/CD
    ├── Reverse Proxy
    ├── Monitoring
    └── Backup & Recovery
```

## 2. Multi-Tenant Architecture

Every corporate is an isolated tenant.

```text
PLATFORM
│
├── Corporate A
│   ├── Users
│   ├── Roles
│   ├── Employees
│   ├── Attendance
│   ├── Leave
│   └── Payroll
│
├── Corporate B
│   └── isolated tenant data
│
└── Corporate C
    └── isolated tenant data
```

Tenant isolation is enforced at the application and database levels using `corporate_id` and PostgreSQL Row Level Security where applicable.

## 3. Access Control

```text
USER
 ↓
USER ROLE
 ↓
ROLE
 ↓
MODULE ACCESS
 ↓
PERMISSION
 ↓
ACTION
 ↓
SCOPE
```

Example:

```text
HR Manager
 ├── Employee → View → Corporate
 ├── Employee → Edit → Corporate
 ├── Attendance → View → Corporate
 ├── Attendance → Approve → Department
 └── Payroll → Approve → Corporate
```

Supported actions include View, Create, Edit, Delete, Approve, Export, Import and module-specific actions.

Supported scopes include Own, Team, Department, Branch, Corporate and Global.

## 4. Approval Architecture

Approval authority is independent from ordinary data access.

```text
REQUESTER
   ↓
APPROVAL WORKFLOW
   ↓
APPROVAL STEP 1
   ↓
APPROVAL STEP 2
   ↓
FINAL APPROVAL
```

Workflows include Leave Request, Attendance Correction, Overtime, Expense, Recruitment and Payroll.

General workflows provide platform defaults. Corporate overrides can customize approval rules per tenant.

## 5. Platform Roles

```text
SUPER ADMIN
├── Global Governance
├── Corporate Management
├── User Management
├── Role & Permission
├── Module Management
├── Security
├── System Settings
└── Integrations

PLATFORM ADMIN - CRM
├── Customers
├── Leads
├── Pipeline
├── Activities
├── Follow Up
└── CRM Corporate Accounts

PLATFORM ADMIN - FINANCE
├── Subscriptions
├── Payment Verification
├── Payment History
├── Service Monitoring
├── Renewal
└── Finance Corporate Accounts

CORPORATE SIDE
├── Corporate Admin
├── HR
├── Finance
├── Operations
├── CRM
└── Employee
```

## 6. Backend Service Boundaries

The initial implementation uses a modular monolith. This keeps deployment simple while maintaining clear domain boundaries. Individual services can later be extracted if scale requires it.

```text
backend/app/
├── api/
│   └── v1/
│       ├── auth.py
│       ├── corporates.py
│       ├── users.py
│       ├── roles.py
│       ├── permissions.py
│       ├── modules.py
│       ├── approvals.py
│       ├── employees.py
│       ├── attendance.py
│       ├── leave.py
│       ├── payroll.py
│       ├── recruitment.py
│       ├── crm.py
│       └── finance.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── logging.py
│   └── exceptions.py
│
├── db/
│   ├── session.py
│   ├── base.py
│   └── models/
│
├── schemas/
├── services/
├── repositories/
├── middleware/
└── main.py
```

## 7. Database Model

Core entities:

```text
corporates
branches
organizations
positions
users
employees
roles
modules
permissions
role_permissions
module_access
user_roles
approval_workflows
approval_steps
audit_logs
notifications
```

HRIS entities:

```text
attendance
attendance_corrections
shifts
schedules
leave_requests
leave_balances
overtime
salary_components
payroll_runs
payslips
vacancies
candidates
interviews
performance_reviews
tasks
```

Platform CRM entities:

```text
crm_customers
crm_leads
crm_pipeline_stages
crm_opportunities
crm_activities
crm_follow_ups
```

Platform Finance entities:

```text
subscriptions
plans
invoices
payments
payment_verifications
renewals
service_status
```

## 8. API Structure

Base URL:

```text
/api/v1
```

Example resources:

```text
POST   /auth/login
POST   /auth/refresh
GET    /me

GET    /corporates
POST   /corporates
GET    /corporates/{id}
PATCH  /corporates/{id}

GET    /users
POST   /users
PATCH  /users/{id}

GET    /roles
POST   /roles
PATCH  /roles/{id}

GET    /modules
GET    /permissions
GET    /approvals/workflows

GET    /employees
GET    /attendance
GET    /leave/requests
GET    /payroll/runs
GET    /recruitment/candidates

GET    /crm/customers
GET    /crm/leads
GET    /crm/pipeline

GET    /finance/subscriptions
GET    /finance/payments
GET    /finance/renewals

GET    /health
```

## 9. Security Architecture

```text
Client
 ↓ HTTPS
Reverse Proxy
 ↓
FastAPI
 ↓
Authentication
 ↓
Authorization / RBAC
 ↓
Tenant Resolution
 ↓
Service Layer
 ↓
Repository
 ↓
PostgreSQL
```

Security requirements:

- Password hashing with Argon2/bcrypt-compatible strategy.
- Short-lived access tokens and refresh tokens.
- Role and permission checks on every protected endpoint.
- Tenant isolation using `corporate_id`.
- Input validation through Pydantic.
- Secrets supplied through environment variables.
- Audit logging for sensitive administrative actions.
- Rate limiting at the edge/API layer.
- CORS restricted by environment.
- Production database credentials never committed to Git.

## 10. Docker Architecture

```text
Docker Compose
│
├── api
│   └── FastAPI application
│
├── postgres
│   └── PostgreSQL database
│
├── redis (optional)
│   └── Cache / background jobs
│
└── nginx (production option)
    └── Reverse proxy / TLS
```

Development:

```bash
docker compose up --build
```

Production should use managed PostgreSQL where practical, external secret management, HTTPS, backups, health checks and resource limits.

## 11. Deployment Target

The application is containerized so it can be deployed to most Docker-capable environments, including a VPS or cloud container platform.

Recommended production topology:

```text
DNS
 ↓
CDN / WAF
 ↓
Reverse Proxy / Load Balancer
 ↓
FastAPI Container(s)
 ↓
Managed PostgreSQL
 ↓
Object Storage / Backup
```

## 12. Observability

The production system should expose:

```text
/health
/ready
/metrics
```

Track:

- API latency
- HTTP error rate
- Database connection health
- Background job failures
- Authentication failures
- Active sessions
- Tenant activity
- Application uptime

## 13. CI/CD

Target pipeline:

```text
Git Push
 ↓
GitHub Actions
 ↓
Lint
 ↓
Unit Tests
 ↓
Integration Tests
 ↓
Docker Build
 ↓
Security Scan
 ↓
Deploy Staging
 ↓
Smoke Test
 ↓
Production Deploy
```

## 14. Architecture Principle

Start as a modular monolith, not a collection of microservices. Keep domain boundaries explicit, APIs versioned, tenant isolation enforced and infrastructure containerized. Split services only when there is a demonstrated operational or scaling reason.
