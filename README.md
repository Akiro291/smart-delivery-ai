# Smart Delivery AI

SaaS-платформа для управления сервисом доставки с поддержкой мультиролевого доступа.

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

### ✅ Реализовано

- **Аутентификация и авторизация**
  - Регистрация и вход пользователей
  - JWT-токены (access + refresh)
  - Ролевой доступ (RBAC)
  - Эндпоинт `/auth/refresh` для обновления токенов
  - Восстановление пароля (одноразовый токен в Redis + email через Celery)
  - Rate limiting на auth-эндпоинтах

- **Управление пользователями**
  - CRUD-операции с профилями
  - Управление ролями (включая MANAGER)
  - Заявки на смену роли с апрувом админом (`/admin/roles`)

- **Заказы и state machine**
  - Валидация переходов статусов (PENDING → CONFIRMED → ASSIGNED → IN_PROGRESS → COMPLETED / CANCELLED)
  - Назначение курьеров (менеджер/админ): `POST /orders/{id}/assign`
  - История изменений статусов
  - Серверный пересчёт суммы, фиксация цен при checkout

- **Корзина и каталог**
  - Каталог товаров с фильтром по категориям
  - Корзина и оформление заказа
  - Загрузка изображений товаров

- **Real-time (WebSocket)**
  - `GET /api/v1/ws?token=...` — JWT-аутентифицированный WebSocket
  - Fan-out через Redis pub/sub
  - События: `tracking.updated`, `order.status_changed`, `order.assigned`
  - Обновление координат курьера: `PUT /delivery/order/{id}/location`

- **Фоновые задачи (Celery + RabbitMQ)**
  - Email/Telegram уведомления при смене статуса заказа
  - Восстановление пароля по email

- **AI-модуль**
  - Прогноз времени доставки (`GET /api/v1/ai/predict?order_id=`)
  - AI-ассистент (`POST /api/v1/ai/chat`) — эвристики или OpenAI (если задан ключ)

- **Аналитика**
  - Сводка заказов: `GET /api/v1/orders/stats/summary`
  - Дашборды менеджера и админа на реальных данных

- **API**
  - REST API с автодокументацией (Swagger UI / ReDoc)
  - Версионирование API (`/api/v1/`)

### 🚧 В разработке

- Оптимизация маршрутов (OR-Tools)
- RAG-поиск по базе знаний
- Интеграция карт-провайдеров
- Мобильное приложение (React Native)

---

## Архитектура

Проект использует подход **Modular Monolith** — единое развёртываемое приложение с чёткими границами модулей, готовое к выделению микросервисов по мере роста.

```
┌─────────────────────────────────────────────────────┐
│                   Nginx / Load Balancer              │
└──────────────────┬──────────────────────────────────┘
                    │
         ┌──────────┼──────────┐
         ▼          ▼          ▼
┌──────────┐    ┌──────────┐    ┌────────┐
│  Nuxt 3  │    │  Backend  │    │  Redis  │
│  (Vue 3) │    │ FastAPI   │    │ :6379  │
└──────────┘    │  :8000    │    └───┬────┘
                └─────┬─────┘        │
                      PostgreSQL     │
                      Celery / RabbitMQ
                      :5432          │
┌──────────────────┐                 │
│  PostgreSQL      │◄────────────────┘
│  :5432           │
└──────────────────┘
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
| bcrypt | ≥4.1.1 | Хеширование паролей |
| Celery | ≥5.3 | Фоновые задачи |
| Redis | ≥5.0 | Кэш / брокер задач |
| Uvicorn | ≥0.27 | ASGI-сервер |

### Frontend
| Технология | Назначение |
|-----------|-----------|
| Nuxt 3 (Vue 3) | Основной frontend |
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
# Отредактируйте backend/.env — ОБЯЗАТЕЛЬНО замените SECRET_KEY!
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
│   └── nuxt3-app/               # Nuxt 3 (Vue 3)
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
ruff check app/
ruff format app/ --check
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
- [x] Заявки на смену роли (страница /admin/roles)
- [x] Модели: Order, OrderHistory, DeliveryTracking, Notification
- [x] Слой репозиториев
- [x] Pydantic-схемы
- [x] Alembic-миграции
- [x] Docker-конфигурация (db, redis, rabbitmq, backend, celery, frontend)
- [x] GitHub Actions CI/CD
- [x] Логирование
- [x] Корзина и оформление заказа
- [x] Каталог товаров
- [x] State machine статусов заказов
- [x] Назначение курьеров менеджером/админом
- [x] WebSocket real-time (Redis pub/sub)
- [x] Celery + RabbitMQ: email/telegram уведомления
- [x] Восстановление пароля (Redis + email)
- [x] Rate limiting auth-эндпоинтов
- [x] AI: прогноз доставки + ассистент (эвристики/OpenAI)
- [x] Аналитика и дашборды на реальных данных

### 🚧 В разработке
- [ ] Оптимизация маршрутов (OR-Tools)
- [ ] Интеграция карт-провайдеров

### 📋 Запланировано
- [ ] RAG-поиск
- [ ] Мобильное приложение (React Native)
- [ ] Kubernetes для production

---

## License

MIT — см. [LICENSE](LICENSE) для подробностей.
