# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify, Response
import json
from flask_login import login_required, logout_user
from app.extensions import cache, csrf_protect
from app.common import InvalidUsage, successReturn, ComplexEncoder
from app.user.models import User
from app.database import db

blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@csrf_protect.exempt
@blueprint.route("/register", methods=["POSt"])
def register():
    """用户注册"""
    data = request.get_json(force=True)
    print(data)
    user = User.create(
        username=data['username'], email=data['email'], password=data['password'])
    # db.session.add(user)
    # db.session.commit()
    return jsonify(successReturn({}, 'register successed.'))


@blueprint.route("/members", methods=["POST"])
@csrf_protect.exempt
@login_required
@cache.memoize(timeout=5)
def getUser():
    """获取用户列表"""
    users = User.query.all()
    users_output = []
    for user in users:
        users_output.append(user.to_json())
    return Response(json.dumps(successReturn({'items': users_output}, ''), cls=ComplexEncoder), mimetype='application/json')


@blueprint.route("/logout", methods=["GET", "POST"])
@csrf_protect.exempt
@login_required
def logout():
    """退出登录"""
    key = request.headers.get('Token')
    print(key)
    logout_user()
    cache.delete(key)
    return jsonify(successReturn({}, 'You are logged out.'))
