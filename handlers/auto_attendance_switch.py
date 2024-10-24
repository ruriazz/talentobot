import asyncio
from discord.ext import commands
from bot.application import bot
from common.models.user import User
from common.models.user_setting import UserSetting
from libs.decorators import authenticated_talento
from libs.handlers import handle_errors, raise_error
from libs.entity import TalentaAuthData
from libs.response import direct_reply


@bot.command(name='auto')
@authenticated_talento
async def auto(ctx: commands.Context, _: TalentaAuthData, state: str = '') -> None:
    with handle_errors():
        async with ctx.typing():
            if (state or '').lower() not in ['on', 'off', 'status']:
                return await direct_reply(ctx, "Invalid parameter\nOnly use **on** / **off** / **status**", True)

            state = state.lower()
            if state == 'status':
                active = await asyncio.to_thread(is_state_on, ctx)
                return await direct_reply(
                    ctx,
                    "Your automatic attendance is now **active**. Stay on top of your schedule!" if active \
                        else "Your automatic attendance is now **inactive**. Don't forget to manage your attendance manually!",
                    True
                )
            else:
                await asyncio.to_thread(update_setitings, ctx, UserSetting.Mode(value=state))
                return await direct_reply(
                    ctx,
                    "Your automatic attendance settings have been successfully updated!",
                    True
                )

def update_setitings(ctx: commands.Context, mode: UserSetting.Mode) -> None:
    try:
        settings = (UserSetting
                    .select()
                    .join(User)
                    .where(User.uid == ctx.author.id))

        for setting in settings:
            query = (UserSetting
                    .update({UserSetting.value: mode.value})
                    .where(UserSetting.id == setting.id))
            query.execute()
    except Exception as err:
        raise_error(err)

def is_state_on(ctx: commands.Context) -> bool:
    try:
        return (UserSetting
                .select()
                .join(User)
                .where((User.uid == ctx.author.id) & (UserSetting.value == UserSetting.Mode.ON.value))
                .exists())
    except Exception as err:
        raise_error(err)