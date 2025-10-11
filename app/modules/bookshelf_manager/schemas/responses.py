from typing import Optional, Union
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from modules.bookshelf_manager.schemas.payload import Tag, Item, User


class UserResponse(BaseModel):
    id: Optional[int] = Field(
        default=None, description="ID пользователя", examples=[1, 2]
    )
    email: EmailStr = Field(
        description="Email пользователя", examples=["user@example.ru"]
    )
    display_name: str = Field(
        description="Отображаемое имя пользователя", examples=["Иван Натаныч"]
    )
    items: list[Item] = Field(
        description="Материалы пользователя"
    )
    tags: list[Tag] = Field(
        description="Теги пользователя"
    )
    created_at: datetime = Field(
        description="Дата и время создания", examples=[datetime.now()]
    )
    updated_at: datetime = Field(
        description="Дата и время обновления", examples=[datetime.now()]
    )
    
    model_config = ConfigDict(from_attributes=True)