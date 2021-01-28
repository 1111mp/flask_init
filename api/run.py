# -*- coding: utf-8 -*-
"""Create an application instance."""

from api.app.app import create_app
from api.app.extensions import socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, port=5000)
