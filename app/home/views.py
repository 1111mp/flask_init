# -*- coding:utf-8 -*-
from flask import Blueprint
from flask_login import login_required

blueprint = Blueprint("home", __name__, static_folder="../static")


@blueprint.route("/")
def home():
    return "home"
