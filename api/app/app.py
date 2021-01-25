# -*- coding: utf-8 -*-
import logging
import sys
import re

from flask import Flask, request, jsonify

from api.app import time, user, login
from api.app.user.models import User
from api.app.extensions import db, login_manager, cors, cache, migrate, flask_static_digest, csrf_protect
from api.app.common import InvalidUsage, ComplexEncoder, getToken, extendToken


def create_app(config_object="config"):
    app = Flask(__name__)
    print(config_object)
    app.config.from_object(config_object)
    app.json_encoder = ComplexEncoder
    register_extensions(app)
    register_blueprints(app)
    load_user(app)
    register_errorhandlers(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """给Flask注册扩展功能"""
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    cors.init_app(app, resources=r'/*', supports_credentials=True)
    migrate.init_app(app, db)
    flask_static_digest.init_app(app)
    return None


def register_blueprints(app):
    """注册蓝图"""
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(login.views.blueprint)
    app.register_blueprint(time.views.blueprint)
    return None


def load_user(app):
    # @app.after_request
    # def call_after_request_callbacks(response):
    #     """每次请求之后延长token的缓存时长"""
    #     if not re.search("/user/logout|/login|/user/register", request.path):
    #         key = str(request.headers.get('Token'))
    #         token = cache.get(key)
    #         cache.set(key, token, timeout=60 * 60)
    #     return response

    @login_manager.request_loader
    def load_user_from_request(request):
        api_key = request.headers.get('Token')
        userId = request.headers.get('UserId')
        if (api_key):
            token = getToken(userId, api_key)
            if (token):
                user = User.verify_auth_token(token)
                if user:
                    extendToken(user.id)
                    return user
        return None

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return jsonify({'code': 401, 'msg': 'Unauthorized'})

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response


def register_errorhandlers(app):
    """注册错误处理回调"""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return {'code': error_code}

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def configure_logger(app):
    """配置日志输出"""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
