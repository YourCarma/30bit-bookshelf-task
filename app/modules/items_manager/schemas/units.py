from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class Kind(Enum):
    BOOK = "book"
    ARTICLE = "article"
    
class Status(Enum):
    PLANNED = "planned"
    READING = "reading"
    DONE = "done"
    
class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"

class Item(BaseModel):
    id: Optional[int] = Field(
        default= None, description="ID задачи", examples=[1, 2]
    )
    user_id: int = Field(
        description="ID задачи", examples=[1, 2]
    )
    kind: Kind = Field(
        description="Вид материала", default=Kind.ARTICLE.value
    )
    title: str = Field(
        description="Название материала"
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