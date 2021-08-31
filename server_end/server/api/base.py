# -*- coding: utf-8 -*-

import os
import tornado
import tornado.web
import datetime
import urllib
import traceback
import urllib.parse as urlparse
from bson.json_util import default as json_util_default
from pycket.session import SessionMixin
import json
import copy
import base64


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    breadcrumbs = []
    smallmenu = False
    res_error = {
        "code": -1,
        "msg": "sign error",
        "data": {}
    }
    res_ok = {
        "code": 0,
        "msg": "ok",
        "data": {}
    }


    def data_received(self, data):
        pass

    def get_res_ok(self):
        return copy.deepcopy(self.res_ok)

    def get_res_error(self):
        return copy.deepcopy(self.res_error)

    @property
    def logger(self):
        """
        在handler中可以用log.debug等进行调试
        """
        import logging
        log = logging.getLogger(__name__)
        log.setLevel(logging.DEBUG)
        return log

    def json(self, para):
        if not isinstance(para, dict):
            para = {"d": para}
        # chunk = json.dumps(para).encode('utf-8').replace("</", "<\\/")
        chunk = json.dumps(para, default=json_util_default).replace("</", "<\\/")
        callback = self.get_argument("callback", None)
        browser = self.request.headers.get("User-Agent", "")
        is_ie = browser.find("compatible") > -1 and browser.find("MSIE") > -1
        is_ie = is_ie or (browser.find("Trident") > -1 and browser.find("rv:") > -1)
        ie_version = 0
        if is_ie:
            try:
                version = float(browser.split("MSIE ", 1)[-1].split(";", 1)[0])
                ie_version = int(version)
            except Exception:
                try:
                    ie_version = int(browser.split("rv:")[-1].split(".")[0])
                except Exception:
                    pass

        if callback:
            if not is_ie:
                self.set_header(
                    "Content-Type", "application/json;charset=utf-8")
            else:
                self.set_header(
                    "Content-Type", "application/javascript;charset=utf-8")
        else:
            if is_ie and ie_version < 14:
                self.set_header("Content-Type", "text/plain;charset=UTF-8")
            else:
                self.set_header(
                    "Content-Type", "application/json;charset=utf-8")

        if callback:
            self.finish(callback + "(" + chunk + ")")
        else:
            self.finish(chunk)

    def get_int(self, arg, default_value=0):
        try:
            ret = self.get_argument(arg, "")
            ret = int(ret)
        except Exception:
            ret = default_value
        return ret

    def get_len32(self, arg, default_value=None):
        try:
            ret = self.get_argument(arg, "")
            assert len(ret) == 32
        except Exception:
            ret = default_value
        return ret

    def get_date(self, arg, datefmt=None, default_value=None):
        datefmt = datefmt or "%Y-%m-%d"
        try:
            _arg = self.get_argument(arg)
            tmpl_date = datetime.datetime.strptime(_arg, datefmt)
            _arg = tmpl_date.strftime(datefmt)
        except Exception:
            _arg = default_value
        return _arg

    def get_datetime(self, arg, datetimefmt=None, default_value=None):
        datetimefmt = datetimefmt or "%Y-%m-%d %H:%M:%S"
        try:
            _arg = self.get_argument(arg)
            tmpl_datetime = datetime.datetime.strptime(_arg, datetimefmt)
            _arg = tmpl_datetime.strftime(datetimefmt)
        except Exception:
            _arg = default_value
        return _arg

    def get_part_of_list(self, arg, value_list=None, default_value=None):
        try:
            ret = self.get_argument(arg)
            assert ret in value_list
        except Exception:
            ret = default_value
        return ret

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        """
        result = {
            "code": status_code,
            "message": str(kwargs["exc_info"])
        }
        self.json(result)

    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.
        May be overridden by subclasses to add or modify values.
        The results of this method will be combined with additional
        defaults in the `tornado.template` module and keyword arguments
        to `render` or `render_string`.
        """
        namespace = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            pgettext=self.locale.pgettext,
            myjson=json,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url,
        )
        namespace.update(self.ui)
        return namespace

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header(
            'Access-Control-Allow-Headers',  # '*')
            'authorization, Authorization, Content-Type, Access-Control-Allow-Origin, '
            'Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def query_error(self):
        return self.json({
            "massage": "query error"
        })


class ViewsBaseHandler(BaseHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('user')
