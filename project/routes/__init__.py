from fastapi import APIRouter

from .projects.views import router as projects_router
from .groups.views import router as groups_router
from .variables.views import router as variables_router

api_router = APIRouter()

api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
api_router.include_router(groups_router, prefix="/groups", tags=["groups"])
api_router.include_router(variables_router, prefix="/variables", tags=["variables"])
