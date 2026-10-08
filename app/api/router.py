from fastapi import APIRouter
from app.api.routers.shipment import shipments_router
from app.api.routers.sellers import sellers_router


router = APIRouter()

router.include_router(shipments_router)
router.include_router(sellers_router)