# -*- coding:utf-8 -*-
from datetime import date, datetime
import json


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['code'] = self.status_code
        rv['message'] = self.message
        return rv


class ComplexEncoder(json.JSONEncoder):
    """jsonu序列化时对datetime和date做特殊处理"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def successReturn(data, msg):
    return {
        'code': 200,
        'data': data,
        'msg': msg
    }
