from _collections_abc import Callable
from dataclasses import dataclass, asdict
from enum import Enum


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class MethodHandler:
    method: HttpMethod
    handler: callable

    def __post_init__(self):
        if not isinstance(self.handler, Callable):
            raise ValueError(f"{self.handler} is not callable")
        try:
            HttpMethod[self.method]
        except:
            raise ValueError(f"{self.method} is not valid http method")


@dataclass(frozen=True)
class Path:
    path: str

    def __post_init__(self):
        if not isinstance(self.path, str):
            raise ValueError(f"{self.path} should be a string")


@dataclass
class Response:
    status: str = "HTTP/1.1 200 OK\r\n"
    data: str = ""
    headers: str = ""

    def __post_init__(self):
        self._encoded_data = bytes()
        if not len(self.data) == 0:
            if isinstance(self.data, str):
                content_type = "text/plain"
            self._encoded_data = self.data.encode("utf-8")
            self.headers = (
                f"Content-type: {content_type + "\r\n"}"
                f"Content-Length: {len(self._encoded_data)}" + "\r\n"
            )

    def buildBytes(self):
        return (self.status + self.headers + "\r\n").encode(
            "utf-8"
        ) + self._encoded_data
