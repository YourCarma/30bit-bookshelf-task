from database.connection import async_session_maker
from modules import models
from loguru import logger
from sqlalchemy import func
from fastapi import HTTPException, status
from sqlalchemy.exc import OperationalError

from modules.models import *
from database.repository import DatabaseRepository
from unitofwork import AbstractUnitOfWork
from exceptions import ServiceUnavailable
from settings import settings


class BookshelfUnitofWork(AbstractUnitOfWork):

    def __init__(self):
        super().__init__()
        self.session = None

    async def __aenter__(self):
        try:
            self.session = self.factory()
            self.users = DatabaseRepository(models.Users, self.session)
            self.items = DatabaseRepository(models.Items, self.session)
            self.tags = DatabaseRepository(models.Tags, self.session)
            
        except OperationalError as e:
            logger.error(
                "Ошибка подключения к СУБД!"
                f"Проверьте подключение по адресу: {settings.DB_URL}"
                )
            raise ServiceUnavailable(
                "База данных"
            )
        
    async def __aexit__(self, *args):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()