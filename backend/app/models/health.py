"""Health and readiness response contracts."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ServiceStatus(BaseModel):
    """Public process status without claiming unavailable dependency checks."""

    service: str
    version: str
    environment: str
    status: Literal["ok"] = "ok"
    timestamp: datetime = Field(description="UTC timestamp when the response was generated.")
    request_id: str
