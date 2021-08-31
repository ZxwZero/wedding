#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import Application
import tornado.ioloop
from tornado.options import define, options, parse_command_line
import os
import sys
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from server_end.server.routers import Routers
from server_end.server.common.util import is_test

define("port", default=8500, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")

static_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "./static"
    )
)


template_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "./templates"
    )
)


if __name__ == "__main__":
    host = "0.0.0.0"
    parse_command_line()
    if is_test():
        options.port = 9999
    print("Tornado Start http://{}:{}".format(host, options.port))

    settings = {
        'debug': options.debug,
        'static_path': static_path,
        'template_path': template_path,
        "login_url": "/login",
        "cookie_secret": "s632504c51d6456781cdf903dcfeeerf"
    }

    app = Application(Routers, **settings)
    http_server = tornado.httpserver.HTTPServer(app, max_buffer_size=2073741824, xheaders=True)  # 最大文件限制传输大小是1个T
    # server=HTTPserver(application)
    http_server.listen(options.port, address=host)
    tornado.ioloop.IOLoop.current().start()
