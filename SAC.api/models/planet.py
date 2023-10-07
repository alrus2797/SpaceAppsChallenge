from typing import List
from pydantic import BaseModel


class Moon(BaseModel):
    name: str
    diameter: float
    distance_from_planet: float
    surface_features: str

class TouristSite(BaseModel):
    name: str
    description: str
    recommended_duration: str


class PlanetIn(BaseModel):
    name: str
    diameter: float
    mass: float
    atmosphere: str
    average_temperature: float
    geography: str
    moons: List[Moon]
    history_and_exploration: str
    spacecraft_and_infrastructure: str
    travel_information: dict
    tourist_attractions_and_activities: List[TouristSite]
    safety_and_health_information: str
    cultural_and_scientific_significance: str
    images_and_visuals: dict
    local_time_and_time_zone: str
    language_and_communication: str
    local_cuisine_and_dining: str
    transportation_within_the_planet: str
    visa_and_entry_requirements: str
    emergency_contacts_and_services: str
    fun_facts_and_trivia: str

class PlanetOut(PlanetIn):
    id: str

    class Config:
        from_attributes = True