from typing import Generic, TypeVar, Any, Optional
from datetime import datetime

import asyncpg
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy import (
    select,
    update,
    BinaryExpression,
)
from sqlalchemy.dialects.postgresql import array

from database.base import Base

Model = TypeVar("Model", bound=Base)


class DatabaseRepository(Generic[Model]):
    """Repository for performing database queries."""

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def create(
        self,
        data: dict,
    ) -> Optional[Model]:
        instance = self.model(**data)
        self.session.add(instance)
        try:
            await self.session.flush()
            await self.session.refresh(instance)
            return instance
        except asyncpg.exceptions.UniqueViolationError as error:
            logger.warning(
                f"Non unique-values, proceed next, details: \n{error}")
            await self.session.rollback()
        except IntegrityError as e:
            logger.warning(e)
            raise e

    async def apply_filters(self, filters: dict, sort_params: dict):
        logger.debug("Применение фильторв...")
        limit = sort_params.get("limit")
        offset = sort_params.get("offset")
        query = select(self.model)
        for field, value in filters.items():
            logger.debug(f"Элемент фильтрации: {field}:{value}")
            if value is None:
                logger.warning("Элемент не подлежит фильтрации!")
                continue
            match field:
                case "created_from":
                    query = query.filter(self.model.created_at >= value)
                    continue
                case "created_to":
                    query = query.filter(self.model.created_at <= value)
                    continue
                case "updated_from":
                    query = query.filter(self.model.updated_at >= value)
                    continue
                case "updated_to":
                    query = query.filter(self.model.updated_at <= value)
                    continue
            column = getattr(self.model, field, None)
            logger.debug(column)
            if column is not None:
                if isinstance(value, str):
                    query = query.filter(column.ilike(f"%{value}%"))
                else:
                    query = query.filter(column == value)
        query = self.sort_items(query, sort_params)
        query = query.limit(limit).offset(limit*offset)
        filtered_users = (await self.session.scalars(query)).all()
        return filtered_users
    
    def sort_items(self, query, sort_params: dict):
        sort_by = sort_params.get("sort_by").value
        desc = sort_params.get("desc")
        logger.debug(sort_by)
        if hasattr(self.model, sort_by):
            column = getattr(self.model, sort_by)
            if desc:
                query = query.order_by(column.desc())
                logger.debug(query)
            else:
                query = query.order_by(column.asc())
        else:
            logger.warning(f"Поле {sort_by} не найдено в модели, используется сортировка по умолчанию (id)")
            query = query.order_by(self.model.id.asc())
        return query
            
    async def filter(
        self,
        *expressions: BinaryExpression,
    ) -> list[Model]:
        query = select(self.model)
        if expressions:
            query = query.where(*expressions)
        return list(await self.session.scalars(query))

    
    async def get_by_filter_or_create(
        self,
        values: dict,
        *filtering_expression: BinaryExpression,
    ) -> Model:
        instance = self.model(**values)
        object_ = (await self.session.scalars(
            select(self.model).where(*filtering_expression))).one_or_none()
        if object_ is None:
            self.session.add(instance)
            await self.session.commit()
            object_ = (await self.session.scalars(
                select(self.model).filter_by(**values))).one()
        return object_

    async def get_by_id_or_none(
        self,
        id_: int,
    ) -> Optional[Model]:
        query = select(self.model).where(self.model.id == id_)
        object_ = (await self.session.scalars(query)).one_or_none()
        return object_

    async def get_by_display_name_or_create(self, display_name: str, values: dict) -> Model:
        instance = self.model(**values)
        objects = await self.filter(self.model.display_name == display_name)
        if not objects:
            self.session.add(instance)
            objects = await self.filter(self.model.display_name == display_name)
        else:
            logger.exception("Объект уже существует...Пропуск")
            raise ValueError()
        return objects[0]

    async def get_or_create(self, values: dict) -> Model:
        abstract_id = values.get("id")
        if isinstance(abstract_id, int):
            objects = await self.filter(self.model.id == abstract_id)
        else:
            objects = (await self.session.scalars(
                select(self.model).filter_by(**values))).all()
        if len(objects) == 0:
            instance = self.model(**values)
            self.session.add(instance)
            await self.session.commit()
            objects = (await self.session.scalars(
                select(self.model).filter_by(**values))).all()
        return objects[0]

    async def get_or_none(self, values: dict) -> Optional[Model]:
        objects = (await self.session.scalars(
            select(self.model).filter_by(**values))).all()
        if len(objects) == 0:
            return None
        return objects[0]

    async def get_or_create_list(self, values: list) -> list[Model]:
        return [await self.get_or_create(value) for value in values]

    async def get_by_id_or_none_list(self, values: list) -> list[Model]:
        return [
            await self.get_by_id_or_none(value.get("id")) for value in values
        ]

    async def get_all(self) -> list[Model]:
        return (await self.session.scalars(select(self.model))).all()

    async def update_multiple_attrs(self, names: list[str], values: list[Any],
                                    *expressions: BinaryExpression) -> Model:
        scalar_object = (await self.session.scalars(
            select(self.model).where(*expressions))).one()
        updated_at = datetime.now()
        setattr(scalar_object, 'updated_at', updated_at)
        await self.update_multiple_attrs_to_object(names=names,
                                                   values=values,
                                                   scalar_object=scalar_object)
        
        return scalar_object

    async def update_multiple_attrs_to_object(self, names: list[str],
                                              values: list[Any],
                                              scalar_object: Model) -> Model:
        _ = [
            setattr(scalar_object, name, value)
            for name, value in zip(names, values)
        ]
        await self.session.flush()
        await self.session.refresh(scalar_object)
        return scalar_object

    async def update_list(self, name: str, value: list, *expressions:
                          BinaryExpression) -> Model:
        """
        Операция изменения атрибутов name объектов с конструкцией

        class Object(Base)
            name: Mapped(List[str])

        Args:
            name: название изменяемого аттрибута
            value: список значений[any]
            *expressions: условие нахождения единственного экземпляра модели self.model

        Output:
            ScalarResult это строка из таблицы self.model, представляет собой имененный объект
        """
        instance = (await self.session.scalars(
            select(self.model).where(*expressions))).one()
        setattr(instance, name, array(value))
        await self.session.flush()
        return instance

    async def update(self, name: str, value: Any, *expressions:
                     BinaryExpression) -> Model:
        result = (await
                  self.session.scalars(select(self.model).where(*expressions)
                                       )).one()
        setattr(
            result, name, value
        )  # нельзя так просто взять и изменить аттрибут (instance это не словарь, это scalar object)
        await self.session.flush()
        return result

    async def delete_instance_list(self, instances) -> None:
        for instance in instances:
            await self.delete_instance(instance)
        return

    async def delete_instance(self, instance) -> None:
        await self.session.delete(instance)
        await self.session.flush()
        return

    async def delete(self, *expressions: BinaryExpression) -> None:
        try:
            result = (await self.session.scalars(
                select(self.model).where(*expressions))).one()
            await self.delete_instance(result)
        except NoResultFound as e:
            logger.error("Объекта на удаление не существует!")
            raise NoResultFound
        return
