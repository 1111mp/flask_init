from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_static_digest import FlaskStaticDigest
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
# login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'

bcrypt = Bcrypt()
csrf_protect = CSRFProtect()
db = SQLAlchemy()
# https://www.jianshu.com/p/5fd8c2cbad3b
migrate = Migrate()
cors = CORS()
# https://www.abbeyok.com/archives/396
cache = Cache()
flask_static_digest = FlaskStaticDigest()
