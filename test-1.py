import pytest
import hmac
import hashlib
import json
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.config import get_settings


def compute_signature(payload: bytes, secret: str) -> str:
    """Compute GitHub webhook signature for testing."""
    signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"


@pytest.mark.asyncio
async def test_webhook_requires_headers():
    """Test that webhook endpoint requires proper headers."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/webhooks/github",
            json={"action": "test"}
        )
        # Should fail due to missing required headers
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_webhook_with_headers():
    """Test webhook endpoint with proper headers."""
    settings = get_settings()
    payload = {"action": "test"}
    payload_bytes = json.dumps(payload).encode('utf-8')
    signature = compute_signature(payload_bytes, settings.GITHUB_WEBHOOK_SECRET)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/webhooks/github",
            content=payload_bytes,
            headers={
                "Content-Type": "application/json",
                "X-GitHub-Event": "ping",
                "X-Hub-Signature-256": signature,
                "X-GitHub-Delivery": "test-id"
            }
        )
        # Should return 202 for non-PR events (ignored)
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "ignored"


@pytest.mark.asyncio
async def test_webhook_pr_opened():
    """Test webhook endpoint with PR opened event."""
    settings = get_settings()
    payload = {
        "action": "opened",
        "number": 1,
        "pull_request": {
            "number": 1,
            "title": "Test PR",
            "state": "open",
            "head": {"sha": "abc123"},
            "base": {"sha": "def456"},
            "user": {"login": "testuser", "id": 12345}
        },
        "repository": {
            "id": 1,
            "name": "test-repo",
            "full_name": "owner/test-repo",
            "private": False
        },
        "installation": {"id": 12345}
    }
    payload_bytes = json.dumps(payload).encode('utf-8')
    signature = compute_signature(payload_bytes, settings.GITHUB_WEBHOOK_SECRET)
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/webhooks/github",
            content=payload_bytes,
            headers={
                "Content-Type": "application/json",
                "X-GitHub-Event": "pull_request",
                "X-Hub-Signature-256": signature,
                "X-GitHub-Delivery": "test-delivery-id"
            }
        )
        
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "queued"
        assert "review_id" in data
