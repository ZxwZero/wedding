# coding=utf-8
# python3

"""
Name: wedding_api.py
Author: zhengxiangwei
Time: 2021-08-30 16:52
Desc:
"""

import json

from server_end.server.api.base import BaseHandler
from server_end.server.model.wedding_model import Users


class ApiWeddingAddUser(BaseHandler):
    """
    二码合一后台接口
    get: 根据产品型号 获取model信息
    post:增加新model/编辑model
    """
    OPERATE_TYPE_ADD = 1  # 新增
    OPERATE_TYPE_EDIT = 2  # 编辑

    def get(self):
        pass

    def post(self):
        res_ok = self.res_ok
        body = json.loads(self.request.body)
        Users.add_user(body)
        return self.json(res_ok)