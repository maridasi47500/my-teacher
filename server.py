#!/usr/bin/env python3
"""
License: MIT License
Copyright (c) 2023 Miel Donkers

Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from route import Route
from urllib import parse
from urllib.parse import parse_qs, urlparse
import requests
req = requests.Session()
req.cookies["email"]=""
req.cookies["name"]=""
req.cookies["notice"]=""
from urllib.parse import urlencode




class S(BaseHTTPRequestHandler):
    def _set_response(self,redirect=False,cookies=False):
        if redirect:
          self.send_response(301)
          self.send_header('Status', '301 Redirect')
          self.send_header('Location', redirect)
          self.send_header('Content-type', 'text/html;charset=utf-8')
        else:
          self.send_response(200)
          self.send_header('Content-type', 'text/html')
        if cookies:
          self.send_header("Cookie", urlencode(cookies))

        self.end_headers()
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        myparams = parse_qs(urlparse(self.path).query)
        dictcook=(req.cookies.get_dict())

        myProgram=Route().run(path=str(self.path),params=myparams,session=dictcook,url=self.path)
        sess= myProgram.get_session()
        print("param session",sess)
        for cookie in req.cookies:
                cookie.value = sess[cookie.name]

        self._set_response(redirect=myProgram.get_redirect(),cookies=req.cookies)
        self.wfile.write(myProgram.get_html().encode('utf-8'))
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))
        myparams=(parse.parse_qs(post_data.decode('utf-8')))
        dictcook=(req.cookies.get_dict())


        logging.info(parse.parse_qs(post_data.decode('utf-8')))
        myProgram=Route().run(path=str(self.path),params=myparams,session=dictcook,url=self.path)
        sess= myProgram.get_session()
        for x in sess:
          req.cookies.set(x,sess[x])

        self._set_response(redirect=myProgram.get_redirect(),cookies=req.cookies)
        self.wfile.write(myProgram.get_html().encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
