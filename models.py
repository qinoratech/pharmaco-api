from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class CityBase(BaseModel):
    name: str
    department: str

class City(CityBase):
    id: str = Field(alias='_id', default=str(ObjectId()))

    class Config:
        populate_objects = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PharmacyBase(BaseModel):
    name: str
    address: str
    phone: str
    latitude: float
    longitude: float
    city: str  # city_id ou name

class Pharmacy(PharmacyBase):
    id: str = Field(alias='_id', default=str(ObjectId()))
    is_active: bool = True

    class Config:
        populate_objects = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
