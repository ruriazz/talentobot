import traceback
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO,
            format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s')



@contextmanager
def handle_errors():
    try:
        yield
    except Exception as e:
        log = logging.getLogger('talentobot@handle_errors')
        traceback.print_exc()
        log.error(f"An error occurred: {e}")