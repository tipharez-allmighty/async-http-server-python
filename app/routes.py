# This code demonstrates how routes work with the `Router` class.
# It defines HTTP endpoints with different methods (GET and POST) to handle requests.

# - The `get_home` route responds with a simple default response.
# - The `get_user_agent` route checks for the "user-agent" header and responds with its value or a "Not Found" status.
# - The `get_abc` route returns the value of the query parameter.
# - The `get_file` route reads and returns a file's contents, or responds with an error if the file is not found.
# - The `create_file` route writes data to a file and responds with the created file's name or an error message.

# This showcases how paths, HTTP methods, and dynamic parameters can be handled by the router.

import sys

from app.types import Response, ResponseType, Status
from app.httpparser import Request
from app.router import Router
from app.context_managers import AsyncFileManager

router = Router()


@router.get(path="/")
async def get_home(reqeust: Request):
    return Response()


@router.get(path="/user-agent")
async def get_user_agent(reqeust: Request):
    if reqeust.headers.get("user-agent"):
        return Response(data=reqeust.headers["user-agent"])
    else:
        return Response(status=Status.NOT_FOUND)


@router.get(path="/echo/{query}")
async def get_abc(reqeust: Request, query: str):
    return Response(data=query)


@router.get(path="/files/{query}")
async def get_file(request: Request, query: str):
    file_path = f"{sys.argv[2]}/{query}"
    try:
        async with AsyncFileManager(file_path, "r") as file:
            data = await file.read()
    except Exception as e:
        return Response(status=Status.NOT_FOUND, data=str(e))
    return Response(content_type=ResponseType.FILE, data=data)


@router.post(path="/files/{query}")
async def create_file(request: Request, query: str):
    file_path = f"{sys.argv[2]}/{query}"
    try:
        async with AsyncFileManager(file_path, "w") as file:
            await file.write(request.body)
    except Exception as e:
        return Response(status=Status.NOT_FOUND, data=str(e))
    return Response(content_type=ResponseType.FILE, status=Status.CREATED, data=query)
