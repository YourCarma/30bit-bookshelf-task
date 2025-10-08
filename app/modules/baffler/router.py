import sys
from pathlib import Path

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status

from api.dependencies import UOWBaffler
from modules.baffler.service import BufflerService
from modules.baffler.schemas.payload import Task
from utils import validation

sys.path.append(Path(__file__).parent.__str__())  # pylint: disable=C2801

router = APIRouter(prefix="/api",
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/tasks", 
            tags=["Задачи"],
            summary="Получение всех задач")
async def get_tables(uow: UOWBaffler) -> list[Task]:
    instance = await BufflerService().get_tasks(uow)
    return instance


@router.post("/tasks", 
             tags=["Задачи"],
             summary="Создание задачи",
             description="""
## Добавление задачи.
### Входные данные:
*  **title** `str` - Желаемое имя (Уникальное) задачи (Задача №1, Задача №2...)
*  **complete** `bool` - Задача выполнена
### Выходные данные:
* Инстанс созданной задачи
             """)
async def create_table(table: Task, uow: UOWBaffler) -> Task:
    instance = await BufflerService().add_table(uow, table)
    return JSONResponse(validation(Task, instance),
                        status_code=status.HTTP_201_CREATED)


@router.delete("/tasks/{id}", 
               tags=["Задачи"],
               summary="Удаление задачи по id",
                description="""
## Удаление задачи.
### Входные данные:
*  **id** `int` - id удаляемой задачи
### Выходные данные:
* **200 OK** - задача успешно удалена
* **400 BAD_REQUEST** - заданной задачи не существует
             """)
async def delete_table(id: int, uow: UOWBaffler) -> JSONResponse:
    await BufflerService().delete_task(uow, id)
    return JSONResponse("Задача успешно удалена!", status_code=status.HTTP_200_OK)
