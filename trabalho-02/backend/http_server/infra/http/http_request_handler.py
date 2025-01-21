"""
    A SIMPLE CUSTOM HTTP SERVER CREATED TO HANDLE REQUEST FOR THE CHATUBA CHAT API
    HEAVILTY INSPIRED BY: https://gist.github.com/dfrankow/f91aefd683ece8e696c26e183d696c29
    IMPORTANT: iN ORTDER of this to work controllers always have to return something
"""

import json
import traceback
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

class HTTPRequestHandler(BaseHTTPRequestHandler):
    http_router = {}

    @classmethod
    def set_http_request_parser(cls, http_request_parser):
        cls.http_request_parser = http_request_parser
    
    @classmethod
    def set_http_router(cls, http_router):   
        cls.http_router = http_router

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "http://localhost:5500")
        self.send_header("Access-Control-Allow-Methods", self.http_router.get_supported_methods())
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_POST(self):
        request_obj = self.http_request_parser.parse_request(self)
        try:
            (statusCode, data) = self.http_router.route_request(request_obj)
            response_body = json.dumps(data).encode('utf-8')
            self.send_response(statusCode)
            self.send_header("Content-Type", "application/json")
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5500')
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.end_headers()

    def do_GET(self):
        request_obj =  self.http_request_parser.parse_request(self)
        try:
            (statusCode, data) = self.http_router.route_request(request_obj)
            response_body = json.dumps(data).encode('utf-8')
            self.send_response(statusCode)
            self.send_header("Content-Type", "application/json")
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5500')
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.end_headers()
    
    def do_DELETE(self):
        request_obj =  self.http_request_parser.parse_request(self)
        try:
            (statusCode, data) = self.http_router.route_request(request_obj)
            response_body = json.dumps(data).encode('utf-8')
            self.send_response(statusCode)
            self.send_header("Content-Type", "application/json")
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5500')
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.end_headers()
    
    def do_PATCH(self):
        request_obj =  self.http_request_parser.parse_request(self)
        try:
            (statusCode, data) = self.http_router.route_request(request_obj)
            response_body = json.dumps(data).encode('utf-8')
            self.send_response(statusCode)
            self.send_header("Content-Type", "application/json")
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5500')
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
            self.end_headers()



