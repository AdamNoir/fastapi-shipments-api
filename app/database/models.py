from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from enum import Enum

class ShipmentStatus(str, Enum):
    placed = "placed" 
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"

class ShipmentModel(SQLModel, table=True):
    __tablename__ = "shipments"
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    weight: float = Field(le=25)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime


class Seller(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str
