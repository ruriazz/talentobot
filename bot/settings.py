from os import getenv

APP_DEBUG = (getenv('APP_DEBUG') or 'false').lower() == 'true'

DISCORD_BOT_TOKEN = getenv('DISCORD_BOT_TOKEN')
TALENTO_API_URL = getenv('TALENTO_API_URL') or 'https://api.talento.ruriazz.com'

COMMANDS = [
    'handlers.auth',
    'handlers.clockin',
    'handlers.clockout',
    'handlers.history',
    'handlers.ping',
]