import socket
import json
from jinja2 import Environment, FileSystemLoader
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from threading import Thread
import logging

class HTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self._render_html('front-init\index.html')
        
    def do_POST(self):
        pass

    def _render_html(self, filename, status_code=200):

        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(filename, 'rb') as file:
                self.wfile.write(file.read())

class serv_socket:
    pass

server = HTTPServer(('', 3000), HTTPHandler)
server.serve_forever()