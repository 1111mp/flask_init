from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="development")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = env.str("SECRET_KEY")
CACHE_TYPE = "redis"
CACHE_REDIS_URL = env.str("CACHE_REDIS_URL")
