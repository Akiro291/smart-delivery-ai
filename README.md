# Smart Delivery AI Platform

AI-powered delivery management platform with modern tech stack.

## Features

- **Multi-role Support**: Customer, Courier, Manager, Admin roles
- **Real-time Tracking**: WebSocket-based delivery tracking
- **AI-powered Features**: Predictive analytics, review analysis, route optimization
- **Notification System**: Telegram and Email notifications
- **Modern Tech Stack**: FastAPI, PostgreSQL, Redis, Celery
- **Docker Ready**: Complete Docker Compose setup

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- SQLAlchemy 2.0 (Async)
- PostgreSQL + pgvector
- Redis
- Celery
- RabbitMQ
- JWT Authentication
- WebSocket

### Frontend
- Nuxt 3 (Vue 3 + TypeScript)
- Next.js (React + TypeScript)
- Tailwind CSS

### DevOps
- Docker & Docker Compose
- GitHub Actions CI/CD
- Nginx reverse proxy

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.12 (for local development)
- Node.js 20+ (for frontend development)

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-username/smart-delivery-ai.git
cd smart-delivery-ai
```

2. Start the backend with Docker:
```bash
cd docker
docker-compose up -d
```

3. Access the API:
- API docs: http://localhost:8000/docs
- API: http://localhost:8000

4. Run database migrations:
```bash
docker-compose exec backend alembic upgrade head
```

## Development

### Backend Development

1. Set up Python environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

3. Run migrations:
```bash
cd backend
alembic upgrade head
```

4. Start development server:
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend Development

#### Nuxt 3
```bash
cd frontend/nuxt3-app
npm install
npm run dev
```

#### Next.js
```bash
cd frontend/nextjs-app
npm install
npm run dev
```

## Project Structure

```
smart-delivery-ai/
├── backend/
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── db/           # Database layer
│   │   ├── modules/      # Business modules
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access layer
│   │   └── schemas/      # Pydantic schemas
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── nuxt3-app/        # Nuxt 3 application
│   └── nextjs-app/       # Next.js application
├── docker/
│   ├── docker-compose.yml
│   └── nginx/           # Nginx configuration
├── .github/workflows/   # CI/CD
└── docs/
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

See `backend/.env.example` for all available environment variables.

## Docker Services

- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- RabbitMQ: `localhost:5672`
- Management UI: `http://localhost:15672`
- Backend API: `localhost:8000`
- Frontend: `localhost:3000`

## Monitoring

- API logs: `docker-compose logs -f backend`
- Database logs: `docker-compose logs -f db`
- Redis logs: `docker-compose logs -f redis`

## Next Steps

1. Implement business logic
2. Add unit and integration tests
3. Set up CI/CD pipeline
4. Deploy to production environment
5. Configure SSL certificates
6. Set up monitoring and alerting

## License

MIT License - see LICENSE file for details