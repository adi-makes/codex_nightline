"""Compose guarded Gemini travel guidance."""

from __future__ import annotations

from app.models.chat import ChatRequest, GroundedAnswer
from app.services.gemini_generator import GeminiGenerator, GenerationUnavailable


class GroundedAnswerService:
    """Return useful, bounded advice while being clear about live-data limits."""

    def __init__(self, generator: GeminiGenerator | None = None) -> None:
        self._generator = generator

    async def answer(self, request: ChatRequest, request_id: str) -> GroundedAnswer:
        if self._generator is not None:
            try:
                answer = await self._generator.answer(request.query)
                return GroundedAnswer(
                    answer=answer,
                    evidence_status="insufficient_evidence",
                    generation_mode="gemini_general",
                    citations=[],
                    suggested_followups=[
                        "Plan a relaxed day in Fort Kochi",
                        "Suggest a rainy-day plan in Kochi",
                    ],
                    request_id=request_id,
                )
            except GenerationUnavailable:
                pass
        return GroundedAnswer(
            answer=("I can't generate a reliable answer right now. Please try again in a moment."),
            evidence_status="insufficient_evidence",
            generation_mode="abstained",
            citations=[],
            suggested_followups=[
                "Plan a relaxed day in Fort Kochi",
                "Suggest a rainy-day plan in Kochi",
            ],
            request_id=request_id,
        )
