import asyncio
from app.httpparser import Request


class RequestManager:
    def __init__(self, connection, max_bytes: int = 1024):
        self.connection = connection
        self.max_bytes = max_bytes

    def __enter__(self):
        recieved_bytes = self.connection.recv(self.max_bytes)
        self.request = Request(recieved_bytes=recieved_bytes)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.close()


class AsyncRequestManager:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        self.writer.close()
        await self.writer.wait_closed()


class AsyncFileManager:
    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.file = None
        self.loop = asyncio.get_running_loop()

    async def __aenter__(self):
        self.file = await self.loop.run_in_executor(
            None, lambda: open(self.filename, self.mode)
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

    async def read(self):
        return await self.loop.run_in_executor(None, lambda: self.file.read())

    async def write(self, text: str):
        return await self.loop.run_in_executor(None, lambda: self.file.write(text))