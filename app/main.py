from fastapi import FastAPI
from .routers import auth_routes, bookings_routes, users_routes, vehicles_routes

app = FastAPI()

app.include_router(auth_routes.router,  prefix="/auth", tags=["auth"])
app.include_router(users_routes.router, prefix="/users", tags=["users"])
app.include_router(vehicles_routes.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(bookings_routes.router, prefix="/bookings", tags=["bookings"])

@app.get("/")
async def root():
    return {"message": "Hello World!!"}
