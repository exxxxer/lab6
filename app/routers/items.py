"""Маршруты товаров. После перезапуска данные восстанавливаются из fake_db."""

from fastapi import APIRouter, HTTPException, Path, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/items", tags=["items"])


class Item(BaseModel):
    name: str = Field(..., title="Название", min_length=1, examples=["Телефон"])
    price: float = Field(..., gt=0, title="Цена", examples=[199.99])
    is_offer: bool | None = Field(None, title="Акционный товар")


fake_db: dict[int, Item] = {1: Item(name="Foo", price=50.2)}


def check_unique_name(item: Item, excluding_id: int | None = None):
    """Имена сравниваются без учёта регистра и пробелов по краям."""
    name = item.name.strip().casefold()
    for existing_id, existing in fake_db.items():
        if existing_id != excluding_id and existing.name.strip().casefold() == name:
            raise HTTPException(status_code=409, detail="Item name already exists")



@router.get("/{item_id}", summary="Получить товар по ID", description="Поиск товара в демонстрационном словаре.")
def read_item(
    item_id: int = Path(..., title="ID товара", ge=1),
    q: str | None = Query(None, title="Поисковый запрос", max_length=50),
):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": fake_db[item_id], "q": q}


@router.post("/", response_model=Item, summary="Создать товар", status_code=200)
def create_item(item: Item):
    if not item.name.strip():
        raise HTTPException(status_code=422, detail="Item name must not be blank")
    check_unique_name(item)
    new_id = max(fake_db, default=0) + 1
    fake_db[new_id] = item
    return item


@router.put("/{item_id}", response_model=Item, summary="Изменить товар")
def update_item(
    item: Item,
    item_id: int = Path(..., title="ID товара", ge=1),
):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    if not item.name.strip():
        raise HTTPException(status_code=422, detail="Item name must not be blank")
    check_unique_name(item, excluding_id=item_id)
    fake_db[item_id] = item
    return item
