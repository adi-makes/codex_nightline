"""Dependency-free process health endpoints."""

from datetime import UTC, datetime

from fastapi import APIRouter, Request

from app.core.config import get_settings
from app.models.health import ServiceStatus

router = APIRouter(tags=["health"])


def _service_status(request: Request) -> ServiceStatus:
    settings = get_settings()
    return ServiceStatus(
        service=settings.app_name,
        version=settings.version,
        environment=settings.environment,
        timestamp=datetime.now(UTC),
        request_id=request.state.request_id,
    )


@router.get("/health", response_model=ServiceStatus)
async def health(request: Request) -> ServiceStatus:
    """Report process health; no external dependency is checked at M0."""

    return _service_status(request)
