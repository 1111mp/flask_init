# -*- coding:utf-8 -*-
from datetime import date, datetime, time
import json
import uuid
from sqlalchemy.ext.declarative import DeclarativeMeta

from redis import WatchError
from .extensions import xtredis
from api.config import USERAUTHKEY

# https://dormousehole.readthedocs.io/en/latest/patterns/apierrors.html


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
        elif isinstance(obj, time):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj.__class__, DeclarativeMeta):
            return self.default({i.name: getattr(obj, i.name) for i in obj.__table__.columns})
        elif isinstance(obj, dict):
            for k in obj:
                try:
                    if isinstance(obj[k], (datetime, date, DeclarativeMeta)):
                        obj[k] = self.default(obj[k])
                    else:
                        obj[k] = obj[k]
                except TypeError:
                    obj[k] = None
            return obj
        else:
            return json.JSONEncoder.default(self, obj)


def successReturn(data, msg=''):
    return {
        'code': 200,
        'data': data,
        'msg': msg
    }


def cacheToken(userId, token, maxAge=60 * 60 * 1000):
    key = str(uuid.uuid4())
    auth = USERAUTHKEY + str(userId)
    with xtredis.pipeline() as pipe:
        while True:
            try:
                pipe.watch(auth)
                pipe.multi()
                pipe.delete(auth).hset(auth, key, token).expire(auth, maxAge)
                pipe.execute()
                break
            except WatchError:
                continue
    return key


def getToken(userId, key):
    auth = USERAUTHKEY + str(userId)
    return xtredis.hget(auth, key)


def extendToken(userId, maxAge=60 * 60 * 1000):
    auth = USERAUTHKEY + str(userId)
    xtredis.expire(auth, maxAge)

def delToken(userId, key):
    auth = USERAUTHKEY + str(userId)
    xtredis.hdel(auth, key)
