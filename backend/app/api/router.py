"""Compose versioned API routers."""

from fastapi import APIRouter

from app.routers.chat import router as chat_router
from app.routers.health import router as health_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(chat_router)
