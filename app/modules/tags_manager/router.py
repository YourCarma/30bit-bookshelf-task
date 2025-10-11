import sys
from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends
from loguru import logger

from api.dependencies import UOWBookshelf
from modules.tags_manager.service import TagsService
from modules.tags_manager.schemas.responses import UserResponse
from modules.tags_manager.schemas.requests import CreatePutUser, PatchUser
from modules.tags_manager.schemas.filters import UserFilter, PaginationAndSorting, user_filter_dependency

from utils import validation

sys.path.append(Path(__file__).parent.__str__())  # pylint: disable=C2801

router = APIRouter(prefix="/api/v1",
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/tags", 
            tags=["Tags"],
            summary="Get users")
async def get_users(uow: UOWBookshelf, filters: UserFilter = Depends(user_filter_dependency), sorting_params: PaginationAndSorting = Depends()) -> list[UserResponse]:
    instance = await TagsService().get_users_by_filters(uow, filters, sorting_params)
    return validation(UserResponse, instance)

@router.get("/tags/{id}", 
            tags=["Tags"],
            summary="Get users by id")
async def get_user_by_id(id: int, uow: UOWBookshelf) -> UserResponse:
    instance = await TagsService().get_user_by_id(id, uow)
    return instance

@router.post("/tags", 
             tags=["Tags"],
             summary="Create User",
             description="""
             """)
async def create_user(user: CreatePutUser, uow: UOWBookshelf) -> UserResponse:
    instance = await TagsService().add_user(uow, user)
    return instance

@router.delete("/tags/{id}", 
               tags=["Tags"],
               summary="Delete user by id",
                description="""
             """)
async def delete_user(id: int, uow: UOWBookshelf) -> JSONResponse:
    await TagsService().delete_user(uow, id)
    return JSONResponse("Пользователь успешно удален!", status_code=status.HTTP_200_OK)

@router.patch("/tags/{id}", 
               tags=["Tags"],
               summary="Delete user by id",
                description="""
             """)
async def patch_user(id: int,  uow: UOWBookshelf, update_data: PatchUser) -> UserResponse:
    result = await TagsService().update_user(uow, id, update_data)
    return result
