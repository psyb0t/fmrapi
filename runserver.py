#!/usr/bin/env python
from fmrapi import app, config
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

http_server = HTTPServer(WSGIContainer(app))
http_server.bind(8088, address='0.0.0.0')
http_server.start(0)
IOLoop.instance().start()
