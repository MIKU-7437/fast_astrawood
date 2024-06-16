from fastapi import FastAPI
from api.v1.endpoints import users, store  # Import the store endpoints
from db.session import database

app = FastAPI()

app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(store.router, prefix="/api/v1", tags=["store"])  # Include the store router

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
