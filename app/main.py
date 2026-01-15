from fastapi import FastAPI
from app.api.routers import main_router

app = FastAPI(title="Excursion API")
app.include_router(main_router)
