from _collections_abc import Callable
from dataclasses import dataclass, field
from enum import Enum


class HttpMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ResponseType(Enum):
    PLAIN_TEXT = "text/plain"
    FILE = "application/octet-stream"


class Compression(Enum):
    gzip = "gzip"


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
class Status:
    OK: str = field(default="HTTP/1.1 200 OK\r\n", init=False)
    CREATED: str = field(default="HTTP/1.1 201 Created\r\n", init=False)
    NOT_FOUND: str = field(default="HTTP/1.1 404 Not Found\r\n", init=False)
    BAD_REQUEST: str = field(default="HTTP/1.1 400 Bad Request\r\n", init=False)


@dataclass
class Response:
    status: str = Status.OK
    data: str = ""
    headers: str = ""
    encoding: str | None = None
    content_type: ResponseType = ResponseType.PLAIN_TEXT

    def __post_init__(self):
        self._encoded_data = bytes()
        self._encoded_data = self.data.encode("utf-8")

        self.headers = self.headers + (
            f"Content-type: {self.content_type.value + "\r\n"}"
            f"Content-Length: {len(self._encoded_data)}" + "\r\n"
        )

    def addEncoding(self):
        if self.encoding:
            encoding_list = self.encoding.split(",")
            encoding = [
                stripped_encoding
                for encoding in encoding_list
                if (stripped_encoding := encoding.strip())
                in Compression._value2member_map_
            ]
            if encoding:
                encoding_line = f"Content-Encoding: {encoding[0]}" + "\r\n"
                self.headers = encoding_line + self.headers

    def buildBytes(self):
        return (self.status + self.headers + "\r\n").encode(
            "utf-8"
        ) + self._encoded_data
