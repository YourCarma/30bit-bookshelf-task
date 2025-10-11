from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from modules.bookshelf_manager.schemas.units import Kind, Status, Priority

class CreateUser(BaseModel):
    email: EmailStr = Field(
        description="Email пользователя", examples=["user@example.ru"]
    )
    display_name: str = Field(
        description="Отображаемое имя пользователя", examples=["Иван Натаныч"]
    )