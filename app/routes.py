import sys

from app.httptypes import Response, ResponseType, Status
from app.httpparser import Request
from app.router import Router
from app.context_managers import AsyncFileManager

router = Router()


@router.get(path="/")
async def getHome(reqeust: Request):
    return Response()


@router.get(path="/user-agent")
async def getUserAgent(reqeust: Request):
    if reqeust.headers.get("user-agent"):
        return Response(data=reqeust.headers["user-agent"])
    else:
        return Response(status=Status.NOT_FOUND)


@router.get(path="/echo/{query}")
async def getAbc(reqeust: Request, query: str):    
    return Response(
        data=query
        )


@router.get(path="/files/{query}")
async def getFile(request: Request, query: str):
    file_path = f"{sys.argv[2]}/{query}"
    try:
        async with AsyncFileManager(file_path, "r") as file:
            data = await file.read()
    except Exception as e:
        return Response(status=Status.NOT_FOUND, data=str(e))
    return Response(content_type=ResponseType.FILE, data=data)

@router.post(path="/files/{query}")
async def createFile(request: Request, query: str):
    file_path = f"{sys.argv[2]}/{query}"
    try:
        async with AsyncFileManager(file_path, "w") as file:
            await file.write(request.body)
    except Exception as e:
        return Response(status=Status.NOT_FOUND, data=str(e))
    return Response(
        content_type=ResponseType.FILE,
        status=Status.CREATED,
        data=query
    )
