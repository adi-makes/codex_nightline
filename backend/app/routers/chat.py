"""Single stateless chat endpoint for the MVP."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.dependencies.answers import get_grounded_answer_service
from app.models.chat import ChatRequest, GroundedAnswer
from app.services.grounded_answer import GroundedAnswerService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=GroundedAnswer)
async def create_answer(
    request: Request,
    body: ChatRequest,
    service: Annotated[GroundedAnswerService, Depends(get_grounded_answer_service)],
) -> GroundedAnswer:
    """Return guarded travel guidance without storing user data."""

    return await service.answer(body, request.state.request_id)
