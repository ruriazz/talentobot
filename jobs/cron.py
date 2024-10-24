import importlib
import asyncio
from typing import NoReturn
import schedule
from jobs.settings import JOBS
from common.log import logging

log = logging.getLogger('cron')

def load_jobs() -> None:
    for job in JOBS:
        _job = importlib.import_module(job)
        _job.setup()
        log.info(f"{job} loaded.")

async def setup() -> NoReturn:
    load_jobs()

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)