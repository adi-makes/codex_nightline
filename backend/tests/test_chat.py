"""Stateless MVP chat contract tests."""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.dependencies.answers import get_grounded_answer_service
from app.main import create_app
from app.models.chat import ChatRequest
from app.services.grounded_answer import GroundedAnswerService


class StubGenerator:
    async def answer(self, query: str) -> str:
        return f"A practical Kochi plan for: {query}"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    app = create_app()
    app.dependency_overrides[get_grounded_answer_service] = lambda: GroundedAnswerService(
        generator=StubGenerator()  # type: ignore[arg-type]
    )
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as api_client:
        yield api_client
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_chat_returns_guarded_llm_answer(client: AsyncClient) -> None:
    response = await client.post("/api/v1/chat", json={"query": "Plan my weekend in Kochi"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["evidence_status"] == "insufficient_evidence"
    assert payload["generation_mode"] == "gemini_general"
    assert payload["answer"] == "A practical Kochi plan for: Plan my weekend in Kochi"
    assert payload["citations"] == []
    assert payload["request_id"] == response.headers["X-Request-ID"]
    assert "session_id" not in payload


@pytest.mark.anyio
async def test_chat_reports_provider_unavailability_without_inventing_facts() -> None:
    service = GroundedAnswerService()

    answer = await service.answer(ChatRequest(query="Things to do tonight"), "test-request-id")

    assert answer.generation_mode == "abstained"
    assert answer.citations == []
    assert "can't generate a reliable answer" in answer.answer
