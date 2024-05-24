import discord
import importlib
from libs.enums import Activity


async def message_received(message: discord.Message, app) -> None:
    if await in_activity(message, app):
        return

    await message.reply(f"sorry, I don't know what you mean.\n```txt\n{message.content}```", True)

async def in_activity(message: discord.Message, app) -> bool:
    if activity := app.repo.my_activity(message):
        if meth := {
            Activity.AUTH_INPUT_USERNAME: 'handlers.auth:input_talenta_email',
            Activity.AUTH_INPUT_PASSWORD: 'handlers.auth:input_talenta_password',
        }.get(activity):
            mod = importlib.import_module(meth.split(':')[0])
            await getattr(mod, meth.split(':')[1])(message)

        return True

    return False