import socket  # noqa: F401

from .httpparser import HttpRequest
from .router import router


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept()
    recieved_bytes = conn.recv(1024)
    parsed_request = HttpRequest(recieved_bytes=recieved_bytes)
    response = router.resolve(parsed_request)
    conn.sendall(response)  # wait for client


if __name__ == "__main__":
    main()
