

from fastapi import APIRouter
from app.api.dependecies import SellerDep, ServiceDep
from app.database.models import ShipmentModel, ShipmentStatus
from app.api.schemas.shipment import ShipmentRequest, ShipmentStatusUpdate, ShipmentResponse, ShipmentCreatedResponse
from fastapi import status, HTTPException

from app.services.shipment import ShipmentService



shipments_router = APIRouter(prefix="/shipments")


### base de datos
@shipments_router.get("/{id}", status_code=200, tags=["shipment_db"], response_model=ShipmentResponse)
async def get_shipment(id: int, service: ServiceDep):
    shipment = await service.get(id)
    
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"Message": "shipment not found"}
        )
    return shipment


### base de datos
@shipments_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ShipmentCreatedResponse)
async def create_shipment(seller: SellerDep, body: ShipmentRequest, service: ServiceDep):
    new_shipment = await service.add(body)

    return {'id': new_shipment}





### Base
@shipments_router.patch("/{id}", response_model=ShipmentResponse)
async def update_shipment(id: int, body: ShipmentStatusUpdate, service: ServiceDep):
    shipment = await service.update(id, body)
    if shipment is None:
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="not found"
                )
    

    return shipment


# bASE
@shipments_router.delete("/{id}")
async def delete_shipment(id: int, service: ServiceDep):
    shipment = await service.delete(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="not found"
        )
    
    return {'message': f"shipment with id {id} was deleted"}


