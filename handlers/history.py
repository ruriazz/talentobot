from discord.ext import commands
from bot.application import bot
from libs.decorators import authenticated_talento
from libs.handlers import handle_errors
from libs.entity import TalentaAuthData
from libs.talento import Talento
from libs.response import direct_reply
from libs.strings import format_message_history


@bot.command(name='history')
@authenticated_talento
async def history(ctx: commands.Context, auth: TalentaAuthData) -> None:
    with handle_errors():
        async with ctx.typing():
            if talento_auth := await Talento().authentication(auth.username, auth.password, True):
                results = await Talento(talento_auth.auth_token).get_histories()
                histories = ''.join(
                    format_message_history(
                        m['checkTime'],
                        m['checkType'],
                        m['locationCoordinate'],
                        m['locationName'],
                    )
                    for m in results
                )
                return await direct_reply(ctx, histories or 'No attendance history data', True)
        await direct_reply(ctx, 'No attendance history data', True)