"""Public contracts for guarded AI travel guidance."""

from typing import Literal

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Bounded user input for a stateless MVP chat request."""

    query: str = Field(min_length=2, max_length=400)


class GroundedAnswer(BaseModel):
    """A bounded travel-guidance response with transparent generation metadata."""

    answer: str
    evidence_status: Literal["source_metadata_present", "insufficient_evidence"]
    generation_mode: Literal[
        "gemini_general",
        "abstained",
    ]
    citations: list[dict[str, object]]
    suggested_followups: list[str]
    request_id: str
