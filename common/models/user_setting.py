from enum import Enum
import peewee as pw
from common.database import BaseModel
from common.models.user import User


class UserSetting(BaseModel):
    class Meta:
        table_name = 'user_settings'

    id = pw.BigAutoField(primary_key=True)
    user = pw.ForeignKeyField(model=User, backref='settings', on_delete='CASCADE')
    name = pw.CharField(max_length=100)
    value = pw.TextField()

    AUTO_CLOCK_IN = 'AutoClockIn'
    AUTO_CLOCK_OUT = 'AutoClockOut'

    class Mode(Enum):
        ON = 'on'
        OFF = 'off'

    @staticmethod
    def init_settings(user: User) -> None:
        cls = UserSetting
        with UserSetting.Atomic():
            UserSetting.insert([
                dict(user=user, name=cls.AUTO_CLOCK_IN, value=cls.Mode.OFF.value),
                dict(user=user, name=cls.AUTO_CLOCK_OUT, value=cls.Mode.OFF.value)
            ]).execute()