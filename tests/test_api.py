"""Тесты проверяют реальные HTTP-ответы API."""

from fastapi.testclient import TestClient

from app.routers.items import Item, fake_db
from main import app

client = TestClient(app)


def setup_function():
    fake_db.clear()
    fake_db[1] = Item(name="Foo", price=50.2)


def test_root_and_docs():
    assert client.get("/").json() == {"message": "Hello, FastAPI!"}
    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 200
    paths = client.get("/openapi.json").json()["paths"]
    assert "/items/{item_id}" in paths and "put" in paths["/items/{item_id}"]


def test_config():
    result = client.get("/info")
    assert result.status_code == 200
    assert result.json()["items_per_page"] == 20


def test_item_found_and_missing():
    assert client.get("/items/1?q=test").json() == {
        "item_id": 1, "item": {"name": "Foo", "price": 50.2, "is_offer": None}, "q": "test",
    }
    response = client.get("/items/42")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
    assert client.get("/items/0").status_code == 422
    assert client.get("/items/1?q=" + "x" * 51).status_code == 422


def test_create_and_update():
    item = {"name": "Телефон", "price": 199.99, "is_offer": False}
    created = client.post("/items/", json=item)
    assert created.status_code == 200 and created.json() == item
    assert client.get("/items/2").json()["item"] == item
    new_item = {"name": "Ноутбук", "price": 600, "is_offer": True}
    changed = client.put("/items/2", json=new_item)
    assert changed.status_code == 200 and changed.json() == new_item
    assert client.get("/items/2").json()["item"]["name"] == "Ноутбук"


def test_duplicate_and_validation():
    assert client.post("/items/", json={"name": " foo ", "price": 12}).status_code == 409
    assert client.post("/items/", json={"name": "Other", "price": 0}).status_code == 422
    assert client.post("/items/", json={"name": "  ", "price": 20}).status_code == 422
    assert client.put("/items/999", json={"name": "Other", "price": 20}).status_code == 404
    assert client.post("/items/", json={"name": "Тест", "price": 20}).status_code == 200
    assert client.put("/items/2", json={"name": "FOO", "price": 20}).status_code == 409
