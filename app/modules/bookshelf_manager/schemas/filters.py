from typing import Optional, Union
from datetime import datetime, timedelta
from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from modules.bookshelf_manager.schemas.payload import Tag, Item, User

class UserSortingParams(str, Enum):
    CREATED_AT = "created_at" 
    UPDATED_AT = "updated_at"
    EMAIL = "email"
    DISPLAY_NAME = "display_name"
    
class UserFilter(BaseModel):
    email: Optional[str] = Query(
        default=None,
        description="Email пользователя", 
        examples=["user@example.ru"]
    )
    display_name: Optional[str] = Query(
        default=None,
        description="Отображаемое имя пользователя", 
        examples=["Иван Натаныч"]
    )
    created_from: Optional[datetime] = Query(
        default=None,
        description="Дата и время создания", 
        examples=[datetime.now()]
    )
    created_to: Optional[datetime] = Query(
        default=None,
        description="Дата и время создания", 
        examples=[datetime.now()]
    )
    updated_from: Optional[datetime] = Query(
        default=None,
        description="Дата и время обновления", 
        examples=[datetime.now()]
    )
    updated_to: Optional[datetime] = Query(
        default=None,
        description="Дата и время обновления", 
        examples=[datetime.now()]
    )

def user_filter_dependency(
    email: Optional[str] = Query(None, description="Email пользователя"),
    display_name: Optional[str] = Query(None, description="Отображаемое имя"),
    created_from: Optional[datetime] = Query(None, description="Создан с", example=(datetime.now()-timedelta(days=1)).isoformat()),
    created_to: Optional[datetime] = Query(None, description="Создан до", example=datetime.now().isoformat()),
    updated_from: Optional[datetime] = Query(None, description="Обновлен с"),
    updated_to: Optional[datetime] = Query(None, description="Обновлен до"),
) -> UserFilter:
    return UserFilter(
        email=email,
        display_name=display_name,
        created_from=created_from,
        created_to=created_to,
        updated_from=updated_from,
        updated_to=updated_to
    )
    
class PaginationAndSorting(BaseModel):
    limit: Optional[int] = Query(
        description="По сколько показывать записей", ge=1, le=100, default=20
    )
    offset: Optional[int] = Query(
        description="Смещение контекстного окна", ge=0, default=0
    )
    sort_by: Optional[UserSortingParams] = Query(
        description="", default=UserSortingParams.DISPLAY_NAME.value
    )
    desc: Optional[bool] = Query(
        default=False
    )

    
