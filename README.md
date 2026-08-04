# FastAPI JWT Auth

A minimal FastAPI project with JWT access tokens and DB-backed, revocable refresh tokens.

## What's in `app/`

- `main.py` — FastAPI app instance, creates DB tables on startup, includes the router
- `config.py` — `Settings` (reads `DATABASE_URL`, `JWT_SECRET`, etc. from `.env`)
- `database.py` — async SQLAlchemy engine, session maker, `get_db` dependency
- `models.py` — `User` and `RefreshToken` tables
- `schemas.py` — Pydantic request/response models
- `auth.py` — password hashing, JWT create/decode, `get_current_user` dependency
- `routes.py` — the `/register`, `/login`, `/refresh`, `/logout`, `/me` endpoints

## Setup

1. Make sure Postgres is running and a database exists (matching `DATABASE_URL` below).

2. Create a `.env` file in the project root:

   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
   JWT_SECRET=some-long-random-secret
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

3. Install dependencies:

   ```bash
   uv sync
   ```

4. Run the app (tables are created automatically on startup):

   ```bash
   uv run uvicorn app.main:app --reload
   ```

5. Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive API docs.

## Endpoints

- `POST /register` — create a user
- `POST /login` — get an access + refresh token
- `POST /refresh` — exchange a refresh token for a new access + refresh token (rotates the old one)
- `POST /logout` — revoke a refresh token
- `GET /me` — returns the current user (requires `Authorization: Bearer <access_token>`)
