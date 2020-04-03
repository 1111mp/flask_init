# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from app.user.models import User
from app.common import InvalidUsage, successReturn
from app.extensions import csrf_protect

blueprint = Blueprint('logon', __name__, url_prefix='/login')


@blueprint.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@blueprint.route('/', methods=['POST'])
@csrf_protect.exempt
def login():
    data = request.get_json(force=True)
    user = User.query.filter_by(username=data['username']).first()

    if not user:
        raise jsonify(InvalidUsage('Unknown username', status_code=400))

    if not user.check_password(data['password']):
        raise jsonify(InvalidUsage('Invalid password', status_code=400))

    token = user.generate_token()
    return jsonify(successReturn({'token': token}, '登录成功！'))
