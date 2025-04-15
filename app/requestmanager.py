from app.httpparser import HttpRequest

class RequestManager:
    def __init__(self, connection, max_bytes=1024):
        self.connection = connection
        self.max_bytes = max_bytes
        
    def __enter__(self):
        recieved_bytes = self.connection.recv(1024)
        self.request = HttpRequest(recieved_bytes=recieved_bytes)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.close()