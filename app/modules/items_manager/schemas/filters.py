from typing import Optional, Union
from datetime import datetime, timedelta
from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from modules.items_manager.schemas.units import Kind, Status, Priority


class ItemSortingParams(str, Enum):
    CREATED_AT = "created_at" 
    UPDATED_AT = "updated_at"
    STATUS = "status"
    TITLE = "title"
    PRIORITY = "priority"
    
class ItemsFilter(BaseModel):
    kind: Optional[Kind] = Field(
        description="Вид материала", default=None
    )
    status: Optional[Status] = Field(
        description="Статус материала", default=None
    )
    priority: Optional[Priority] = Field(
        description="Приоритет материала", default=None
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

def item_filter_dependency(
    kind: Optional[str] = Query(None, description="Вид материала", examples=[Kind.ARTICLE.value]),
    status: Optional[str] = Query(None, description="Отображаемое имя", examples= [Status.PLANNED.value]),
    priority: Optional[str] = Query(None, description="Отображаемое имя", examples=[Priority.NORMAL.value]),
    
    created_from: Optional[datetime] = Query(None, description="Создан с", example=(datetime.now()-timedelta(days=1)).isoformat()),
    created_to: Optional[datetime] = Query(None, description="Создан до", example=datetime.now().isoformat()),
    
    updated_from: Optional[datetime] = Query(None, description="Обновлен с"),
    updated_to: Optional[datetime] = Query(None, description="Обновлен до"),
) -> ItemsFilter:
    return ItemsFilter(
        kind=kind,
        status=status,
        priority=priority,
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
    sort_by: Optional[ItemSortingParams] = Query(
        description="", default=ItemSortingParams.TITLE.value
    )
    desc: Optional[bool] = Query(
        default=False
    )

    
