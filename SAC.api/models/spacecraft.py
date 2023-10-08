from pydantic import BaseModel

class SpacecraftType(BaseModel):
    name: str

class SpacecraftIn(BaseModel):
    name: str
    agency: str
    description: str
    spacecraft_type: SpacecraftType
    orbit: str
    status: str
    velocity_kmps: float

class SpacecraftOut(SpacecraftIn):
    id: str

    class Config:
        from_attributes = True