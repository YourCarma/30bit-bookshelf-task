from typing import Annotated

from fastapi import Depends

from unitofwork import AbstractUnitOfWork
from modules.uow import BookshelfUnitofWork

UOWBookshelf = Annotated[AbstractUnitOfWork, Depends(BookshelfUnitofWork)]
