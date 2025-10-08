from typing import Annotated

from fastapi import Depends

from unitofwork import AbstractUnitOfWork
from modules.baffler.uow import BafflerUnitofWork

UOWBaffler = Annotated[AbstractUnitOfWork, Depends(BafflerUnitofWork)]
