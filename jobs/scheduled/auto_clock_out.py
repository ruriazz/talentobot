import schedule
import contextlib
import pytz
import random
import hashlib
from peewee import IntegrityError
from datetime import datetime, timedelta
from threading import Timer
from common.models.user import User
from common.models.user_setting import UserSetting
from common.models.attendance_cron_job import AttendanceCronJob
from libs.enums import AttendanceJobStatus
from libs.strings import format_message_history
from libs.notification import send_discord_message
from libs.talento import Talento
from common.log import logging
from libs.times import is_weekday_in_indonesia
from common.settings import DEFAULT_CLOCKOUT_JOB_TIME, SECONDS_RANGE_CLOCK_OUT


log = logging.getLogger('auto-clock-out@jobs')
tz = pytz.timezone('Asia/Jakarta')

def setup() -> None:
    def setup_clockout_job() -> None:
        users = (User
                .select(User)
                .join(UserSetting)
                .where(
                    (UserSetting.name == UserSetting.AUTO_CLOCK_OUT) & (UserSetting.value == UserSetting.Mode.ON.value))
                )

        init_data = [
            dict(key=create_key(user), event_name=UserSetting.AUTO_CLOCK_OUT, uid=user.uid)
            for user in users
        ]

        with contextlib.suppress(IntegrityError):
            with AttendanceCronJob.Atomic():
                (AttendanceCronJob
                .insert([{k: v for k, v in data.items() if k != 'uid'} for data in init_data])
                .execute())

        for data in init_data:
            if _ := (AttendanceCronJob
             .select(AttendanceCronJob.id)
             .where(AttendanceCronJob.key==data['key'])
             .exists()):
                random_seconds = random.uniform(*SECONDS_RANGE_CLOCK_OUT)
                log.info(f"Sleep {random_seconds} seconds for execute job {data['key']}")
                excecute_time = datetime.now(tz=tz) + timedelta(seconds=random_seconds)
                notification = (f"📣 Talento will auto **clock-out** at **{excecute_time.strftime('%H:%M:%S')} WIB**.\n"
                                f"You can **cancel** it by sending `/abort` command.")
                Timer(random_seconds, submit, args=[data['key'], data['uid']]).start()
                send_discord_message(data['uid'], notification)

    def create_key(user: User) -> str:
        now = datetime.now(tz=tz)
        return hashlib.sha1(f"{now.strftime('%Y%m%d')}_{UserSetting.AUTO_CLOCK_OUT}_{user.id}".encode()).hexdigest()

    def submit(job_key: str, uid: int) -> None:
        if not (_ := (AttendanceCronJob
                      .select(AttendanceCronJob.id)
                      .where((AttendanceCronJob.key==job_key) & (AttendanceCronJob.job_status==AttendanceJobStatus.PENDING.value))
                      .exists())):
            return

        user = User.get(uid=uid)
        lib = Talento(user.AuthData.auth_token)
        if [i for i in (lib.sync_get_histories() or []) if i['checkType'] == 'checkout']:
            # TODO: Cancel Job if already clock-out before
            return (AttendanceCronJob
            .update(
                job_status=AttendanceJobStatus.CANCEL.value,
                executed_at=datetime.now(tz=tz)
            )
            .where(AttendanceCronJob.key==job_key)
            .execute())


        # TODO: Submit attendance
        created, result = lib.sync_create_attendance('clock-out')
        if created:
            submited, result = lib.sync_submit_attendance(result)
            if submited:
                # TODO: Send Notification to user discord
                data = result['data']
                message = format_message_history(data['clock_time'], 'checkout', data['coordinate'], data['location_address'])
                send_discord_message(uid, message)

                # TODO: Set Cron Job Status to SUCCESS
                return (AttendanceCronJob
                .update(
                    job_status=AttendanceJobStatus.SUCCESS.value,
                    executed_at=datetime.now(tz=tz)
                    )
                .where(AttendanceCronJob.key==job_key)
                .execute())

        send_discord_message(uid, f"Talento **failed** to submit attendance. Error: **'{result}'**.")
        return (AttendanceCronJob
                .update(
                    job_status=AttendanceJobStatus.FAILED.value,
                    executed_at=datetime.now(tz=pytz.timezone('Asia/Jakarta'))
                )
                .where(AttendanceCronJob.key==job_key)
                .execute())

    (schedule
     .every()
     .day
     .at(time_str=DEFAULT_CLOCKOUT_JOB_TIME, tz='Asia/Jakarta')
     .do(lambda: setup_clockout_job() if is_weekday_in_indonesia() else None))