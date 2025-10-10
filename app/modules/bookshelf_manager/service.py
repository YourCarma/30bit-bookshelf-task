from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm.exc import NoResultFound

from unitofwork import AbstractUnitOfWork
from modules.bookshelf_manager.schemas.payload import User
from api.dependencies import UOWBaffler
from exceptions import ResultNotFound


class BookshelfService:
    
    async def get_users(self, uow: AbstractUnitOfWork):
        logger.info(
            "\n\tПолучение списка задач"
            )
        async with uow:
            try:
                tasks = await uow.users.get_all()
                logger.success(
                    "\n\tUsers: \n"
                    f"\t {tasks}"
                    )
            except Exception as e:
                logger.error(f"Ошибка в получении списка пользователей: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка в получении списка пользователей")
            return tasks
        
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
        data = user_data.model_dump(exclude={'id'})
        logger.info(
            f"\n\tСоздание задачи:"
            f"{data}"
        )
        display_name = data.get("display_name")
        async with uow:
            try:
                task = await uow.users.get_by_display_name_or_create(
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
            except Integr
            except Exception as e:
                await uow.rollback()
                logger.error(f"Ошибка при создании пользователя: {str(e)}")
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Ошибка при валидации данных")
            return task
        
    async def delete_task(self, uow: AbstractUnitOfWork, task_id: int):
        async with uow:
            try:
                await uow.tasks.delete(uow.tasks.model.id == task_id)
                await uow.commit()
            except NoResultFound as e:
                await uow.rollback()
                logger.error(f"Задачи с id '{task_id}' не существует!")
                raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Задачи с id '{task_id}' не существует!")
            except Exception as e:
                await uow.rollback()
                logger.error(
                    f"Ошибка при удалении стола: {e}"
                    )
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка при удалении стола")
            
    async def update_task(self, uow: AbstractUnitOfWork):
        pass



