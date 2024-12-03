from fastapi import FastAPI
from routers import routers

app = FastAPI(title = "User Management System")

app.include_router(routers.router)