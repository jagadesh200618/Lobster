from http.server import BaseHTTPRequestHandler, HTTPServer

class Lobster(BaseHTTPRequestHandler):
    def do_GET(self):
        with open('index.html', 'r') as file:
            content = file.read()
        self.wfile.write(content.encode('utf-8'))

def runServer():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Lobster)
    print('Starting server on http://127.0.0.1:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    runServer()
