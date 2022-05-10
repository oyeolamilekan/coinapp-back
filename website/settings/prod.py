from .base import *
import dj_database_url

DEBUG = False

DATABASES = {}

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES["default"] = db_from_env
