"""FastAPI application factory for Ask Kochi."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.request_id import RequestIdMiddleware
from app.dependencies.answers import get_gemini_generator


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Release the optional Gemini client on shutdown."""
    yield
    if get_gemini_generator.cache_info().currsize:
        await get_gemini_generator().close()


def create_app() -> FastAPI:
    """Create the API without connecting to unconfigured external services."""

    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version, lifespan=lifespan)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-Request-ID"],
    )
    app.include_router(api_router)
    return app


app = create_app()
