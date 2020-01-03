# -*- coding: utf-8 -*-
import logging
import sys

from flask import Flask, render_template

from app import user, public
from app.extensions import db, login_manager, cors, cache, migrate, flask_static_digest, csrf_protect


def create_app(config_object="config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
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
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """注册错误处理回调"""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def configure_logger(app):
    """配置日志输出"""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
