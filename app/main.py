import asyncio
from app.routes import router
from app.context_managers import AsyncRequestManager
from app.httpparser import Request


async def handleRequest(reader, writer):
    async with AsyncRequestManager(reader, writer) as arm:
        while True:
            recieved_bytes = await arm.reader.read(1024)
            if not recieved_bytes:
                break
            request = Request(recieved_bytes=recieved_bytes)
            response = await router.resolve(request)
            arm.writer.write(response)
            await arm.writer.drain()
            if request.headers.get("connection", ""):
                break


async def main():
    print("Logs will appear here!")
    server = await asyncio.start_server(handleRequest, "localhost", 4221)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer is shutting down")
    finally:
        print("\nServer is shut down")
