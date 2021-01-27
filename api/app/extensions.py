from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
# from flask_wtf.csrf import CSRFProtect
from flask_redis import FlaskRedis

login_manager = LoginManager()
# login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'

bcrypt = Bcrypt()
# csrf_protect = CSRFProtect()
db = SQLAlchemy()
# https://www.jianshu.com/p/5fd8c2cbad3b
migrate = Migrate()
cors = CORS()
# https://www.abbeyok.com/archives/396
cache = Cache()
flask_static_digest = FlaskStaticDigest()
xtredis = FlaskRedis()
# 不要使用localhost 使用127.0.0.1 因为默认会尝试走ipv6连接 造成连接时间特别长
# https://github.com/andymccurdy/redis-py/issues/740
