from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from firebase_admin import credentials, firestore
from typing import List
from firebase_init import db

from models.spacecraft import SpacecraftIn, SpacecraftOut

router = APIRouter()

entity_name = 'spacecrafts'

@router.post(f"/{entity_name}/", response_model=SpacecraftOut)
async def create_item(item: SpacecraftIn):
    try:
        _, doc_ref = await db.collection(entity_name).add(item.model_dump())
        return {"id": doc_ref.id, **item.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

@router.get(f"/{entity_name}/", response_model=List[SpacecraftOut])
async def get_items(skip: int = 0, limit: int = 10):
    try:
        items_collection = db.collection(entity_name)
        items: List[SpacecraftOut] = await items_collection.limit(limit).offset(skip).get()
        item_list = [SpacecraftOut(**item.to_dict(), id=item.id) for item in items]

        return item_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

@router.get(f"/{entity_name}/{{item_id}}", response_model=SpacecraftOut)
async def get_item(item_id: str):
    try:
        item_ref = db.collection(entity_name).document(item_id)
        item_doc = await item_ref.get()

        if not item_doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")

        item_data = item_doc.to_dict()
        return SpacecraftOut(**item_data, id=item_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

@router.put(f"/{entity_name}/{{item_id}}", response_model=SpacecraftOut)
async def update_item(item_id: str, updated_item: SpacecraftIn):
    try:
        item_ref = db.collection(entity_name).document(item_id)
        await item_ref.set(updated_item.model_dump())

        return {**updated_item.model_dump(), "id": item_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

@router.delete(f"/{entity_name}/{{item_id}}", response_model=SpacecraftOut)
async def delete_item(item_id: str):
    try:
        item_ref = db.collection(entity_name).document(item_id)
        item_doc = await item_ref.get()

        if not item_doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")

        await item_ref.delete()
        item_data = item_doc.to_dict()
        return SpacecraftOut(**item_data, id=item_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")
