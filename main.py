import socket
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from threading import Thread
import mimetypes
import datetime
import json

HOST = '127.0.0.1'
PORT = 5000

class HTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        url = urllib.parse.urlparse(self.path)

        if url.path == '/':
            self._render_html('front-init\index.html')
        elif url.path=='/message.html':
             self._render_html("front-init\message.html")
        else:
            path=pathlib.Path().joinpath('front-init'+url.path)
            if path.exists():
                self.send_static(path)
            else:
                self._render_html('front-init\error.html', 404)

        
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        # data_parse = urllib.parse.unquote_plus(data.decode())
        # data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        self.send(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
    
    def send(self,data):
        print(data)
        client_socket = socket.socket()
        client_socket.connect(('127.0.0.1', 5000))
        client_socket.send(data)

    def send_static(self,path):
        self.send_response(200)
        mt = mimetypes.guess_type(path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(path, 'rb') as file:
            self.wfile.write(file.read())
    
    def _render_html(self, filename, status_code=200):

        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
                self.wfile.write(file.read())




def run(host,port):
        sock = socket.socket()
        sock.bind((host,port))
        sock.listen(1)
        conn, addr = sock.accept()
        with conn:
            while True:
                time=str(datetime.datetime.now())
                data = conn.recv(1024)
                if not data:
                    break
                data = urllib.parse.unquote_plus(data.decode())
                data=[param.split('=') for param in data.split('&')]
                data_dict={}
                for i in data:
                    data_dict[i[0]]=i[1]
                data_json={time:data_dict}
                with open('front-init/storage/data.json') as file:
                    file_data = json.load(file)
                try:
                    file_data.update(data_json)
                    with open ('front-init/storage/data.json','w') as file: 
                        json.dump(file_data, file, indent=2)
                except ValueError:
                    data_json=json.dump(data_json,indent=2)
                    with open ('front-init/storage/data.json','w') as file: 
                        file.write(data_json)

t1 = Thread(target=run, args=(HOST, PORT))
t1.start()
server = HTTPServer(('', 3000), HTTPHandler)

server.serve_forever()