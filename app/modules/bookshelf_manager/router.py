import sys
from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends
from loguru import logger

from api.dependencies import UOWBaffler
from modules.bookshelf_manager.service import BookshelfService
from modules.bookshelf_manager.schemas.payload import User
from modules.bookshelf_manager.schemas.responses import UserResponse
from modules.bookshelf_manager.schemas.requests import CreatePutUser, PatchUser
from modules.bookshelf_manager.schemas.filters import UserFilter, PaginationAndSorting, user_filter_dependency

from utils import validation

sys.path.append(Path(__file__).parent.__str__())  # pylint: disable=C2801

router = APIRouter(prefix="/api/v1",
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/users", 
            tags=["Users"],
            summary="Get users")
async def get_users(uow: UOWBaffler, filters: UserFilter = Depends(user_filter_dependency), sorting_params: PaginationAndSorting = Depends()) -> list[UserResponse]:
    instance = await BookshelfService().get_users_by_filters(uow, filters, sorting_params)
    return validation(UserResponse, instance)

@router.get("/users/{id}", 
            tags=["Users"],
            summary="Get users by id")
async def get_user_by_id(id: int, uow: UOWBaffler) -> UserResponse:
    instance = await BookshelfService().get_user_by_id(id, uow)
    return instance

@router.post("/users", 
             tags=["Users"],
             summary="Create User",
             description="""
             """)
async def create_user(user: CreatePutUser, uow: UOWBaffler) -> UserResponse:
    instance = await BookshelfService().add_user(uow, user)
    return instance

@router.delete("/users/{id}", 
               tags=["Users"],
               summary="Delete user by id",
                description="""
             """)
async def delete_user(id: int, uow: UOWBaffler) -> JSONResponse:
    await BookshelfService().delete_user(uow, id)
    return JSONResponse("Пользователь успешно удален!", status_code=status.HTTP_200_OK)

@router.patch("/users/{id}", 
               tags=["Users"],
               summary="Delete user by id",
                description="""
             """)
async def patch_user(id: int,  uow: UOWBaffler, update_data: PatchUser) -> UserResponse:
    result = await BookshelfService().update_user(uow, id, update_data)
    return result
