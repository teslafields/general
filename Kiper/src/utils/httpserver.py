from threading import Thread
import socketserver
import http.server

class HttpServer:
    def __init__(self, address='10.5.0.13', port=8888):
        Handler = http.server.SimpleHTTPRequestHandler
        self.handler = socketserver.TCPServer((address, port), Handler)
        print("Serving at port: ", port)

    def thread_me(self):
        Thread(target=self.handler.serve_forever).start()

s = HttpServer().thread_me()
