from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from modules.bookshelf_manager.schemas.units import Kind, Status, Priority

class CreatePutUser(BaseModel):
    email: EmailStr = Field(
        description="Email пользователя", examples=["user@example.ru"]
    )
    display_name: str = Field(
        description="Отображаемое имя пользователя", examples=["Иван Натаныч"]
    )
    
class PatchUser(BaseModel):
    email: Optional[EmailStr] = Field(default=None,
        description="Email пользователя", examples=["user@example.ru"]
    )
    display_name: Optional[str] = Field(
        default=None,
        description="Отображаемое имя пользователя", examples=["Иван Натаныч"]
    )