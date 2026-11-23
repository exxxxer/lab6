import time

from fastapi import FastAPI
from fastapi import Request

from app.config import Settings
from app.logging_setup import get_logger
from app.routers import items

settings = Settings()
app = FastAPI(
    title=settings.app_name,
    description="Лабораторная работа №6 «Введение в FastAPI». Работа с товарами.",
    version="1.0.0",
    contact={"name": "Студент", "email": settings.admin_email},
)
app.include_router(items.router)
logger = get_logger()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("%s %s -> ошибка сервера", request.method, request.url.path)
        raise
    elapsed_ms = (time.perf_counter() - started) * 1000
    logger.info("%s %s -> %d | %.1f ms", request.method, request.url.path, response.status_code, elapsed_ms)
    return response


@app.get("/", tags=["general"], summary="Главная страница")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/info", tags=["general"], summary="Настройки приложения")
def get_info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_page": settings.items_per_page,
    }
