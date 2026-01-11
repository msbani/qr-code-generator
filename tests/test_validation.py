import json
from app import app

def test_valid_url():
    client = app.test_client()
    response = client.post(
        "/generate",
        data=json.dumps({"url": "https://example.com"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert "qr_image" in response.get_json()

def test_invalid_url():
    client = app.test_client()
    response = client.post(
        "/generate",
        data=json.dumps({"url": "example"}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid URL format"

def test_empty_url():
    client = app.test_client()
    response = client.post(
        "/generate",
        data=json.dumps({"url": ""}),
        content_type="application/json"
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "No URL provided"
