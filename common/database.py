import logging
from typing import Optional, TypeVar, Generic, Type
from common.log import logging
from common.settings import MYSQL_DSN, SECRET_KEY
from libs.text_encryption import TextEncryption
from peewee import (
    MySQLDatabase,
    Model,
    DoesNotExist
)


db = MySQLDatabase(
    MYSQL_DSN.path[1:],
    user=MYSQL_DSN.username,
    password=MYSQL_DSN.password,
    host=MYSQL_DSN.hostname,
    port=MYSQL_DSN.port,
    charset='utf8mb4',
    ssl={'ca': '/etc/ssl/cert.pem'}
)

T = TypeVar('T', bound='BaseModel')

class BaseModel(Model):
    class Meta:
        database = db

    @classmethod
    def get(cls, *query, **filters) -> Optional["User"]:
        try:
            return super().get(*query, **filters)
        except DoesNotExist:
            pass
        except Exception as err:
            cls.Log().warning(f"User.get Exception: {err}")

    @classmethod
    def get(cls: Type[T], *query, **filters) -> Optional[T]:
        try:
            return super().get(*query, **filters)
        except DoesNotExist:
            pass
        except Exception as err:
            cls.Log().warning(f"{cls.__qualname__}.get Exception: {err}")

    @classmethod
    def TextEncryption(cls, secret_key: str = '') -> TextEncryption:
        return TextEncryption(f"{cls.__module__}.{cls.__qualname__}{SECRET_KEY}{secret_key or ''}")

    @classmethod
    def Log(cls) -> logging.Logger:
        return logging.getLogger(f"{cls.__qualname__}@Model")

    @classmethod
    def Atomic(cls) -> MySQLDatabase:
        return BaseModel._meta.database.atomic()