from fastapi import HTTPException, status
from loguru import logger

from settings import settings


class ServiceExceptions(HTTPException):

    def __init__(self, status_code, detail):
        logger.error(detail)
        super().__init__(status_code, detail)


class ServiceUnavailable(ServiceExceptions):

    def __init__(
        self,
        service_name: str = "Неизвестный сервис",
        status_code: status = status.HTTP_503_SERVICE_UNAVAILABLE,
    ):
        detail = f"Сервис '{service_name}' недоступен. Проверьте подключение!"
        super().__init__(status_code, detail)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail=detail)


class ResultNotFound(ServiceExceptions):

    def __init__(self, status_code = status.HTTP_404_NOT_FOUND, detail: str = "Объект не найден!"):
        super().__init__(status_code, detail)
        raise HTTPException(status_code=self.status_code, detail=self.detail)