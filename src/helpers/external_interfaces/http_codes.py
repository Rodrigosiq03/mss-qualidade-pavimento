from typing import Any

from src.helpers.enum.http_status_code_enum import HttpStatusCodeEnum
from src.helpers.external_interfaces.http_models import HttpResponse


class OK(HttpResponse):
    def __init__(self, message: str = None, body: Any= None, pagination: dict = None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.OK.value, body=body)


class Created(HttpResponse):
    def __init__(self, message: str = None, body: Any= None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.CREATED.value, body=body, message=message)


class NoContent(HttpResponse):
    def __init__(self, message: str = None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.NO_CONTENT.value, body=None, message=message)


class BadRequest(HttpResponse):
    def __init__(self, message: str = None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.BAD_REQUEST.value, body=message)


class InternalServerError(HttpResponse):
    def __init__(self, message: str = None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.INTERNAL_SERVER_ERROR.value, body=message)


class NotFound(HttpResponse):
    def __init__(self, message: str = None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.NOT_FOUND.value, body=message)


class Conflict(HttpResponse):
    def __init__(self, message: str = None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.CONFLICT.value, body=message)


class RedirectResponse(HttpResponse):
    def __init__(self, body: dict, message: str = None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.REDIRECT.value, body=None, message=message,)
        self.location = body


class Forbidden(HttpResponse):
    def __init__(self, message: str = None) -> None:
        super().__init__(status_code=HttpStatusCodeEnum.FORBIDDEN.value, message=message,)
