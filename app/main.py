from fastapi import FastAPI
from .routers import auth, vehicles, bookings, users

app = FastAPI()

app.include_router(auth.router,  prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])

@app.get("/")
async def root():
    return {"message": "Hello World!!"}
