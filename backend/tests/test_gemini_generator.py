"""Provider failover tests for concise LLM answers."""

import pytest

from app.services.gemini_generator import GeminiGenerator


@pytest.mark.anyio
async def test_generator_uses_the_backup_model_when_the_primary_fails() -> None:
    class Response:
        text = "A complete answer."
        candidates: list[object] = []

    class Models:
        def __init__(self) -> None:
            self.models: list[str] = []

        async def generate_content(self, **kwargs: object) -> Response:
            self.models.append(str(kwargs["model"]))
            if len(self.models) == 1:
                raise RuntimeError("primary model unavailable")
            return Response()

    models = Models()
    generator = GeminiGenerator(api_key=None, model="primary-model", max_output_tokens=512)
    generator._client = type("Client", (), {"aio": type("Aio", (), {"models": models})()})()  # type: ignore[assignment]

    assert await generator.answer("Best cafes to work from in Kochi") == "A complete answer."
    assert models.models == ["primary-model", "gemini-flash-lite-latest"]
