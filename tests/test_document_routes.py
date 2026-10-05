from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from main import app
from app.auth.dependencies import get_current_user
from app.routes import document_routes


@pytest.fixture
def authenticated_client():
    app.dependency_overrides[get_current_user] = lambda: SimpleNamespace(
        id=7,
        username="testuser",
    )

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_upload_document_success(
    authenticated_client,
    monkeypatch,
):
    saved_data = {}

    def fake_save_document(filename, content, uploaded_by):
        saved_data["filename"] = filename
        saved_data["content"] = content
        saved_data["uploaded_by"] = uploaded_by

        return {
            "id": "document-123",
            "filename": filename,
            "path": "documents/document-123_test.txt",
            "chunks": 2,
            "content_hash": "abc123",
            "uploaded_by": uploaded_by,
        }

    monkeypatch.setattr(
        document_routes.document_service,
        "save_document",
        fake_save_document,
    )

    response = authenticated_client.post(
        "/documents/upload",
        files={
            "file": (
                "test.txt",
                b"This is test document content.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Document uploaded successfully"
    assert data["document"]["id"] == "document-123"
    assert data["document"]["filename"] == "test.txt"
    assert data["document"]["chunks"] == 2

    assert saved_data["filename"] == "test.txt"
    assert saved_data["content"] == b"This is test document content."
    assert saved_data["uploaded_by"] == 7


def test_upload_duplicate_document_returns_conflict(
    authenticated_client,
    monkeypatch,
):
    def fake_save_document(filename, content, uploaded_by):
        raise ValueError("This document already exists")

    monkeypatch.setattr(
        document_routes.document_service,
        "save_document",
        fake_save_document,
    )

    response = authenticated_client.post(
        "/documents/upload",
        files={
            "file": (
                "duplicate.txt",
                b"Duplicate content",
                "text/plain",
            )
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "This document already exists"


def test_upload_requires_authentication():
    app.dependency_overrides.clear()

    with TestClient(app) as client:
        response = client.post(
            "/documents/upload",
            files={
                "file": (
                    "test.txt",
                    b"Test content",
                    "text/plain",
                )
            },
        )

    assert response.status_code == 401


def test_get_documents_returns_current_users_documents(
    authenticated_client,
    monkeypatch,
):
    documents = [
        {
            "id": "document-1",
            "filename": "resume.pdf",
            "path": "documents/resume.pdf",
            "chunks": 3,
            "content_hash": "hash123",
            "uploaded_by": 7,
        }
    ]

    monkeypatch.setattr(
        document_routes.document_service,
        "get_documents",
        lambda uploaded_by: documents,
    )

    response = authenticated_client.get("/documents/")

    assert response.status_code == 200
    assert response.json()["documents"] == documents


def test_delete_document_success(
    authenticated_client,
    monkeypatch,
):
    called = {}

    def fake_delete_document(document_id, uploaded_by):
        called["document_id"] = document_id
        called["uploaded_by"] = uploaded_by
        return True

    monkeypatch.setattr(
        document_routes.document_service,
        "delete_document",
        fake_delete_document,
    )

    response = authenticated_client.delete("/documents/document-123")

    assert response.status_code == 200
    assert response.json()["message"] == "Document deleted successfully"
    assert called["document_id"] == "document-123"
    assert called["uploaded_by"] == 7


def test_delete_missing_document_returns_404(
    authenticated_client,
    monkeypatch,
):
    monkeypatch.setattr(
        document_routes.document_service,
        "delete_document",
        lambda document_id, uploaded_by: None,
    )

    response = authenticated_client.delete("/documents/unknown-document")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"