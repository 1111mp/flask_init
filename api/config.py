from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="development")
# https://stackoverflow.com/questions/37531067/how-to-prevent-unicode-representation-for-latin1-characters
DEBUG = ENV == "development"
JSON_AS_ASCII=False
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = env.str("SECRET_KEY")
CACHE_TYPE = "redis"
CACHE_REDIS_URL = env.str("REDIS_URL")
USERAUTHKEY="user_auth"
