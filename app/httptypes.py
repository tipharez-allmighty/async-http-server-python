from _collections_abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Literal
from app.status import status


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class ResponseType(Enum):
    PLAIN_TEXT = "text/plain"
    FILE = "application/octet-stream"
    
@dataclass
class MethodHandler:
    method: HttpMethod
    handler: callable

    def __post_init__(self):
        if not isinstance(self.handler, Callable):
            raise ValueError(f"{self.handler} is not callable")
        if not isinstance(self.method, HttpMethod):
            raise ValueError(f"{self.method} is not valid http method")


@dataclass(frozen=True)
class Path:
    path: str

    def __post_init__(self):
        if not isinstance(self.path, str):
            raise ValueError(f"{self.path} should be a string")


@dataclass
class Response:
    status: str = status.OK
    data: str = ""
    headers: str = ""
    content_type: ResponseType = ResponseType.PLAIN_TEXT
    def __post_init__(self):
        self._encoded_data = bytes()
        # if isinstance(self.data, str):
        #     content_type = "text/plain"
        self._encoded_data = self.data.encode("utf-8")
        self.headers = (
            f"Content-type: {self.content_type.value + "\r\n"}"
            f"Content-Length: {len(self._encoded_data)}" + "\r\n"
        )

    def buildBytes(self):
        return (self.status + self.headers + "\r\n").encode(
            "utf-8"
        ) + self._encoded_data
