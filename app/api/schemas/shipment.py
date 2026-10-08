from pydantic import BaseModel, Field
from random import randint
from app.database.models import ShipmentStatus
from datetime import datetime

def get_random_destination():
    return randint(1100012, 1231512)





class BaseShipment(BaseModel):
    content: str = Field(description="The type of content of shimpent", max_length=30)
    weight: float = Field(le=25, ge=1)
    destination: int | None = Field(default_factory=get_random_destination)


class ShipmentResponse(BaseShipment):
    status: ShipmentStatus
    estimated_delivery: datetime


class ShipmentRequest(BaseShipment):
    pass

class ShipmentCreatedResponse(BaseModel):
    id: int

class ShipmentStatusUpdate(BaseModel):
    status: ShipmentStatus
    estimated_delivery: datetime | None = Field(default=None)
