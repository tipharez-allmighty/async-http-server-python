class Request:
    def __init__(self, recieved_bytes: bytes):
        self.recieved_bytes: bytes = recieved_bytes
        self.request_string: str = recieved_bytes.decode("utf-8")
        self.request_line: None | str = None
        self.headers: None | list[str] | dict[str, str] = None
        self.body: None | str = None
        self.method: str | None = None
        self.path: str | None = None
        self.http_version: str | None = None
        self._parse_data()

    def __repr__(self):
        return self.request_string

    def _parse_data(self):
        if not self.request_string:
            return None
        reqeust_data_list = self.request_string.split("\r\n")
        self.request_line, *self.headers, _, self.body = reqeust_data_list
        self._parse_request_line()
        self._parse_headers()

    def _parse_request_line(self):
        if not self.request_line:
            return None
        try:
            requset_line_list = self.request_line.split(" ")
            self.method, self.path, self.http_version = requset_line_list
        except Exception as e:
            print(f"Malformed Request line. Error: {str(e)}")
            self.method, self.path, self.http_version = None, None, None

    def _parse_headers(self):
        headers_dict = dict()
        if not self.headers:
            return None
        for header in self.headers:
            if isinstance(header, str) and len(header) != 0:
                header = header.split(":", maxsplit=1)
                headers_dict[header[0].lower()] = header[1].strip()
        self.headers = headers_dict
