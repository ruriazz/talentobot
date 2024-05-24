import pytz
from datetime import datetime
from discord.ext import commands
from bot.application import bot
from libs.decorators import authenticated_talento
from libs.handlers import handle_errors
from libs.entity import TalentaAuthData
from libs.talento import Talento
from libs.response import direct_reply


@bot.command(name='history')
@authenticated_talento
async def history(ctx: commands.Context, auth: TalentaAuthData) -> None:
    with handle_errors():
        async with ctx.typing():
            if talento_auth := await Talento().authentication(auth.username, auth.password, True):
                results = await Talento(talento_auth.auth_token).get_histories()
                histories = ''
                for m in results:
                    check_time = datetime.strptime(m['checkTime'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.timezone('Asia/Jakarta'))
                    check_type = 'Clock-in' if m['checkType'] == 'checkin' else 'Clock-out'
                    histories += f'### {check_type} [{check_time.strftime("%d-%m-%Y %H:%M")}]\nCoordinate: **{m["locationCoordinate"]}**\nLocation: **{m["locationName"]}**\n\n'
                return await direct_reply(ctx, histories or 'No attendance history data', True)

        await direct_reply(ctx, 'No attendance history data', True)