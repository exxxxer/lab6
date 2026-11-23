"""Наглядная демонстрация FastAPI через реальный HTTP (стандартная библиотека)."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "http://127.0.0.1:8000"


def check(method, path, data=None):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data is not None else None
    request = Request(
        BASE + path,
        data=body,
        headers={"Content-Type": "application/json"} if data is not None else {},
        method=method,
    )
    try:
        with urlopen(request, timeout=5) as response:
            code = response.status
            content = response.read().decode("utf-8")
    except HTTPError as error:
        code = error.code
        content = error.read().decode("utf-8")
    print(f"\n{method} {path} — HTTP {code}")
    try:
        print(json.dumps(json.loads(content), indent=2, ensure_ascii=False))
    except ValueError:
        print(content[:200])


if __name__ == "__main__":
    try:
        check("GET", "/")
        check("GET", "/items/1?q=test")
        check("GET", "/info")
        check("GET", "/items/42")
        check("POST", "/items/", {"name": "Телефон", "price": 199.99, "is_offer": False})
        check("POST", "/items/", {"name": "телефон", "price": 100})
        check("POST", "/items/", {"name": "Ошибка", "price": -5})
        # Чтобы показать PUT, сначала перезапустите сервер: у нового товара ID 2.
        check("PUT", "/items/2", {"name": "Ноутбук", "price": 650, "is_offer": True})
        check("GET", "/items/2")
    except URLError:
        print("Сервер не запущен. Сначала выполните: uv run uvicorn main:app --reload")
