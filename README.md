[![progress-banner](https://backend.codecrafters.io/progress/http-server/4f9189f1-aa5a-41c9-8dc8-fbff854028f1)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a repository for Python solution to the
["Build Your Own HTTP server" Challenge](https://app.codecrafters.io/courses/http-server/overview).

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# Asynchronous HTTP Server with Custom Routing

This project implements a simple asynchronous HTTP server that can handle GET and POST requests using custom routes. The server supports dynamic routing with URL parameters and allows file reading and writing from specified directories.

## Features

* Asynchronous handling of HTTP requests.
* Handles multiple HTTP methods: GET, POST.
* Supports dynamic URL parameters (e.g., `/echo/{query}`).
* Allows reading and writing files to/from specified directories.
* Returns file contents or error messages in response.

## Requirements

* Ensure you have `python (3.11)` installed locally
* Run `./your_program.sh` to run your program, which is implemented in
   `app/main.py`.
* Run the program with the `--directory` option to specify where files are located or where they should be written. Example: `./your_program.sh --directory /tmp`

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/tipharez-allmighty/async-http-server-python
    cd async-http-server-python
    ```
*  Make the script executable (if needed):
    ```bash
    chmod +x your_program.sh
    ```

## Testing Request Examples

# GET Request to /user-agent
curl http://localhost:4221/user-agent

# This will return the User-Agent header from the request. If not provided, the server will return a "Not Found" status.

# GET Request with URL Parameters (/echo/{query})
curl -v http://localhost:4221/echo/abc

# This request echoes the parameter abc passed in the URL path (/echo/abc).

# POST Request to /files/{query} (File Creation)
curl -v --data "12345" -H "Content-Type: application/octet-stream" http://localhost:4221/files/file_123

# This POST request sends the data 12345 with a Content-Type: application/octet-stream header, which will create a file named file_123 in the directory specified when running the server.

# GET Request to Retrieve a File
echo -n 'Hello, World!' > /tmp/foo
curl -i http://localhost:4221/files/foo

# This command first creates a file /tmp/foo with the content Hello, World!, then retrieves the file's content via a GET request to /files/foo.

# Testing Connection Close with Multiple Requests
curl --http1.1 -v http://localhost:4221/echo/banana --next http://localhost:4221/user-agent -H "User-Agent: blueberry/apple-blueberry"

# This command makes two consecutive requests using HTTP/1.1. The first request is to /echo/banana, and the second is to /user-agent, with a custom User-Agent header.

curl --http1.1 -v http://localhost:4221/echo/orange --next http://localhost:4221/ -H "Connection: close"

# This test makes two consecutive requests, using HTTP/1.1. The connection is closed after the first request, indicated by the Connection: close header.

# Testing Compression (GZIP)
curl -v -H "Accept-Encoding: gzip" http://localhost:4221/echo/abc | hexdump -C

# This request asks for the response to be compressed using gzip encoding and uses hexdump to display the binary output. You can observe the compressed response here.
