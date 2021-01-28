from flask import request
from flask_socketio import ConnectionRefusedError
from api.app.extensions import socketio
from api.app.common import getToken, extendToken
from api.app.user.models import User


def init_socketio():
    """ 初始化 """

    @socketio.on('connect')
    def connect(namespace=None, query_string=None, headers=None):
        api_key = request.headers.get('token')
        userId = request.headers.get('userId')
        if (api_key):
            token = getToken(userId, api_key)
            if (token):
                user = User.verify_auth_token(token)
                if user:
                    extendToken(user.id)
                    return user
        raise ConnectionRefusedError('authentication failed')
    
    @socketio.on('invoke')
    def invoke(data):
      print(data)
