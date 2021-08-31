# -*- coding: utf-8 -*-

import os
import sys
import time
import redis
import hashlib
import pymongo
import base64
import pprint
from openpyxl import load_workbook
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = "/".join(PROJECT_ROOT.split("/")[:-1])


def get_platform():
    """
    返回系统平台
    Mac为Darwin
    Linux为Linux
    """
    res = os.popen("uname").readlines()[0]
    return res.strip()


def is_test():
    try:
        if get_platform() == "Darwin":
            return True
        else:
            return False
    except Exception:
        return True


def auth(func):
    def wrapper(self, *args, **kwargs):
        cms_cookie = self.get_secure_cookie('cms_cookie')
        # user = self.session.get('user')
        if cms_cookie:
            print('验证成功')
            return func(self, *args, **kwargs)
        else:
            print('验证失败')
    return wrapper


def get_ts():
    return int(time.time())


def make_md5(res):
    """入参为字符串，返回小写的md5值"""
    m = hashlib.md5()
    if isinstance(res, str):
        res = res.encode("utf-8")
    m.update(res)
    return m.hexdigest()


def make_md5_bytes(text):
    """入参为字符串，返回小写的md5值"""
    md5 = hashlib.md5()
    if not isinstance(text, bytes):
        text = str(text).encode('utf-8')
    md5.update(text)
    return md5.digest()


def sort_keys(params, salt=None):
    _keys = []
    for k, v in params.items():
        _keys.append("=".join(
            (str(k), str(v))
        ))
    _keys.sort()
    if salt:
        _keys.append(salt)
    return "&".join(_keys)


if __name__ == "__main__":
    print(PROJECT_ROOT)
    # read_from_xlsx()
    # read_from()
