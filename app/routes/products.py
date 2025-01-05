# app/routes/products.py
from pydantic import BaseModel, Field, HttpUrl
from app.database import SessionLocal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Product
from app.schemas import ProductCreate
from app.database import get_db

router = APIRouter(prefix="/products", tags=["Products"])




# Схемы для валидации входящих данных
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Название товара")
    description: str = Field(None, description="Описание товара")
    price: float = Field(..., gt=0, description="Цена товара")
    image_url: HttpUrl = Field(..., description="Ссылка на изображение")

class ProductUpdate(BaseModel):
    name: str = Field(None, min_length=1, description="Название товара")
    description: str = Field(None, description="Описание товара")
    price: float = Field(None, gt=0, description="Цена товара")
    image_url: HttpUrl = Field(None, description="Ссылка на изображение")

# Депенденсы для подключения к сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Маршрут для добавления нового товара
@router.post("/", response_model=ProductCreate, summary="Добавить новый товар")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Convertir HttpUrl a str
    product_data = product.dict()
    product_data["image_url"] = str(product.image_url)

    # Crear el producto en la base de datos
    db_product = Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# Маршрут для редактирования товара
@router.put("/{product_id}", summary="Редактировать товар")
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

# Маршрут для удаления товара
@router.delete("/{product_id}", summary="Удалить товар")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}