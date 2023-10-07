
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from firebase_admin import credentials, firestore
from typing import List
from firebase_init import db

router = APIRouter()

class Item(BaseModel):
    name: str
    description: str
    price: float

@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    try:

        print(item.model_dump())
        _, doc_ref = await db.collection('items').add(item.model_dump())
        print('asdsa', _, doc_ref)
        return {"id": doc_ref.id, **item.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

@router.get("/items/", response_model=List[Item])
async def get_items(skip: int = 0, limit: int = 10):
    try:
        items_collection = db.collection('items')
        items: List[Item] = await items_collection.limit(limit).offset(skip).stream()
        item_list = [Item(**item.to_dict(), id=item.id) for item in items]

        return item_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    try:
        item_ref = db.collection('items').document(item_id)
        item_doc = await item_ref.get()

        if not item_doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")

        item_data = item_doc.to_dict()
        return Item(**item_data, id=item_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, updated_item: Item):
    try:
        item_ref = db.collection('items').document(item_id)
        await item_ref.set(updated_item.dict())

        return {**updated_item.dict(), "id": item_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

@router.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: str):
    try:
        item_ref = db.collection('items').document(item_id)
        item_doc = await item_ref.get()

        if not item_doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")

        await item_ref.delete()
        item_data = item_doc.to_dict()
        return Item(**item_data, id=item_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")