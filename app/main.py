import socket  # noqa: F401
import time
import threading
import asyncio
from app.router import router
from app.requestmanager import RequestManager

def handleRequest(conn):
    print(f"Handling request in thread: {threading.current_thread().name}", flush=True)
    with RequestManager(conn) as rq:
        response = router.resolve(rq.request)
        rq.connection.sendall(response)
        
def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print('Server is running on port: 4221')
    try:
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(
                target=handleRequest,
                args=[conn]
            )
            client_thread.start()
            # await asyncio.to_thread(handleRequest, conn)
    except KeyboardInterrupt:
        print('\nServer is shutting down')
    finally:
        server_socket.close()
        print('\nServer has been shut down')


if __name__ == "__main__":
    # asyncio.run(main())
    main()
