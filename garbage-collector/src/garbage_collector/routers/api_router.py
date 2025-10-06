from fastapi import APIRouter
from src.garbage_collector.routers.garbage_bin import router as bin_router
from src.garbage_collector.routers.location import router as location_router
from src.garbage_collector.routers.truck import router as truck_router
from src.garbage_collector.routers.bin_truck_assignment import router as smart_management

router = APIRouter(prefix="/v1")

router.include_router(bin_router, tags=["Bin"])
router.include_router(location_router, tags=["Location"])
router.include_router(truck_router, tags=["Truck"])
router.include_router(smart_management, tags=["Smart-Management"])  