from fastapi import APIRouter, Depends
from src.garbage_collector.services.user import get_current_user
from src.garbage_collector.routers.garbage_bin import router as bin_router
from src.garbage_collector.routers.location import router as location_router
from src.garbage_collector.routers.truck import router as truck_router
from src.garbage_collector.routers.bin_truck_assignment import router as smart_management
from src.garbage_collector.routers.auth_router import router as auth_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router, tags=["Auth"])
router.include_router(bin_router, tags=["Bin"], dependencies=[Depends(get_current_user)])
router.include_router(location_router, tags=["Location"], dependencies=[Depends(get_current_user)])
router.include_router(truck_router, tags=["Truck"], dependencies=[Depends(get_current_user)])
router.include_router(smart_management, tags=["Smart-Management"], dependencies=[Depends(get_current_user)])  