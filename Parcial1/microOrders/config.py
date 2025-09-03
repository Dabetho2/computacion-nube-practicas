import os

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "devkey")

    # DB (sirve para correr directo o en docker)
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "root")
    DB_NAME = os.environ.get("DB_NAME", "myflaskapp")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # URL del micro de productos
    PRODUCTS_BASE = os.environ.get("PRODUCTS_BASE", "http://127.0.0.1:5003")
