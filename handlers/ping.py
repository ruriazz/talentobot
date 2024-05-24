from discord.ext import commands
from bot.application import app, bot
from libs.response import direct_reply


@bot.hybrid_command()
async def ping(ctx: commands.Context) -> None:
    app.repo.add_member(id=ctx.author.id, name=ctx.author.name)
    await direct_reply(ctx, "pong!", True)