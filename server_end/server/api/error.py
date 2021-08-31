# coding=utf-8
# python3

"""
Name: error.py
Author: zhengxiangwei
Time: 2021-04-14 14:21
Desc: 404路由错误
"""

from datetime import datetime

from server_end.server.api.base import BaseHandler


class NotFoundHandler(BaseHandler):
    def get(self):
        res_ok = self.get_res_ok()
        res_error = self.get_res_error()

        try:
            title = "404"
            items = ["Item 1", "Item 2", "Item 3"]
            date = datetime.now()
            context = {
                "items": items,
                "name": "你好",
                "date": str(date)[:-4],
            }
            self.render("404.html", title=title, context=context)

        except Exception as e:
            res_error['msg'] = str(e)
            return self.json(res_error)




