from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

 
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