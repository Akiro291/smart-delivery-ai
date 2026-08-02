# Smart Delivery AI

SaaS-платформа для управления сервисом доставки с поддержкой мультиролевого доступа и AI-инструментами.

> Модульный монолит на FastAPI с современной архитектурой и готовностью к масштабированию в микросервисы.

---

## О проекте

**Smart Delivery AI** — это платформа для автоматизации процессов доставки, предназначенная для компаний, управляющих курьерской логистикой. Система обеспечивает полный цикл управления заказами, от оформления до доставки, с поддержкой реального времени.

### Для кого

- **Владельцы бизнеса** — аналитика и контроль процессов
- **Менеджеры** — управление заказами и курьерами
- **Курьеры** — получение задач и обновление статуса доставки
- **Клиенты** — отслеживание заказов и коммуникация

### Роли пользователей

| Роль | Описание |
|------|----------|
| `ADMIN` | Полный доступ: пользователи, заказы, аналитика, настройки системы |
| `MANAGER` | Управление заказами, курьерами, клиентами |
| `COURIER` | Просмотр назначенных заказов, обновление статуса доставки |
| `CUSTOMER` | Создание заказов, отслеживание, история покупок |

---

## Возможности системы

### Реализовано

- **Аутентификация и авторизация**
  - Регистрация и вход пользователей
  - JWT-токены (access + refresh)
  - Ролевой доступ (RBAC)

- **Управление пользователями**
  - CRUD-операции с профилями
  - Управление ролями
  - Деактивация аккаунтов

- **Модели данных**
  - Заказы и их статусы
  - История изменения статусов
  - Трекинг доставки
  - Система уведомлений

- **API**
  - REST API с автодокументацией (Swagger UI / ReDoc)
  - Версионирование API (/api/v1/)

### В разработке

- Управление товарами и каталогом
- Панель менеджера (назначение курьеров, контроль)
- Личный кабинет курьера
- Личный кабинет клиента
- Аналитика и отчёты
- WebSocket-уведомления в реальном времени
- Telegram-бот для уведомлений
- Email-рассылки

### Запланировано

- AI-помощник для оптимизации маршрутов
- Прогнозирование времени доставки
- RAG-поиск по базе знаний
- Анализ отзывов клиентов
- Push-уведомления

---

## Архитектура

Проект использует подход **Modular Monolith** — единое развёртываемое приложение с чёткими границами модулей, готовое к выделению микросервисов по мере роста.

```
┌─────────────────────────────────────────────────────┐
│                   Nginx / Load Balancer              │
└──────────────────┬──────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
┌───────┐    ┌────────┐    ┌──────────┐
│  Nuxt │    │ Next.js│    │  Backend  │
│  3    │    │  (React)│    │ FastAPI  │
│Vue 3  │    │TypeScript│   │  :8000   │
└───────┘    └────────┘    └────┬─────┘
    Frontend                PostgreSQL :5432
                               Redis    :6379
                               Celery / RabbitMQ
```

### Слои приложения

```
API Layer (FastAPI Routes)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Database Layer (SQLAlchemy + PostgreSQL)
```

---

## Технологический стек

### Backend
| Технология | Версия | Назначение |
|-----------|--------|-----------|
| Python 3.12+ | — | Язык разработки |
| FastAPI | ≥0.109 | Веб-фреймворк |
| SQLAlchemy | ≥2.0.25 | ORM (async) |
| asyncpg | ≥0.29 | Асинхронный драйвер PostgreSQL |
| Alembic | ≥1.13 | Миграции БД |
| Pydantic | ≥2.6 | Валидация данных |
| python-jose | ≥3.3 | JWT-токены |
| passlib + bcrypt | ≥1.7 | Хеширование паролей |
| Celery | ≥5.3 | Фоновые задачи |
| Redis | ≥5.0 | Кэш / брокер задач |
| Uvicorn | ≥0.27 | ASGI-сервер |

### Frontend
| Технология | Назначение |
|-----------|-----------|
| Nuxt 3 (Vue 3) | Основной frontend |
| Next.js (React) | Альтернативный интерфейс |
| TypeScript | Типизация |
| Tailwind CSS | Стилизация |
| Pinia | Управление состоянием |

### DevOps
| Технология | Назначение |
|-----------|-----------|
| Docker / Docker Compose | Контейнеризация |
| GitHub Actions | CI/CD |
| Nginx | Reverse-proxy |

---

## Запуск проекта

### Требования

