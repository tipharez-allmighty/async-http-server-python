from queue import Queue

from app.httptypes import MethodHandler, HttpMethod, Response
from app.httpparser import HttpRequest
from app.status import status


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

    async def _routerLookup(
        self, path: str, parsed_request: HttpRequest, parameter: str | None = None
    ):
        if path in self.__route_map:
            for method_handler in self.__route_map[path]:
                if method_handler.method.value == parsed_request.method:
                    return (
                        await method_handler.handler(parsed_request)
                        if not parameter
                        else await method_handler.handler(parsed_request, parameter)
                    )

    async def resolve(self, parsed_request: HttpRequest):
        response = await self._routerLookup(
            path=parsed_request.path,
            parsed_request=parsed_request,
        )
        path_queue = self._pathQueue(path=parsed_request.path)
        while not response and not path_queue.empty():
            current_path, current_parameter = path_queue.get()
            response = await self._routerLookup(
                path=current_path,
                parsed_request=parsed_request,
                parameter=current_parameter,
            )
        response = (
            response if response else
            Response(
                status=status.NOT_FOUND
            )
        )
        return response.buildBytes()

    def get(self, path: str):
        def wrapper(handler: callable):
            if self.__route_map.get(path):
                self.__route_map[path].append(
                    MethodHandler(method=HttpMethod.GET, handler=handler)
                )
            else:
                self.__route_map[path] = [MethodHandler(method=HttpMethod.GET, handler=handler)]

        return wrapper
