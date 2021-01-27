# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify
from flask_login import login_user
from api.app.user.models import User, UserSchema
from api.app.common import InvalidUsage, cacheToken, successReturn

blueprint = Blueprint('login', __name__, url_prefix='/login')


@blueprint.app_errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@blueprint.route('', methods=['GET', 'POST'])
def login():
    params = None
    user = None
    if request.method == 'GET':
        params = request.args
        user = User.query.filter_by(account=params.get('account')).first()
    if request.method == 'POST':
        params = request.get_json(force=True)
        user = User.query.filter_by(account=params['account']).first()

    if not user:
        raise InvalidUsage('Unknown account', status_code=401)

    if not user.check_password(params['password'] or params.get('password')):
        raise InvalidUsage('Invalid password', status_code=401)

    login_user(user)
    schema = UserSchema(exclude=['password'])

    token = user.generate_token()
    key = cacheToken(user.id, token)
    data = schema.dump(user)
    data['token'] = key

    # https://stackoverflow.com/questions/57663557/flask-how-to-change-status-code-using-jsonify-to-return-response
    # Flask: How to change status code using jsonify to return Response?
    # return make_response(jsonify(successReturn({'token': 111}, '登录成功！')), 403)
    return jsonify(successReturn(data, '登录成功！'))
