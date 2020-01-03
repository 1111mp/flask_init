# -*- coding:utf-8 -*-
from flask import Blueprint
from flask_login import login_required

blueprint = Blueprint("login", __name__, url_prefix="/login", static_folder="../static")


@blueprint.route("/")
def user_info():
    return "login"
