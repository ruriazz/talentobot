import sys
import os
import logging
import asyncio

sys.path.append(
    os.path.dirname(os.path.dirname(__file__))
)

from common.settings import APP_DEBUG
from bot.application import app
from libs.handlers import handle_errors
from common.log import logging

os.environ['PYTHONASYNCIODEBUG'] = '1' if APP_DEBUG else '0'
log = logging.getLogger('talentobot@main')

async def main():
    """Fungsi utama bot yang mengatur konfigurasi dan eksekusi aplikasi."""
    log.info("Setting up bot...")

    try:
        await app.configure()
        log.info("Bot is running...")

        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        log.info("Bot is shutting down...")
        raise

async def shutdown(loop):
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

def custom_exception_handler(loop, context):
    """Exception handler untuk loop async."""
    exception = context.get('exception')
    if exception:
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
        log.info("Bot stopped.")
