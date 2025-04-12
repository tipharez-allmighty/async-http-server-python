class HttpParser:
    def __init__(self, recieved_bytes: bytes):
        self.recieved_bytes = recieved_bytes
        self.request_string = recieved_bytes.decode("utf-8")
        self.request_line = None
        self.headers = None
        self.method = None
        self.path = None
        self.http_version = None
        self._parseData()
        self._parseRequestLine()

    def _parseData(self):
        if not self.request_string:
            return None
        reqeust_data_list = self.request_string.split("\r\n")
        self.request_line, *self.headers = reqeust_data_list

    def _parseRequestLine(self):
        if not self.request_line:
            return None
        try:
            requset_line_list = self.request_line.split(" ")
            self.method, self.path, self.http_version = requset_line_list
        except Exception as e:
            print("Malformed Request line")
            self.method, self.path, self.http_version = None, None, None
