# coding=utf-8
# python3

"""
Name: test.py
Author: zhengxiangwei
Time: 2021-08-31 16:06
Desc:
"""

import json

from server_end.server.api.base import BaseHandler


class ApiTest(BaseHandler):
    """
    二码合一后台接口
    get: 根据产品型号 获取model信息
    post:增加新model/编辑model
    """
    OPERATE_TYPE_ADD = 1  # 新增
    OPERATE_TYPE_EDIT = 2  # 编辑

    def get(self):
        res_ok = self.res_ok
        return self.json(res_ok)
