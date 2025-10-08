from typing import Annotated

from fastapi import Depends

from unitofwork import AbstractUnitOfWork
from modules.bookshelf_manager.uow import BookshelfUnitofWork

UOWBaffler = Annotated[AbstractUnitOfWork, Depends(BookshelfUnitofWork)]
