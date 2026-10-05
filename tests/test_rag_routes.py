from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from main import app
from app.auth.dependencies import get_current_user
from app.routes import rag_routes


@pytest.fixture
def authenticated_client():
    """
    Bypass JWT authentication for route tests.
    Authentication itself is tested separately below.
    """
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=1,
        username="testuser",
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_ask_returns_answer_and_sources(
    authenticated_client,
    monkeypatch,
):
    def fake_ask(question):
        assert question == "What is this document about?"

        return {
            "answer": "This document is about company policies. [Source 1]",
            "sources": [
                {
                    "source": "company.txt",
                    "page": 1,
                    "content": "This document contains company policies.",
                }
            ],
        }

    monkeypatch.setattr(rag_routes, "get_rag_service", lambda: SimpleNamespace(
        ask=fake_ask,
    ))

    response = authenticated_client.post(
        "/ask",
        json={"question": "What is this document about?"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "What is this document about?"
    assert "[Source 1]" in data["answer"]
    assert len(data["sources"]) == 1
    assert data["sources"][0]["source"] == "company.txt"
    assert data["sources"][0]["page"] == 1


def test_ask_requires_authentication():
    app.dependency_overrides.clear()

    with TestClient(app) as client:
        response = client.post(
            "/ask",
            json={"question": "What is this document about?"},
        )

    assert response.status_code == 401


def test_ask_returns_empty_sources(
    authenticated_client,
    monkeypatch,
):
    monkeypatch.setattr(
        rag_routes,
        "get_rag_service",
        lambda: SimpleNamespace(
            ask=lambda question: {
                "answer": "I could not find relevant information.",
                "sources": [],
            },
        ),
    )

    response = authenticated_client.post(
        "/ask",
        json={"question": "Unknown question"},
    )

    assert response.status_code == 200
    assert response.json()["sources"] == []


def test_ask_rejects_empty_question(authenticated_client):
    response = authenticated_client.post(
        "/ask",
        json={"question": "   "},
    )

    assert response.status_code == 422


def test_ask_rejects_question_over_2000_characters(authenticated_client):
    response = authenticated_client.post(
        "/ask",
        json={"question": "a" * 2001},
    )

    assert response.status_code == 422


def test_ask_returns_clear_error_when_no_documents_are_indexed(
    authenticated_client,
    monkeypatch,
):
    def fail_to_load_service():
        raise FileNotFoundError(
            "No indexed documents are available. Upload a document first."
        )

    monkeypatch.setattr(
        rag_routes,
        "get_rag_service",
        fail_to_load_service,
    )

    response = authenticated_client.post(
        "/ask",
        json={"question": "What is this document about?"},
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "No indexed documents are available. Upload a document first."
    )
