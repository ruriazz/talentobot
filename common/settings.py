from os import getenv
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


APP_DEBUG = (getenv('APP_DEBUG') or 'false').lower() == 'true'

SECRET_KEY = getenv('SECRET_KEY')

MYSQL_DSN = urlparse(getenv('MYSQL_DSN'))

DISCORD_BOT_TOKEN = getenv('DISCORD_BOT_TOKEN')
DISCORD_PERMISSION_INTEGER= 1126829767518272

TALENTO_API_URL = getenv('TALENTO_API_URL')

DEFAULT_CLOCKIN_JOB_TIME = getenv('DEFAULT_CLOCKIN_JOB_TIME')
DEFAULT_CLOCKOUT_JOB_TIME = getenv('DEFAULT_CLOCKOUT_JOB_TIME')

SECONDS_RANGE_CLOCK_IN = (300, 1500)
SECONDS_RANGE_CLOCK_OUT = (300, 900)