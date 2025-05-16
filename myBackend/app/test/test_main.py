import pytest
from fastapi.testclient import TestClient
from app.main import app

# establish client
client = TestClient(app)


# test api is running
def test_health_checker():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running ✅"}