"""FastAPI dependencies for grounded response composition."""

from functools import lru_cache

from app.core.config import get_settings
from app.services.gemini_generator import GeminiGenerator
from app.services.grounded_answer import GroundedAnswerService


@lru_cache
def get_gemini_generator() -> GeminiGenerator:
    """Create the optional answer provider once; it stays inactive without a key."""

    settings = get_settings()
    return GeminiGenerator(
        api_key=settings.gemini_api_key,
        model=settings.generation_model,
        max_output_tokens=settings.max_generation_tokens,
    )


def get_grounded_answer_service() -> GroundedAnswerService:
    """Bind chat responses to the optional Gemini provider."""

    generator = get_gemini_generator()
    return GroundedAnswerService(generator=generator if generator.configured else None)