- Docker и Docker Compose
- Python 3.12+ (для локальной разработки)
- Node.js 18+ (для frontend)

### Быстрый старт через Docker

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/<your-username>/smart-delivery-ai.git
cd smart-delivery-ai
```

2. **Настройте переменные окружения:**
```bash
cp backend/.env.example backend/.env
# Отредактируйте backend/.env при необходимости
```

3. **Запустите сервисы:**
```bash
docker-compose -f docker-compose.yml up -d
```

4. **Создайте базу данных и выполните миграции:**
```bash
docker-compose -f docker-compose.yml exec backend alembic upgrade head
```

5. **Откройте браузер:**
| Сервис | Адрес |
|--------|-------|
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

### Локальная разработка

#### Backend

```bash
cd backend

# Создайте виртуальное окружение
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Запустите сервер
uvicorn app.main:app --reload --port 8000
```

#### Frontend — Nuxt 3

```bash
cd frontend/nuxt3-app
npm install
npm run dev
# http://localhost:3000
```

#### Frontend — Next.js

```bash
cd frontend/nextjs-app
npm install
npm run dev
# http://localhost:3001
```

---

## Структура проекта

```
smart-delivery-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/    # REST-эндпоинты
│   │   │       └── dependencies.py # Зависимости FastAPI
│   │   ├── core/                 # Конфигурация, безопасность, логирование
│   │   ├── db/
│   │   │   ├── models/           # SQLAlchemy модели
│   │   │   └── migrations/       # Alembic миграции
│   │   ├── modules/              # Бизнес-модули
│   │   ├── repositories/         # Слой доступа к данным
│   │   ├── services/             # Бизнес-логика
│   │   ├── schemas/              # Pydantic-схемы
│   │   └── main.py               # Точка входа
│   ├── tests/                    # Тесты
│   ├── alembic.ini               # Конфигурация Alembic
│   ├── requirements.txt          # Зависимости
│   └── Dockerfile
├── frontend/
│   ├── nuxt3-app/               # Nuxt 3 (Vue 3)
│   └── nextjs-app/              # Next.js (React)
├── docker-compose.yml           # Описание сервисов
├── .github/
│   └── workflows/               # CI/CD GitHub Actions
├── docs/                        # Документация
├── ARCHITECTURE.md              # Архитектура
└── DEVELOPMENT.md               # Гайд по разработке
```

---

## Разработка

### Работа с миграциями

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "описание изменений"

# Применить миграции
alembic upgrade head

# Откатить последнюю миграцию
alembic downgrade -1

# Показать текущую версию
alembic current
```

### Тестирование

```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app --cov-report=html
```

### Линтинг

```bash
flake8 app/ --max-line-length=120
mypy app/ --ignore-missing-imports
black app/ --check
isort app/ --check-only
```

### Рекомендации

- Следуйте [PEP 8](https://peps.python.org/pep-0008/)
- Используйте type hints везде
- Максимальная длина строки: 120 символов
- Асинхронные операции через `async/await`
- Каждый новый модуль должен иметь тесты

---

## Статус проекта

### ✅ Реализовано
- [x] Архитектура модульного монолита
- [x] Базовое FastAPI-приложение
- [x] Аутентификация (регистрация, логин, JWT)
- [x] Ролевой доступ (ADMIN, MANAGER, COURIER, CUSTOMER)
- [x] Модель пользователей с CRUD
- [x] Модели: Order, OrderHistory, DeliveryTracking, Notification
- [x] Слой репозиториев
- [x] Pydantic-схемы
- [x] Alembic-миграции
- [x] Docker-конфигурация
- [x] GitHub Actions CI/CD
- [x] Логирование
- [x] Frontend-скелет (Nuxt 3 + Next.js)

### 🚧 В разработке
- [ ] Панель администратора
- [ ] Управление заказами (CRUD)
- [ ] Личный кабинет курьера
- [ ] Личный кабинет клиента
- [ ] WebSocket-трекинг в реальном времени
- [ ] Фоновые задачи (Celery)
- [ ] Telegram-уведомления
- [ ] Email-уведомления

### 📋 Запланировано
- [ ] AI-оптимизация маршрутов
- [ ] Прогнозирование времени доставки
- [ ] Аналитика и дашборды
- [ ] RAG-поиск
- [ ] Mобильное приложение (React Native)
- [ ] Production-развёртывание

---

## License

MIT — см. [LICENSE](LICENSE) для подробностей.
