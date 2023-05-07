from http.server import HTTPServer, SimpleHTTPRequestHandler

print('\n=> http://localhost:8000')

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)

for i in range(3):
    try:
        httpd.handle_request()
    except Exception as e:
        print(e)
httpd.server_close()