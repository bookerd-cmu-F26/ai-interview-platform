from fastapi import FastAPI

from app.routers.user_router import router as user_router


app = FastAPI(
    title="AI Interview Platform",
    description="FastAPI backend for the AI Interview project",
    version="1.0.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


app.include_router(user_router)
