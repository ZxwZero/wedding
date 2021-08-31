# -*- codding: utf-8 -*-

import os
import sys
from tornado.web import url
from tornado.web import RequestHandler

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))

from server_end.server.api import wedding_api
from server_end.server.api import test


class BaseHandler(RequestHandler):
    def get(self):
        self.render("index.html", data={})

    def post(self):
        self.get()

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def prepare(self):
        pass

    def on_finish(self):
        pass


Routers = [
    # 接口路径
    url(r"/api/wedding_add", wedding_api.ApiWeddingAddUser),

    # 测试
    url(r"/api/test", test.ApiTest),

]
