import socket  # noqa: F401
import threading
from concurrent.futures import ThreadPoolExecutor
from app.routes import router
from app.context_managers import RequestManager


def handle_request(conn):
    print(f"Handling request in thread: {threading.current_thread().name}", flush=True)
    with RequestManager(conn) as rq:
        response = router.resolve(rq.request)
        rq.connection.sendall(response)


def thread_execution(port=4221):
    server_socket = socket.create_server(("localhost", port), reuse_port=True)
    print(f"Server is running on port: {port}")
    try:
        with ThreadPoolExecutor(max_workers=8) as executor:
            while True:
                conn, addr = server_socket.accept()
                executor.submit(handle_request, conn)
    except KeyboardInterrupt:
        print("\nServer is shutting down")
    finally:
        server_socket.close()
        print("\nServer has been shut down")


def main():
    print("Logs from your program will appear here!")
    thread_execution()


if __name__ == "__main__":
    main()
