from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

class Task(BaseModel):
    id: Optional[int] = Field(
        default= None, description="ID задачи", examples=[1, 2]
    )
    title: str = Field(
        description="Заголовок задачи", examples=["Выполнить тестовое задание", "Отправить решение"]
    )
    completed: bool = Field(
        description="Задача выполнена", examples=[True, False]
    )
    
class UpdateTask(BaseModel):
    title: Optional[str] = Field(
        description="Заголовок задачи", examples=["Выполнить тестовое задание", "Отправить решение"]
    )
    completed: Optional[bool] = Field(
        description="Задача выполнена", examples=[True, False]
    )