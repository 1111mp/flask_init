# -*- coding:utf-8 -*-
from flask import Blueprint
import time

blueprint = Blueprint("time", __name__, url_prefix="/time",
                      static_folder="../static")


@blueprint.route("/")
def index():
    return {'time': time.time()}
