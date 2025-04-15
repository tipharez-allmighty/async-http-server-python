from queue import Queue

from app.httptypes import Path, Response, MethodHandler


class Router:
    def __init__(self):
        self.__route_map = {}

    @property
    def route_map(self):
        return self.__route_map

    def _pathQueue(self, path: Path):
        queue = Queue()
        splited_path = path.path.split("/")[::-1]
        splited_path.pop()
        for parameter in splited_path:
            query_path = Path(
                path=path.path.replace(parameter, "{query}"),
            )
            queue.put((query_path, parameter))
        return queue

    def _routerLookup(self, path: Path, method: str, parameter: str | None = None):
        if path in self.__route_map:
            for method_handler in self.__route_map[path]:
                if method_handler.method == method:
                    return (
                        method_handler.handler()
                        if not parameter
                        else method_handler.handler(parameter)
                    )

    def resolve(self, path: str, method: str, http_version: str):
        path = Path(path)
        response = self._routerLookup(
            path=path,
            method=method,
        )
        path_queue = self._pathQueue(path=path)
        while not response and not path_queue.empty():
            current_path, current_parameter = path_queue.get()
            response = self._routerLookup(
                path=current_path, method=method, parameter=current_parameter
            )
        return response.buildBytes() if response else b"HTTP/1.1 404 Not Found\r\n"

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
    return Response()


@router.get(path="/echo/{query}")
def getAbc(query: str):
    return Response(data=query)
