import os

class Config:
    MYSQL_HOST = os.getenv("DB_HOST", "localhost")
    MYSQL_USER = os.getenv("DB_USER", "root")
    MYSQL_PASSWORD = os.getenv("DB_PASSWORD", "root")
    MYSQL_DB = os.getenv("DB_NAME", "myflaskapp")

    # Usa PyMySQL para SQLAlchemy; añade :3306 explícito
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
