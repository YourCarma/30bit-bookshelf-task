from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from modules.items_manager.schemas.units import Kind, Status, Priority

class CreatePutItem(BaseModel):
    user_id: Optional[int] = Field(
        description="ID пользователя", examples=[1, 2]
    )
    kind: Kind = Field(
        description="Вид материала", default=Kind.ARTICLE.value
    )
    status: Status = Field(
        description="Статус материала", default=Status.PLANNED.value
    )
    title: str = Field(
        description="Название материала"
    )
    priority: Priority = Field(
        description="Приоритет материала", default=Priority.NORMAL.value
    )
    notes: Optional[str] = Field(
        description="Приоритет материала", default=""
    )
    
class PatchItem(BaseModel):
    user_id: Optional[int] = Field(
        description="ID пользователя", examples=[1, 2]
    )
    kind: Optional[Kind] = Field(
        description="Вид материала", default=None
    )
    status: Optional[Status] = Field(
        description="Статус материала", default=None
    )
    priority: Optional[Priority] = Field(
        description="Приоритет материала", default=None
    )
    notes: Optional[str] = Field(
        description="Приоритет материала", default=None
    )