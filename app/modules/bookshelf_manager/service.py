from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm.exc import NoResultFound

from unitofwork import AbstractUnitOfWork
from modules.bookshelf_manager.schemas.payload import Task
from api.dependencies import UOWBaffler


class BookshelfService:
    
    async def get_tasks(self, uow: AbstractUnitOfWork):
        logger.info(
            "\n\tПолучение списка задач"
            )
        async with uow:
            try:
                tasks = await uow.tasks.get_all()
                logger.success(
                    "\n\tЗадачи: \n"
                    f"\t {tasks}"
                    )
            except Exception as e:
                logger.error(f"Ошибка в получении списка задач: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка в получении списка задач")
            return tasks
    
    async def add_table(self, uow: AbstractUnitOfWork, task_data: Task):
        data = task_data.model_dump(exclude={'id'})
        logger.info(
            f"\n\tСоздание задачи:"
            f"{data}"
        )
        title = data.get("title")
        async with uow:
            try:
                task = await uow.tasks.get_by_title_or_create(
                    title,
                    {
                        **data
                    }
                    )
                await uow.commit()
                logger.success(f"Стол '{data.get("title")}' успешно создан!")
            except ValueError as e:
                await uow.rollback()
                logger.error(f"Стол {data.get("title")} уже существует!")
                raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Задача '{data.get("title")}' уже существует!")
            except Exception as e:
                await uow.rollback()
                logger.error(f"Ошибка при создании задачи: {str(e)}")
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



