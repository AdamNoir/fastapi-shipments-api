from datetime import datetime, timedelta
from typing import Optional

from app.api.schemas.shipment import ShipmentRequest, ShipmentResponse, ShipmentStatusUpdate
from app.database.models import ShipmentModel, ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession

class ShipmentService():
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get(self, id: int) -> ShipmentModel | None:
        return await self.session.get(ShipmentModel, id)

    async def add(self, shipment_create: ShipmentRequest) -> int:
        new_shipment = ShipmentModel(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta()
        )
        self.session.add(new_shipment)
        await self.session.commit()
        await self.session.refresh(new_shipment)
        return new_shipment.id

    async def update(self, id: int, shipment_update: ShipmentStatusUpdate) -> ShipmentModel | None:
        shipment = await self.get(id)
        if shipment is None:
            return None
        shipment.sqlmodel_update(shipment_update.model_dump(exclude_unset=True))
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete(self, id: int) -> ShipmentModel | None:
        shipment = await self.get( id)
        if shipment is None:
            return None
        await self.session.delete(shipment)
        await self.session.commit()
        return shipment
