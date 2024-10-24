import sys
import os
import asyncio
sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

from common.settings import APP_DEBUG
from jobs import cron
from libs.handlers import handle_errors
from common.log import logging

os.environ['PYTHONASYNCIODEBUG'] = '1' if APP_DEBUG else '0'
log = logging.getLogger('cron@main')

async def main() -> sys.NoReturn:
    """Fungsi utama untuk mengatur task cron."""
    log.info("Setting up cron...")
    try:
        await cron.setup()

        log.info("Cron task is running...")
        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        log.info("Cron task is shutting down...")
        raise

async def shutdown(loop) -> None:
    """Fungsi untuk menangani shutdown dan membersihkan semua task."""
    log.info("Shutting down...")
    pending = asyncio.all_tasks(loop)

    for task in pending:
        task.cancel()

    results = await asyncio.gather(*pending, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            log.error(f"Exception during shutdown: {result}")

    loop.stop()

def custom_exception_handler(loop, context) -> None:
    """Exception handler untuk loop async."""
    if exception := context.get('exception'):
        log.error(f"An exception occurred: {exception}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_exception_handler(custom_exception_handler)

    try:
        with handle_errors():
            loop.run_until_complete(main())
    except KeyboardInterrupt:
        log.info("Received exit signal (Ctrl+C), shutting down...")
        loop.run_until_complete(shutdown(loop))
    finally:
        loop.close()
        log.info("Cron task stopped.")
