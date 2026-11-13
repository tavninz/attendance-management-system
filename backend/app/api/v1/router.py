from fastapi import APIRouter 

from app.api.v1.enpoints.users import auth
from app.api.v1.enpoints.health import health
from app.api.v1.enpoints.leave import leaveRequest

api_router = APIRouter()

# Include individual endpoint routers
api_router.include_router(auth.router)
api_router.include_router(health.router)
api_router.include_router(leaveRequest.router)