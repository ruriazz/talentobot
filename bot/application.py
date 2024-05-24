import importlib
import discord
import logging
from discord.ext import commands
from bot.settings import COMMANDS
from bot.settings import DISCORD_BOT_TOKEN
from libs.entity import Repository
from handlers.message_received import message_received


bot = commands.Bot(command_prefix='/', intents=discord.Intents.default())

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(name)s][%(levelname)s] %(message)s')

class Application:
    repo: Repository
    log: logging = logging.getLogger('talentobot@application')

    async def configure(self):
        self._load_commands()
        self.repo = Repository()

        await bot.start(token=DISCORD_BOT_TOKEN)

    async def close(self):
        await bot.close()

    def _load_commands(self):
        for command in COMMANDS:
            importlib.import_module(command)

@bot.event
async def on_ready():
    app.log.info(f'Logged in as {bot.user.name}@{bot.user.id}')


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
    else:
        app.repo.add_member(id=message.author.id, name=message.author.name)
        await message_received(message, app)


app = Application()