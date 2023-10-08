from fastapi import FastAPI
from controllers.item_controller import router as item_router
from controllers.planet_controller import router as planet_router
from controllers.spacecraft_controller import router as spacecraft_router

app = FastAPI()

app.include_router(item_router)
app.include_router(planet_router)
app.include_router(spacecraft_router)