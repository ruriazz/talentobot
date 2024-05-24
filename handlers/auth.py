from discord.ext import commands
from discord.user import User
from discord.message import Message
from bot.application import app, bot
from libs.decorators import init_member
from libs.response import direct_reply
from libs.enums import Activity
from libs.strings import is_email_address
from libs.handlers import handle_errors
from libs.talento import Talento


@bot.command(name='auth')
@init_member
async def auth(ctx: commands.Context, author: User) -> None:
    with handle_errors():
        app.repo.create_authentication(app.repo.me(ctx))
        async with ctx.typing():
            app.repo.do_activity(ctx, Activity.AUTH_INPUT_USERNAME)
            await direct_reply(ctx, "Please input your email of talenta account")

async def input_talenta_email(ctx: Message) -> None:
    with handle_errors():
        if email := is_email_address(ctx.content):
            if auth := app.repo.get_authentication(app.repo.me(ctx)):
                auth.set_username(email) \
                    .next_step()
            app.repo.do_activity(ctx, Activity.AUTH_INPUT_PASSWORD)
            return await ctx.author.send('Please input your password of talenta account')
        
        await ctx.author.send(f"`{ctx.content}` is invalid email. Please enter the appropriate email address!")

async def input_talenta_password(ctx: Message) -> None:
    with handle_errors():
        if auth := app.repo.get_authentication(app.repo.me(ctx)):
            auth.set_password(ctx.content) \
                .next_step()
            
        auth_data = app.repo.get_authentication(app.repo.me(ctx))
        if auth_data.username and auth_data.password:
            async with ctx.author.typing():
                talento = Talento()
                result = await talento.authentication(auth.username, auth.password)
                if isinstance(result, str):
                    app.repo.do_activity(ctx, Activity.AUTH_INPUT_USERNAME)
                    return await ctx.author.send(f"Your authentication got error with message `{result}`.\nPlease re-enter your email address")

                auth_data.set_session(result.auth_token) \
                    .next_step()
                app.repo.clear_activity(ctx)

        await ctx.author.send(f'Authentication success!\nCurrently you are logged in Talenta as `{result.user.fullname}<{result.user.email}>`')