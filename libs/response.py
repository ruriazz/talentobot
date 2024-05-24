from discord.ext import commands
from discord.channel import DMChannel

async def direct_reply(ctx: commands.Context, content: str, reply_content: bool = False) -> None:
    if not isinstance(ctx.message.channel, DMChannel) or not reply_content:
        return await ctx.author.send(content)

    return await ctx.message.reply(content)