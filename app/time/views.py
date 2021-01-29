# -*- coding:utf-8 -*-
import time
from flask import Blueprint, jsonify
from app.common import InvalidUsage
# from flask_login import login_required
from app.extensions import cache
from proto.message_pb2 import Message

blueprint = Blueprint("time", __name__, url_prefix="/time",
                      static_folder="../static")

# https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/


@blueprint.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# https://www.abbeyok.com/archives/396


@blueprint.route("/")
@cache.memoize(timeout=5)
# @login_required
def index():
    # proto = Message()
    # proto.name = 'sdasdas'
    # proto.age = 24
    # print(proto)
    # buf = proto.SerializeToString()
    # print(buf)
    
    # hw = Message()
    # hw.ParseFromString(buf)
    # print(hw.name)
    # print(hw.age)

    return {'time': time.time()}
