# item_controller.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from firebase_admin import credentials, firestore
from typing import List
from firebase_init import db

# Create an APIRouter for the item-related endpoints
router = APIRouter()

# Define a Pydantic model for the item
class Item(BaseModel):
    name: str
    description: str
    price: float

# Create an endpoint to save an item to Firestore
@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    try:
        # Create a new document in the 'items' collection with the provided data

        print(item.model_dump())
        _, doc_ref = await db.collection('items').add(item.model_dump())
        print('asdsa', _, doc_ref)
        # Return the ID of the newly created document as part of the response
        return {"id": doc_ref.id, **item.model_dump()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

# Create an endpoint to get a list of all items from Firestore
@router.get("/items/", response_model=List[Item])
async def get_items(skip: int = 0, limit: int = 10):
    try:
        # Query Firestore to retrieve items with pagination
        items_collection = db.collection('items')
        items: List[Item] = await items_collection.limit(limit).offset(skip).stream()
        # Convert Firestore documents to a list of Item objects
        item_list = [Item(**item.to_dict(), id=item.id) for item in items]

        return item_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

# Create an endpoint to get a single item by ID from Firestore
@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    try:
        # Retrieve the item document by its ID from the 'items' collection
        item_ref = db.collection('items').document(item_id)
        item_doc = await item_ref.get()

        if not item_doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")

        # Convert Firestore document to an Item object
        item_data = item_doc.to_dict()
        return Item(**item_data, id=item_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

# Create an endpoint to update an item by ID in Firestore
@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, updated_item: Item):
    try:
        # Update the item document with the provided data
        item_ref = db.collection('items').document(item_id)
        await item_ref.set(updated_item.dict())

        # Return the updated item data
        return {**updated_item.dict(), "id": item_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")

# Create an endpoint to delete an item by ID from Firestore
@router.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: str):
    try:
        # Delete the item document by its ID from the 'items' collection
        item_ref = db.collection('items').document(item_id)
        item_doc = await item_ref.get()

        if not item_doc.exists:
            raise HTTPException(status_code=404, detail="Item not found")

        # Delete the item and return its data
        await item_ref.delete()
        item_data = item_doc.to_dict()
        return Item(**item_data, id=item_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Firestore error: {str(e)}")