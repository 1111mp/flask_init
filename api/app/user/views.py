# -*- coding:utf-8 -*-
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from api.app.extensions import cache
from api.app.common import InvalidUsage, cacheToken, delToken, successReturn
from api.app.user.models import User, UserSchema

blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@blueprint.route("/register", methods=["POSt"])
def register():
    """用户注册"""
    params = request.get_json(force=True)
    data = None
    try:
        user = User.create(
            account=params['account'], email=params['email'], password=params['password'])
        if user.id:
            schema = UserSchema(exclude=['password'])
            data = schema.dump(user)

            token = user.generate_token()
            key = cacheToken(user.id, token)
            data['token'] = key
    except IntegrityError:
        raise InvalidUsage(
            'account or email has been registered', status_code=400)

    return jsonify(successReturn(data, 'register successed.'))


@blueprint.route("/members", methods=["POST"])
@login_required
@cache.memoize(timeout=60)
def getUser():
    """获取用户列表"""
    users = User.query.all()
    schema = UserSchema(many=True, exclude=['password'])
    data = schema.dump(users)
    return jsonify(successReturn(data))


@blueprint.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """退出登录"""
    key = request.headers.get('Token')
    delToken(current_user.get_id(), key)
    logout_user()
    return jsonify(successReturn({}, 'You are logged out.'))
