# -*- coding:utf-8 -*-
from flask import Blueprint, jsonify
from app.extensions import cache
from app.utils import make_cache_key
from app.common import InvalidUsage
import time

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
def index():
    # if True:
    #     raise InvalidUsage('This view is gone', status_code=410)
    return {'time': time.time()}
