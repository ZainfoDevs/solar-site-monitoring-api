import sqlite3

from sqlalchemy import event
from sqlalchemy.engine import Engine

from flask_migrate import Migrate
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


api = Api()
db = SQLAlchemy(model_class=Base)
migrate = Migrate()


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        original_autocommit = dbapi_connection.autocommit
        dbapi_connection.autocommit = True

        try:
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute("PRAGMA foreign_keys=ON")
            finally:
                cursor.close()
        finally:
            dbapi_connection.autocommit = original_autocommit
