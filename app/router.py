from _collections_abc import Callable
from dataclasses import dataclass
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

class Router:
    def __init__(self):
        self.__route_map = {}

    @property
    def route_map(self):
        return self.__route_map

    def resolve(self, path: str, method: str, http_version: str):
        path = Path(path=path)
        
        if path in self.__route_map:
            return self.route_map[path][0].handler()
        else:
            return b"HTTP/1.1 404 Not Found\r\n\r\n"

    def get(self, path: str):
        path = Path(path=path)

        def wrapper(handler: callable):
            if self.__route_map.get(path):
                self.__route_map[path].append(
                    MethodHandler(method="GET", handler=handler)
                )
            else:
                self.__route_map[path] = [MethodHandler(method="GET", handler=handler)]

        return wrapper


router = Router()


@router.get(path="/")
def getHome():
    return b"HTTP/1.1 200 OK\r\n\r\n"
