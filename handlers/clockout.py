import json
from discord.ext import commands
from bot.application import bot
from libs.decorators import authenticated_talento
from libs.handlers import handle_errors
from libs.entity import TalentaAuthData
from libs.talento import Talento
from libs.response import direct_reply


@bot.command(name='clockout', aliases=['clock-out', 'co'])
@authenticated_talento
async def clockout(ctx: commands.Context, auth: TalentaAuthData) -> None:
    with handle_errors():
        async with ctx.typing():
            if talento_auth := await Talento().authentication(auth.username, auth.password, True):
                talento = Talento(talento_auth.auth_token)
                ok, attendance_token = await talento.create_attendance('clock-out')
                if ok:
                    result = await talento.submit_attendance(attendance_token)
                    if isinstance(result, str):
                        return await direct_reply(ctx, f"got `{result}` error response when submitting clock-out attendance", True)
                    return await direct_reply(ctx, f"```json\n{json.dumps(result, indent=2)}\n```", True)
                return await direct_reply(ctx, f"got `{attendance_token}` error response when submitting clock-out attendance", True)

            return await direct_reply(
                ctx,
                "Your talenta authentication info is invalid. Please re-init youtr auth using `/auth` command",
                True
            )