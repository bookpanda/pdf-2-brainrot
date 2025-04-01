from app.models.item import Item
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_items():
    return {"message": "List of items"}


@router.post("/")
def create_item(item: Item):
    return {"message": f"Item {item.name} created!"}
