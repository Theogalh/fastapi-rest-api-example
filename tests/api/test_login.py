from fastapi.testclient import TestClient
from app.api.app import app

client = TestClient(app)


def test_read_users_without_login():
    response = client.get('/user/')
    assert response.status_code == 401
