from http.server import HTTPServer
from socketserver import ThreadingMixIn
# https://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python/51559006#51559006
# Basically a wrapper to our custom http request handler
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass