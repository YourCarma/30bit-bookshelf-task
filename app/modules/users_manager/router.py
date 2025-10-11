import sys
from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends
from loguru import logger

from api.dependencies import UOWBookshelf
from modules.users_manager.service import UserService
from modules.users_manager.schemas.responses import UserResponse
from modules.users_manager.schemas.requests import CreatePutUser, PatchUser
from modules.users_manager.schemas.filters import UserFilter, PaginationAndSorting, user_filter_dependency

from utils import validation

sys.path.append(Path(__file__).parent.__str__())  # pylint: disable=C2801

router = APIRouter(prefix="/api/v1",
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/users", 
            tags=["Users"],
            summary="Get users")
async def get_users(uow: UOWBookshelf, filters: UserFilter = Depends(user_filter_dependency), sorting_params: PaginationAndSorting = Depends()) -> list[UserResponse]:
    instance = await UserService().get_users_by_filters(uow, filters, sorting_params)
    return validation(UserResponse, instance)

@router.get("/users/{id}", 
            tags=["Users"],
            summary="Get users by id")
async def get_user_by_id(id: int, uow: UOWBookshelf) -> UserResponse:
    instance = await UserService().get_user_by_id(id, uow)
    return instance

@router.post("/users", 
             tags=["Users"],
             summary="Create User",
             description="""
             """)
async def create_user(user: CreatePutUser, uow: UOWBookshelf) -> UserResponse:
    instance = await UserService().add_user(uow, user)
    return instance

@router.delete("/users/{id}", 
               tags=["Users"],
               summary="Delete user by id",
                description="""
             """)
async def delete_user(id: int, uow: UOWBookshelf) -> JSONResponse:
    await UserService().delete_user(uow, id)
    return JSONResponse("Пользователь успешно удален!", status_code=status.HTTP_200_OK)

@router.patch("/users/{id}", 
               tags=["Users"],
               summary="Delete user by id",
                description="""
             """)
async def patch_user(id: int,  uow: UOWBookshelf, update_data: PatchUser) -> UserResponse:
    result = await UserService().update_user(uow, id, update_data)
    return result
