# AGENTS.md — Инструкции для AI-агентов и разработчиков

Проект: **Smart Delivery AI** — SaaS-платформа доставки (модульный монолит FastAPI + Nuxt 3).

## Суть проекта

- **Backend**: `backend/` — FastAPI (async), SQLAlchemy 2.0 + asyncpg, PostgreSQL, Alembic, JWT-аутентификация, RBAC (CUSTOMER / COURIER / MANAGER / ADMIN), Celery + Redis + RabbitMQ, WebSocket real-time.
- **Frontend**: `frontend/nuxt3-app/` — Nuxt 3, TypeScript, Tailwind, Pinia. UI на русском языке.
- **Слои backend**: `api/v1/endpoints` → `services` → `repositories` → `db/models`. Не нарушать эту последовательность: эндпоинт не обращается к репозиторию напрямую.

## Команды

### Backend (из `backend/`, venv активирован)
```bash
uvicorn app.main:app --reload --port 8000   # запуск
pytest tests/ -v                            # тесты (нужен живой PostgreSQL, см. backend/.env)
ruff check app/                             # линт
ruff format app/                            # форматирование
alembic upgrade head                        # миграции
alembic revision --autogenerate -m "..."    # новая миграция
```

### Frontend (из `frontend/nuxt3-app/`)
```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # проверка сборки
npm run test       # vitest
npm run test:e2e   # playwright
```

### Docker (из корня)
```bash
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.yml exec backend alembic upgrade head
```

## Правила кодирования

### Backend
- Python 3.12+, type hints везде, макс. длина строки 120 (см. `ruff.toml`).
- Всё I/O — через `async/await`. Синхронный код в эндпоинтах запрещён.
- Схемы Pydantic v2 в `app/schemas/`, модели SQLAlchemy 2.0 в `app/db/models/`.
- Каждое изменение схемы БД — через Alembic-миграцию. Не редактировать применённые миграции.
- Доступ по ролям — через зависимости `app/api/v1/dependencies.py` (`require_role`, `require_admin`).
- Секреты только через `backend/.env` (шаблон: `backend/.env.example`). `SECRET_KEY` обязателен.
- Каждый новый модуль/эндпоинт сопровождается тестами в `backend/tests/`.

### Frontend
- Vue 3 `<script setup lang="ts">`, Composition API.
- Состояние — Pinia (`stores/`), запросы — через `useApi` / `$fetch` с `runtimeConfig.public.apiBase`. Не хардкодить `http://localhost:8000`.
- Проверка доступа — через middleware (`auth`, `guest`, `admin`, `courier`, `customer`) в `definePageMeta` страницы. В layout-файлах `definePageMeta` не работает.
- Русский язык UI — сохранять.
- Не оставлять мок-данные в страницах, которые подключены к API: данные только из сторов/API.

## Известные проблемы (исторические — не воспроизводить паттерн)

- В frontend ранее лежали мусорные `__init__.py` (артефакты скаффолда) — при встрече удалять.
- Исторические баги: middleware `customer.ts` зацикливал редирект, `guest.ts` был инвертирован, `websocket.ts`/`apiClient.ts` были заглушками, тесты-файлы содержали python-комментарии. Проверять, что исправлено, и не воспроизводить.
- `Notification.sent_at` / `DeliveryTracking.last_updated` были Integer — исправлены миграцией 004 на timestamptz.

## Что нельзя делать

- Не коммитить `.env`, секреты, токены, `node_modules`, `venv/`, `.venv/`, `__pycache__/`, `.nuxt/`.
- Не переписывать проект на микросервисы — архитектура «модульный монолит», границы модулей сохранять.
- Не добавлять второй frontend (Next.js из старого ARCHITECTURE.md — не развиваем, только Nuxt 3).
- Не ломать обратную совместимость `/api/v1` — ломающие изменения только в новой версии API.
- Не редактировать применённые Alembic-миграции — только новые ревизии.
