import sys
from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends
from loguru import logger

from api.dependencies import UOWBookshelf
from modules.items_manager.service import ItemsService
from modules.items_manager.schemas.responses import ItemResponse
from modules.items_manager.schemas.requests import CreatePutItem, PatchItem
from modules.items_manager.schemas.filters import ItemsFilter, PaginationAndSorting, item_filter_dependency

from utils import validation

sys.path.append(Path(__file__).parent.__str__())  # pylint: disable=C2801

router = APIRouter(prefix="/api/v1",
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/items", 
            tags=["Items"],
            summary="Get items")
async def get_items(uow: UOWBookshelf, filters: ItemsFilter = Depends(item_filter_dependency), sorting_params: PaginationAndSorting = Depends()) -> list[ItemResponse]:
    instance = await ItemsService().get_items_by_filters(uow, filters, sorting_params)
    return validation(ItemResponse, instance)

@router.get("/items/{id}", 
            tags=["Items"],
            summary="Get items by id")
async def get_user_by_id(id: int, uow: UOWBookshelf) -> ItemResponse:
    instance = await ItemsService().get_user_by_id(id, uow)
    return instance

@router.post("/items", 
             tags=["Items"],
             summary="Create item",
             description="""
             """)
async def create_item(item: CreatePutItem, uow: UOWBookshelf) -> ItemResponse:
    instance = await ItemsService().add_item(uow, item)
    return instance

@router.delete("/items/{id}", 
               tags=["Items"],
               summary="Delete item by id",
                description="""
             """)
async def delete_user(id: int, uow: UOWBookshelf) -> JSONResponse:
    await ItemsService().delete_item(uow, id)
    return JSONResponse("Материал успешно удален!", status_code=status.HTTP_200_OK)

@router.patch("/items/{id}", 
               tags=["Items"],
               summary="Patch item by id",
                description="""
             """)
async def patch_user(id: int,  uow: UOWBookshelf, update_data: PatchItem) -> ItemResponse:
    result = await ItemsService().update_item(uow, id, update_data)
    return result
