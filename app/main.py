from fastapi import FastAPI, Request
from .routers import auth_routes, bookings_routes, users_routes, vehicles_routes
from app.logger import logger
from starlette.middleware.base import BaseHTTPMiddleware
from app.middleware import log_middleware

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
logger.info('Starting API...')

app.include_router(auth_routes.router,  prefix="/auth", tags=["auth"])
app.include_router(users_routes.router, prefix="/users", tags=["users"])
app.include_router(vehicles_routes.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(bookings_routes.router, prefix="/bookings", tags=["bookings"])

@app.get("/")
async def root():
    return {"message": "Hello World!!"}
