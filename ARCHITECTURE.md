# Smart Delivery AI Platform - Architecture

## Overview

Production-ready modular monolith AI-powered delivery management platform with FastAPI backend and modern frontend frameworks.

## Architecture Principles

### Modular Monolith
- Single deployable unit with clean module boundaries
- Clear separation of concerns between business domains
- Easy to extract microservices when needed
- Shared database with domain-specific schemas

### Layered Architecture
```
API Layer (FastAPI Routes)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Database Layer (SQLAlchemy + PostgreSQL)
```

### Domain-Driven Design
- Customer, Courier, Manager, Admin domains
- Clear domain boundaries and interfaces
- Event-driven communication between domains
- CQRS pattern preparation

## Tech Stack

### Backend
- Python 3.12
- FastAPI (async web framework)
- SQLAlchemy 2.0 (ORM)
- PostgreSQL + pgvector (vector database)
- Redis (caching, sessions)
- Celery (background tasks)
- RabbitMQ (message broker)
- WebSocket (real-time updates)
- JWT (authentication)
- Alembic (migrations)

### Frontend
- Nuxt 3 (Vue 3 + TypeScript) — единственный frontend
- Tailwind CSS
- Pinia (state management)
- WebSocket (real-time tracking)

### AI
- OpenAI API
- LangChain
- RAG architecture
- embeddings
- pgvector

### DevOps
- Docker & Docker Compose
- Nginx (reverse proxy)
- GitHub Actions (CI/CD)
- Prometheus + Grafana (monitoring)
- ELK Stack (logging)

## Project Structure

```
smart-delivery-ai/
├── backend/
│   ├── app/
│   │   ├── api/                    # API routes
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/     # REST endpoints
│   │   │   │   └── dependencies.py
│   │   │   └── __init__.py
│   │   ├── core/                  # Core functionality
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── utils.py
│   │   ├── db/                    # Database layer
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   ├── models/           # SQLAlchemy models
│   │   │   └── migrations/       # Alembic migrations
│   │   ├── modules/               # Business modules
│   │   │   ├── users/
│   │   │   ├── orders/
│   │   │   ├── delivery/
│   │   │   ├── notifications/
│   │   │   └── ai/
│   │   ├── services/              # Business logic
│   │   │   ├── users_service.py
│   │   │   ├── orders_service.py
│   │   │   └── ...
│   │   ├── repositories/          # Data access layer
│   │   │   ├── users_repo.py
│   │   │   ├── orders_repo.py
│   │   │   └── ...
│   │   └── main.py               # Application entry point
│   ├── tests/                    # Test suite
│   ├── alembic.ini
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── nuxt3-app/               # Nuxt 3 application
│       ├── pages/
│       ├── components/
│       ├── stores/
│       └── ...
├── docker/
│   ├── docker-compose.yml
│   ├── nginx/                   # Nginx configuration
│   └── scripts/                 # Deployment scripts
├── docs/                        # Documentation
├── .github/
│   └── workflows/              # CI/CD pipelines
└── README.md
```

## Module Structure

### 1. Users Module
- User registration and authentication
- Role management (CUSTOMER, COURIER, MANAGER, ADMIN)
- Profile management
- Password recovery

### 2. Orders Module
- Order creation and management
- Status tracking
- Courier assignment
- Order history

### 3. Delivery Module
- Real-time delivery tracking
- WebSocket updates
- Location tracking
- Estimated delivery times

### 4. Notifications Module
- Telegram Bot integration
- Email notifications
- In-app notifications
- Notification preferences

### 5. AI Module (Future)
- AI assistant for customers
- Review analysis
- Delivery time prediction
- RAG-based information retrieval
- Smart routing optimization

## Data Flow

### User Authentication Flow
1. User registers/logs in via API
2. JWT tokens generated (access + refresh)
3. Tokens validated on each request
4. User roles checked for authorization

### Order Creation Flow
1. Customer creates order via API
2. Order validated and saved to database
3. Event published to RabbitMQ
4. Notifications sent via Telegram/Email
5. Order assigned to available courier

### Real-time Tracking Flow
1. Courier updates location
2. WebSocket broadcast to interested clients
3. Order status updated in database
4. Notifications sent to customer

## Security

- JWT token-based authentication
- Password hashing with bcrypt
- Role-based authorization
- SQL injection prevention via SQLAlchemy
- XSS prevention via FastAPI
- Rate limiting
- CORS configuration

## Performance

- Async/await throughout
- Connection pooling
- Redis caching
- Background tasks with Celery
- WebSocket for real-time updates
- Database indexing

## Monitoring & Logging

- Structured logging with context
- Error tracking (Sentry integration)
- Metrics collection (Prometheus)
- Dashboard (Grafana)
- Centralized logging (ELK)

## CI/CD

- Automated testing
- Code quality checks (flake8, mypy)
- Docker image building
- Automated deployment to staging
- Manual deployment to production

## Deployment

- Docker Compose for local development
- Kubernetes for production (prepared)
- Environment-specific configuration
- Secret management
- Health checks
- Graceful shutdown

## Future Enhancements

- Microservices extraction when needed
- Multi-tenancy support
- GraphQL API
- Mobile apps (React Native)
- Advanced AI features
- Multi-language support
- Dark mode
- PWA support