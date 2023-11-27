from pydantic import BaseModel
from datetime import date


class UsersController(BaseModel):
    name: str
    email: str
    cep: str


class CategoryController(BaseModel):
    name: str


class ProductController(BaseModel):
    category_id: int
    name: str
    price: float
    stock: int
    fabricated_at: date


class ProductResp(BaseModel):
    id: int
    category: str
    name: str
    price: float
    stock: int
    fabricated_at: date