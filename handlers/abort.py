import pytz
import hashlib
from typing import Literal
from datetime import datetime
from discord.ext import commands
from bot.application import bot
from common.models.user import User
from common.models.user_setting import UserSetting
from common.models.attendance_cron_job import AttendanceCronJob
from libs.decorators import authenticated_talento
from libs.enums import AttendanceJobStatus
from libs.handlers import handle_errors, raise_error
from libs.entity import TalentaAuthData
from libs.response import direct_reply


@bot.command(name='abort')
@authenticated_talento
async def abort(ctx: commands.Context, _: TalentaAuthData) -> None:
    with handle_errors():
        async with ctx.typing():
            if _ := abort_all(ctx):
                return await direct_reply(ctx, "All scheduled jobs have been successfully **canceled!**", True)

def abort_all(ctx) -> None | Literal[True]:
    try:
        if keys := get_keys(ctx):
            print('keys', keys)
            with AttendanceCronJob.Atomic():
                (AttendanceCronJob
                .update(job_status=AttendanceJobStatus.CANCEL.value)
                .where(AttendanceCronJob.key.in_(keys))
                .execute())

            return True
    except Exception as err:
        raise_error(err)

def get_keys(ctx: commands.Context) -> list[str]:
    tz = pytz.timezone('Asia/Jakarta')
    if user := User.get(User.uid==ctx.author.id):
        now = datetime.now(tz=tz)
        return [
            (hashlib
             .sha1(f"{now.strftime('%Y%m%d')}_{UserSetting.AUTO_CLOCK_OUT}_{user.id}".encode())
             .hexdigest()),
            (hashlib
             .sha1(f"{now.strftime('%Y%m%d')}_{UserSetting.AUTO_CLOCK_IN}_{user.id}".encode())
             .hexdigest()),
        ]
    return []