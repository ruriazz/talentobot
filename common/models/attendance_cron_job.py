
from typing import Optional
import peewee as pw
from common.database import BaseModel
from datetime import datetime


class AttendanceCronJob(BaseModel):
    class Meta:
        table_name = 'attendance_cron_jobs'

    id = pw.BigAutoField(primary_key=True)
    key = pw.CharField(max_length=100, unique=True, null=False)
    event_name = pw.CharField(max_length=100, null=False)
    job_status = pw.CharField(max_length=20)
    created_at = pw.DateTimeField(default=datetime.now)
    executed_at = pw.DateTimeField(default=None, null=True)

    @staticmethod
    def Create(key: str, event_name: str) -> Optional["AttendanceCronJob"]:
        try:
            with AttendanceCronJob.Atomic():
                result = AttendanceCronJob.create(key=key, event_name=event_name)
            return result
        except Exception as err:
            AttendanceCronJob.Log().warning(f"AttendanceCronJob.Create Exception: {err}")