from queue import Queue

from app.types import MethodHandler, HttpMethod, Status, Response
from app.httpparser import Request


class Router:
    """
    A router that maps HTTP methods to specific request handlers based on path.

    It handles routing for different HTTP methods (GET, POST) and can resolve paths with parameters.
    """

    def __init__(self):
        self.__route_map = {}

    @property
    def route_map(self):
        return self.__route_map

    def _route(self, path: str, method: HttpMethod):
        """
        Decorator to register a request handler for a specific HTTP method and path.

        Args:
            path (str): The path for the request.
            method (HttpMethod): The HTTP method (GET, POST, etc.).

        Returns:
            callable: A decorator that registers the handler function for the path and method.
        """

        def wrapper(handler: callable):
            if self.__route_map.get(path):
                self.__route_map[path].append(
                    MethodHandler(method=method, handler=handler)
                )
            else:
                self.__route_map[path] = [MethodHandler(method=method, handler=handler)]

        return wrapper

    def get(self, path: str):
        """
        Register a handler for HTTP GET requests.
        """
        return self._route(path=path, method=HttpMethod.GET)

    def post(self, path: str):
        """
        Register a handler for HTTP POST requests.
        """
        return self._route(path=path, method=HttpMethod.POST)

    def _pathQueue(self, path: str):
        """
        Create a queue of potential routes by breaking down the path into segments.

        This is useful for handling routes with parameters.

        Args:
            path (str): The full path to be resolved.

        Returns:
            Queue: A queue of paths with parameters replaced by placeholders (e.g., {query}).
        """
        queue = Queue()
        splited_path = path.split("/")[::-1]
        splited_path.pop()
        for parameter in splited_path:
            query_path = path.replace(parameter, "{query}")
            queue.put((query_path, parameter))
        return queue

    @staticmethod
    def _getEncoding(parsed_request: Request):
        if encoding := parsed_request.headers.get("accept-encoding", ""):
            return encoding

    @staticmethod
    def _getConnection(paresed_request: Request):
        if conn := paresed_request.headers.get("connection", ""):
            conn = f"Connection: {conn + "\r\n"}"
        return conn

    def _formResponse(self, parsed_request: Request, response: Response | None):
        if response:
            response.encoding = self._getEncoding(parsed_request)
            response.headers += self._getConnection(parsed_request)
            response.addEncoding()
        else:
            response = Response(status=Status.NOT_FOUND)
        return response.buildBytes()

    async def _routerLookup(
        self, path: str, parsed_request: Request, parameter: str | None = None
    ):
        """
        Attempt to resolve the request based on the route map.

        This method checks for a matching path and method handler, and calls the handler if found.

        Args:
            path (str): The path of the incoming request.
            parsed_request (Request): The parsed request object.
            parameter (str | None): A path parameter, if applicable (default is None).

        Returns:
            Response | None: The response returned by the handler, or None if no match is found.
        """
        if path in self.__route_map:
            for method_handler in self.__route_map[path]:
                if method_handler.method.value == parsed_request.method:
                    return (
                        await method_handler.handler(parsed_request)
                        if not parameter
                        else await method_handler.handler(parsed_request, parameter)
                    )

    async def resolve(self, parsed_request: Request):
        """
        Resolve the request by looking up the appropriate handler in the router.

        It first checks for an exact match, and then tries to resolve the path with parameters.

        Args:
            parsed_request (Request): The parsed request object.

        Returns:
            bytes: The formatted response ready to be sent to the client.
        """
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
        return self._formResponse(parsed_request, response)
