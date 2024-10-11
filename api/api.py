from endpoints import user, login, devices, updates
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login",  tags=["login"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
api_router.include_router(updates.router, prefix="/updates", tags=["updates"])