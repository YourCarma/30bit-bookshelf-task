from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from unitofwork import AbstractUnitOfWork
from modules.bookshelf_manager.schemas.payload import User
from modules.bookshelf_manager.schemas.filters import UserFilter, UserSortingParams
from api.dependencies import UOWBaffler
from exceptions import ResultNotFound, AlreadyExists


class BookshelfService:
    
    async def get_all_users(self, uow: AbstractUnitOfWork):
        logger.info(
            "\n\tПолучение списка пользователей"
            )
        async with uow:
            try:
                users = await uow.users.get_all()
                logger.success(
                    "\n\tUsers: \n"
                    f"\t {users}"
                    )
            except Exception as e:
                logger.error(f"Ошибка в получении списка пользователей: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка в получении списка пользователей")
            return users
    
    async def get_users_by_filters(self, uow: AbstractUnitOfWork, filters: UserFilter, sorting_params: UserSortingParams):
        async with uow:
            try:
                filters = filters.model_dump()
                filtered_users = await uow.users.apply_filters(filters)
            except Exception as e:
                logger.error(f"Ошибка в получении списка пользователей: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка в получении списка пользователей")
            return filtered_users
                
    async def get_user_by_id(self, id: int,  uow: AbstractUnitOfWork):
        async with uow:
            try:
                user = await uow.users.get_by_id_or_none(id)
                if not user:
                    raise NoResultFound
                return user
            except NoResultFound as e:
                await uow.rollback()
                logger.error(f"Пользователя с id '{id}' не существует!")
                raise ResultNotFound()
            except Exception as e:
                await uow.rollback()
                logger.error(f"Ошибка при получении пользователя: {str(e)}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка при валидации данных")

            
    
    async def add_user(self, uow: AbstractUnitOfWork, user_data: User):
        data = user_data.model_dump()
        logger.info(
            f"\n\tСоздание задачи:"
            f"{data}"
        )
        display_name = data.get("display_name")
        async with uow:
            try:
                user = await uow.users.get_by_display_name_or_create(
                    display_name,
                    {
                        **data
                    }
                    )
                await uow.commit()
                logger.success(f"Пользователь '{data.get("display_name")}' успешно создан!")
            except ValueError as e:
                await uow.rollback()
                logger.error(f"Пользователь {data.get("display_name")} уже существует!")
                raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Пользователь '{data.get("display_name")}' уже существует!")
            except IntegrityError as e:
                logger.error("Текущий Email уже занят!")
                raise AlreadyExists(detail=f"Email '{data.get("email")}' занят!")
            except Exception as e:
                await uow.rollback()
                logger.error(f"Ошибка при создании пользователя: {str(e)}")
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Ошибка при валидации данных")
            return user
        
    async def delete_user(self, uow: AbstractUnitOfWork, user_id: int):
        async with uow:
            try:
                await uow.users.delete(uow.users.model.id == user_id)
                await uow.commit()
            except NoResultFound as e:
                await uow.rollback()
                logger.error(f"Пользователя с id '{user_id}' не существует!")
                raise ResultNotFound()
            except Exception as e:
                await uow.rollback()
                logger.error(
                    f"Ошибка при удалении пользоваетля: {e}"
                    )
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка при удалении пользователя")
            
    async def update_task(self, uow: AbstractUnitOfWork):
        pass



