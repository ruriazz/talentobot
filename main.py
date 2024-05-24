import logging
import os
import asyncio
os.path.abspath(__file__)

from bot.settings import APP_DEBUG
from bot.application import app
from libs.handlers import handle_errors

os.environ['PYTHONASYNCIODEBUG'] = '1' if APP_DEBUG else '0'

logging.basicConfig(level=logging.INFO,
            format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
log = logging.getLogger('talentobot@main')

def custom_exception_handler(loop, context):
    if exception := context.get('exception'):
        log.error(f"An exception occurred: {exception}")

if __name__ == '__main__':
    log.info("Setting up bot..")
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(custom_exception_handler)

    with handle_errors():
        loop.run_until_complete(app.configure())