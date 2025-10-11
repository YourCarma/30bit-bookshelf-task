from typing import Optional, Union
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from modules.items_manager.schemas.units import Item
from modules.tags_manager.schemas.units import Tag
from modules.users_manager.schemas.units import User
from modules.items_manager.schemas.units import Kind, Status, Priority

class ItemResponse(BaseModel):
    id: int = Field(
        default= None, description="ID задачи", examples=[1, 2]
    )
    user_id: int = Field(
        description="ID задачи", examples=[1, 2]
    )
    title: str = Field(
        description="Название материала"
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
    
    user: User = Field(
        description="Инфомрация о пользователе"
    )
    tags: list[Tag] = Field(
        description="Прикрепленные к материалу теги"
    )
    
    notes: str = Field(
        description="Приоритет материала", default=""
    )
    created_at: datetime = Field(
        description="Дата и время создания", examples=[datetime.now()]
    )
    updated_at: datetime = Field(
        description="Дата и время обновления", examples=[datetime.now()]
    )
    
    model_config = ConfigDict(from_attributes=True)