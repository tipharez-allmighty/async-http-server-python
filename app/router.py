from queue import Queue

from app.httptypes import Path, Response, MethodHandler
from app.httpparser import HttpRequest

class Router:
    def __init__(self):
        self.__route_map = {}

    @property
    def route_map(self):
        return self.__route_map

    def _pathQueue(self, path: str):
        queue = Queue()
        splited_path = path.split("/")[::-1]
        splited_path.pop()
        for parameter in splited_path:
            query_path = path.replace(parameter, "{query}")
            queue.put((query_path, parameter))
        return queue

    def _routerLookup(self, path: str, parsed_request: HttpRequest, parameter: str | None = None):
        if path in self.__route_map:
            for method_handler in self.__route_map[path]:
                if method_handler.method == parsed_request.method:
                    return (
                        method_handler.handler(parsed_request)
                        if not parameter
                        else method_handler.handler(parsed_request, parameter)
                    )

    def resolve(self, parsed_request: HttpRequest):
        response = self._routerLookup(
            path=parsed_request.path,
            parsed_request=parsed_request,
        )
        path_queue = self._pathQueue(path=parsed_request.path)
        while not response and not path_queue.empty():
            current_path, current_parameter = path_queue.get()
            response = self._routerLookup(
                path=current_path,
                parsed_request=parsed_request,
                parameter=current_parameter
            )
        return response.buildBytes() if response else b"HTTP/1.1 404 Not Found\r\n\r\n"

    def get(self, path: str):
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
def getHome(reqeust: HttpRequest):
    return Response()

@router.get(path="/user-agent")
def getUserAgent(reqeust: HttpRequest):
    return Response(data=reqeust.headers['User-Agent'])

@router.get(path="/echo/{query}")
def getAbc(reqeust: HttpRequest, query: str):
    return Response(data=query)
