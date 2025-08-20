from fastapi import APIRouter
from .endpoints import query

api_router = APIRouter()
api_router.include_router(query.router, prefix="/query", tags=["query"])

# Add more routers as needed
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
