from fastapi import FastAPI
from controllers.item_controller import router as item_router

# Initialize FastAPI app
app = FastAPI()

# Include the item-related router from the controller
app.include_router(item_router)