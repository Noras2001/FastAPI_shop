from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl



# Схема для товара
class ProductCreate(BaseModel):
    name: str
    price: float
    class Config:
        from_attributes = True


class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

    class Config:
        orm_mode = True

# Схема для категории
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Схема для пользователя
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

# Схема для заказа
class OrderCreate(BaseModel):
    user_id: int
    product_ids: List[int]

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_ids: List[int]
    total_price: float

    class Config:
        orm_mode = True




