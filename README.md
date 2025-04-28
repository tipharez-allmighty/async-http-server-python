[![progress-banner](https://backend.codecrafters.io/progress/http-server/4f9189f1-aa5a-41c9-8dc8-fbff854028f1)](https://app.codecrafters.io/users/codecrafters-bot?r=2qF)

This is a starting point for Python solutions to the
["Build Your Own HTTP server" Challenge](https://app.codecrafters.io/courses/http-server/overview).

[HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) is the
protocol that powers the web. In this challenge, you'll build a HTTP/1.1 server
that is capable of serving multiple clients.

Along the way you'll learn about TCP servers,
[HTTP request syntax](https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html),
and more.

**Note**: If you're viewing this repo on GitHub, head over to
[codecrafters.io](https://codecrafters.io) to try the challenge.

# Passing the first stage

The entry point for your HTTP server implementation is in `app/main.py`. Study
and uncomment the relevant code, and push your changes to pass the first stage:

```sh
git commit -am "pass 1st stage" # any msg
git push origin master
```

Time to move on to the next stage!

# Stage 2 & beyond

Note: This section is for stages 2 and beyond.

1. Ensure you have `python (3.11)` installed locally
1. Run `./your_program.sh` to run your program, which is implemented in
   `app/main.py`.
1. Commit your changes and run `git push origin master` to submit your solution
   to CodeCrafters. Test output will be streamed to your terminal.

# Asynchronous HTTP Server with Custom Routing

This project implements a simple asynchronous HTTP server that can handle GET and POST requests using custom routes. The server supports dynamic routing with URL parameters and allows file reading and writing from specified directories.

## Features

* Asynchronous handling of HTTP requests.
* Handles multiple HTTP methods: GET, POST.
* Supports dynamic URL parameters (e.g., `/echo/{query}`).
* Allows reading and writing files to/from specified directories.
* Returns file contents or error messages in response.

## Requirements

* Python 3.7 or later

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2.  Make the script executable (if needed):
    ```bash
    chmod +x your_program.sh
    ```

## Running the Server

To run the server, use one of the following options:

**Option 1: Running with a specified directory**

Run the program with the `--directory` option to specify where files are located or where they should be written. Example:

```bash
./your_program.sh --directory /tmp
This will start the asynchronous server and use /tmp as the working directory for reading and writing files.Option 2: Running without a directoryIf you don't specify the directory, the program will still work without file reading or writing functionality. Example:./your_program.sh
In this case, the file-related routes will return an error or not be functional.RoutesThe server supports the following routes:GET /: Returns a default HTTP response.GET /user-agent: Returns the user-agent from the request headers or a "Not Found" status.GET /echo/{query}: Echoes the {query} parameter from the URL.GET /files/{query}: Reads a file from the specified directory and returns its contents.POST /files/{query}: Creates a file in the specified directory with the provided request body.Example Requestscurl -v http://localhost:4221/

# This request will return the default response from the server.

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
