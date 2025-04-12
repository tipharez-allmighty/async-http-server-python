import socket  # noqa: F401

from .httpparser import HttpParser
from .router import router


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept()
    recieved_bytes = conn.recv(1024)
    parser = HttpParser(recieved_bytes=recieved_bytes)
    response = router.resolve(parser.path, parser.method, parser.http_version)
    conn.sendall(response)  # wait for client


if __name__ == "__main__":
    main()
