import os
import sys

from app.httptypes import Response, ResponseType
from app.httpparser import HttpRequest
from app.router import Router
from app.status import status

router = Router()

@router.get(path="/")
async def getHome(reqeust: HttpRequest):
    return Response()


@router.get(path="/user-agent")
async def getUserAgent(reqeust: HttpRequest):
    if reqeust.headers.get("user-agent"):
        return Response(data=reqeust.headers["user-agent"])
    else:
        return Response(status=status.NOT_FOUND)


@router.get(path="/echo/{query}")
async def getAbc(reqeust: HttpRequest, query: str):
    return Response(data=query)

@router.get(path="/files/{query}")
async def getFile(request: HttpRequest, query: str):
    file_path = f"{sys.argv[2]}/{query}"
    print(file_path)
    try: 
        with open(file_path, 'r') as file:
            data = file.read()
    except Exception as e:
        return Response(
            status=status.NOT_FOUND,
            data=str(e)
            )
    return Response(
        content_type=ResponseType.FILE,
        data=data
    )