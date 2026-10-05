import os
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from main import app
from app.auth.dependencies import get_current_user


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="Integration tests require RUN_INTEGRATION_TESTS=1",
)


@pytest.fixture
def authenticated_client():
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=999,
        username="integration-user",
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_upload_then_ask(authenticated_client):
    document_content = b"""
    RAG stands for Retrieval Augmented Generation.
    It retrieves relevant document chunks before generating an answer.
    """

    upload_response = authenticated_client.post(
        "/documents/upload",
        files={
            "file": (
                "integration_test.txt",
                document_content,
                "text/plain",
            )
        },
    )

    assert upload_response.status_code == 200

    uploaded_document = upload_response.json()["document"]
    document_id = uploaded_document["id"]

    try:
        ask_response = authenticated_client.post(
            "/ask",
            json={
                "question": "What does RAG stand for?"
            },
        )

        assert ask_response.status_code == 200

        result = ask_response.json()

        assert result["question"] == "What does RAG stand for?"
        assert result["answer"]
        assert len(result["sources"]) > 0

    finally:
        authenticated_client.delete(
            f"/documents/{document_id}"
        )