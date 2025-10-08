from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from modules.bookshelf_manager.schemas.units import Kind, Status, Priority

class User(BaseModel):
    id: Optional[int] = Field(
        default= None, description="ID пользователя", examples=[1, 2]
    )
    email: EmailStr = Field(
        description="Email пользователя", examples=["Выполнить тестовое задание", "Отправить решение"]
    )
    display_name: bool = Field(
        description="Отображаемое имя пользователя", examples=[True, False]
    )
    
class Item(BaseModel):
    id: Optional[int] = Field(
        default= None, description="ID задачи", examples=[1, 2]
    )
    user_id: Optional[int] = Field(
        description="ID задачи", examples=[1, 2]
    )
    kind: Kind = Field(
        description="Вид материала", default=Kind.ARTICLE.value
    )
    status: Status = Field(
        description="Статус материала", default=Status.PLANNED.value
    )
    priority: Priority = Field(
        description="Приоритет материала", default=Priority.NORMAL.value
    )
    notes: Optional[str] = Field(
        description="Приоритет материала", default=""
    )

class Tag(BaseModel):
    id: Optional[int] = Field(
        default= None, description="ID задачи", examples=[1, 2]
    )
    user_id: Optional[int] = Field(
        description="ID задачи", examples=[1, 2]
    )
    name: str = Field(
        description="уникальное имя тега (в рамках пользователя)"
    )