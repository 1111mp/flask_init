# -*- coding:utf-8 -*-
import json
from flask import Blueprint, request, jsonify
from flask_login import login_required, logout_user
from sqlalchemy.exc import IntegrityError

from api.app.extensions import cache, csrf_protect
from api.app.common import InvalidUsage, cacheToken, successReturn
from api.app.user.models import User

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
    params = request.get_json(force=True)
    data = None
    try:
        user = User.create(
            account=params['account'], email=params['email'], password=params['password'])
        if user.id:
            data = user.to_json()
            token = user.generate_token()
            key = cacheToken(user.id, token)
            data['token'] = key
    except IntegrityError:
        raise InvalidUsage(
            'account or email has been registered', status_code=400)

    return jsonify(successReturn(data, 'register successed.'))


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
    return jsonify(successReturn(users_output))


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
