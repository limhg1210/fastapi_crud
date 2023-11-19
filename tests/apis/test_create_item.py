from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_read_item():
    response = client.get("/item/1")
    assert response.status_code == 404


def test_create_item():
    response = client.post("/item/", json={"name": "test_name", "content": "test_content"})
    assert response.status_code == 200
