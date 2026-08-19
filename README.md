# AI Interview User Service

A basic FastAPI User Service using layered architecture and in-memory storage.

## Project Structure

```text
app/
├── main.py
├── models/
│   └── user.py
├── repositories/
│   └── user_repository.py
├── services/
│   └── user_service.py
└── routers/
    └── user_router.py
```

## Setup

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## APIs

- `GET /health`
- `POST /users`
- `GET /users`
- `GET /users/{user_id}`
- `PATCH /users/{user_id}`
- `DELETE /users/{user_id}`
