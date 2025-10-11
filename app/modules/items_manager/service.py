from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from unitofwork import AbstractUnitOfWork
from modules.items_manager.schemas.requests import CreatePutItem, PatchItem
from modules.items_manager.schemas.filters import ItemsFilter, PaginationAndSorting
from modules.items_manager.schemas.responses import ItemResponse
from api.dependencies import UOWBookshelf
from exceptions import ResultNotFound, AlreadyExists


class ItemsService:
    
    async def get_all_tags(self, uow: AbstractUnitOfWork) -> list[ItemResponse]:
        logger.info(
            "\n\tПолучение списка пользователей"
            )
        async with uow:
            try:
                users = await uow.items.get_all()
                logger.success(
                    "\n\tUsers: \n"
                    f"\t {users}"
                    )
            except Exception as e:
                logger.error(f"Ошибка в получении списка материалов: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка в получении списка материалов")
            return users
    
    async def get_items_by_filters(self, uow: AbstractUnitOfWork, filters: ItemsFilter, sorting_params: PaginationAndSorting) -> list[ItemResponse]:
        async with uow:
            try:
                filters = filters.model_dump()
                sort_by = sorting_params.model_dump()
                filtered_users = await uow.items.apply_filters(filters, sort_by)
            except Exception as e:
                logger.error(f"Ошибка в получении списка пользователей: {e}")
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка в получении списка пользователей")
            return filtered_users
                
    async def get_user_by_id(self, id: int,  uow: AbstractUnitOfWork):
        async with uow:
            try:
                user = await uow.items.get_by_id_or_none(id)
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

            
    
    async def add_item(self, uow: AbstractUnitOfWork, item_data: CreatePutItem) -> ItemResponse:
        data = item_data.model_dump()
        logger.info(
            f"\n\tСоздание материала:"
            f"{data}"
        )
        async with uow:
            try:
                user_id = data.get("user_id")
                user = await uow.users.get_by_id_or_none(user_id)
                if not user:
                    raise NoResultFound
                item = await uow.items.create(
                    data
                    )
                await uow.commit()
                logger.success(f"Материал '{data.get("title")}' успешно создан!")
            except NoResultFound as e:
                logger.error("Пользователя не сущетсвует!")
                raise ResultNotFound(detail="Привязка к несуществуещему пользователю!")
            except IntegrityError as e:
                logger.error("Текущий Email уже занят!")
                raise AlreadyExists(detail=f"Email '{data.get("email")}' занят!")
            except Exception as e:
                await uow.rollback()
                logger.error(f"Ошибка при создании пользователя: {str(e)}")
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Ошибка при валидации данных")
            return item
        
    async def delete_item(self, uow: AbstractUnitOfWork, item_id: int):
        async with uow:
            try:
                await uow.items.delete(uow.items.model.id == item_id)
                await uow.commit()
            except NoResultFound as e:
                await uow.rollback()
                logger.error(f"Материала с id '{item_id}' не существует!")
                raise ResultNotFound()
            except Exception as e:
                await uow.rollback()
                logger.error(
                    f"Ошибка при удалении материала: {e}"
                    )
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка при удалении материала")
            
    async def update_item(self, uow: AbstractUnitOfWork, item_id: int, update_data: PatchItem) -> ItemResponse:
        async with uow:
            try:
                update_data = update_data.model_dump(exclude_unset=True)
                user_id = update_data.get("user_id", None)
                if user_id:
                    user = await uow.users.get_by_id_or_none(user_id)
                    if not user:
                        raise NoResultFound
                names = update_data.keys()
                values = update_data.values()
                expression = (uow.items.model.id == item_id)
                result = await uow.items.update_multiple_attrs(names, values, expression)
                await uow.commit()
                return result
            except NoResultFound as e:
                await uow.rollback()
                logger.error(f"Объект не найден!")
                raise ResultNotFound()
            except IntegrityError as e:
                await uow.rollback()
                logger.error(f"Поля для ввода занято")
                raise AlreadyExists(detail="Поле с таким именем уже занято!")
            except Exception as e:
                await uow.rollback()
                logger.error(
                    f"Ошибка при изменении пользователя: {e}"
                    )
                raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ошибка при изменении материала")



