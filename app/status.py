from dataclasses import dataclass, field


@dataclass(frozen=True)
class Status:
    OK: str = field(default="HTTP/1.1 200 OK\r\n", init=False)
    NOT_FOUND: str = field(default="HTTP/1.1 404 Not Found\r\n", init=False)


status = Status()
