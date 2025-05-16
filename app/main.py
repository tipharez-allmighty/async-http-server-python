import asyncio
from app.routes import router
from app.context_managers import AsyncRequestManager
from app.httpparser import Request


async def hande_request(reader, writer):
    """
    Handle a single client TCP connection.

    - Reads incoming data from the client.
    - Parses it into a Request object.
    - Resolves the Request into a Response using the router.
    - Writes the Response back to the client.
    - Continues processing multiple requests on the same connection unless:
        - No data is received (client disconnected), or
        - 'Connection: close' header is found in the request.
    - Closes the connection when finished.
    """
    async with AsyncRequestManager(reader, writer) as arm:
        while True:
            recieved_bytes = await arm.reader.read(1024)
            if not recieved_bytes:
                break
            request = Request(recieved_bytes=recieved_bytes)
            response = await router.resolve(request)
            arm.writer.write(response)
            await arm.writer.drain()
            if request.headers.get("connection", "").lower() == "close":
                print("Connection is closed")
                break


async def main():
    """
    Start the TCP server.

    - Binds the server to localhost:4221.
    - Listens for incoming client connections.
    - Dispatches each client connection to hande_request().
    - Keeps running until manually interrupted (e.g., Ctrl+C).
    """
    print("Logs will appear here!")
    server = await asyncio.start_server(hande_request, "localhost", 4221)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer is shutting down")
    finally:
        print("\nServer is shut down")
