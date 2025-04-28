from _collections_abc import Callable
from dataclasses import dataclass, field
from enum import Enum

import gzip


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
    """
    Represents an HTTP response with status, headers, content type, and data.

    Attributes:
        status (str): The HTTP status line (e.g., "200 OK").
        data (str): The response body/content.
        headers (str): Response headers.
        encoding (str): The encoding type (e.g., gzip).
        content_type (ResponseType): The content type (e.g., text, file).

    Methods:
        addEncoding: Adds encoding (e.g., gzip) and compresses data.
        buildBytes: Constructs the HTTP response as bytes.
    """

    status: str = Status.OK
    data: str = ""
    headers: str = ""
    encoding: str = ""
    content_type: ResponseType = ResponseType.PLAIN_TEXT

    def __post_init__(self):
        self._encoded_data = self.data.encode("utf-8")

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
                self._encoded_data = gzip.compress(self._encoded_data)

    def buildBytes(self):
        self.headers = self.headers + (
            f"Content-type: {self.content_type.value + "\r\n"}"
            f"Content-Length: {len(self._encoded_data)}" + "\r\n"
        )
        return (self.status + self.headers + "\r\n").encode(
            "utf-8"
        ) + self._encoded_data
