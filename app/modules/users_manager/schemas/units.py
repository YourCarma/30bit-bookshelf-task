from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: Optional[int] = Field(
        default=None, description="ID пользователя", examples=[1, 2]
    )
    email: EmailStr = Field(
        description="Email пользователя", examples=["user@example.ru"]
    )
    display_name: str = Field(
        description="Отображаемое имя пользователя", examples=["Иван Натаныч"]
    )