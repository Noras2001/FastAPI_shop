# app/main.py
from fastapi import FastAPI
from app.routes import products

app = FastAPI()

# Registrar las rutas
app.include_router(products.router)


@app.get("/", summary="Home")
def read_root():
    return {"message": "Welcome to My Shop API!"}
