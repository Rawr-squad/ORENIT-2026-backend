# OPENIT-2026-backend

Backend для платформы обучающих курсов с геймификацией, системой достижений, магазином, комментариями и realtime-чатом.

---

## Стек

* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy + Alembic**
* **Docker / Docker Compose**
* **WebSocket (чат)**

---

## Старт

### 1. Клонирование проекта

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

### 2. Настройка `.env`

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=edu
POSTGRES_PORT=5432

DATABASE_URL=postgresql://postgres:postgres@db:5432/edu

BACKEND_PORT=8000
```

---

### 3. Запуск контейнеров

```bash
docker-compose up --build
```

После этого:

* Backend: http://localhost:8000
* Swagger: http://localhost:8000/docs

---

## ВАЖНО: Первый запуск (миграции)

После первого запуска необходимо вручную применить миграции:

```bash
docker exec -it backend bash
```

Внутри контейнера выполнить:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## Создание администратора (обязательно)

В системе нет сидера admin-пользователя — его нужно создать вручную.

---

### Шаг 1. Зарегистрировать пользователя

Через Swagger (`/auth/register`) создать пользователя:

```json
{
  "email": "admin@example.com",
  "password": "admin123",
  "nickname": "Admin",
  "role": "student"
}
```

---

### Шаг 2. Изменить роль на admin

Подключиться к базе:

```bash
docker exec -it db psql -U postgres -d edu
```

Выполнить SQL:

```sql
UPDATE users
SET role = 'admin'
WHERE email = 'admin@example.com';
```