# app/main.py
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="FastAPI + MongoDB CRUD")

app.include_router(router)
