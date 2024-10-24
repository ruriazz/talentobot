from typing import Any, Callable, Coroutine
from discord.ext import commands
from bot.application import app
from common.models.user import User

def init_member(function) -> Callable[..., Coroutine[Any, Any, Any]]:
    async def wrapper(ctx: commands.Context, *args, **kwargs) -> Coroutine[Any, Any, Any]:
        app.repo.add_member(id=ctx.author.id, name=ctx.author.name)
        result = await function(ctx, ctx.author, *args, **kwargs)
        return result
    return wrapper

def authenticated_talento(function) -> Callable[..., Coroutine[Any, Any, Any]]:
    async def wrapper(ctx: commands.Context, *args, **kwargs) -> Coroutine[Any, Any, Any]:
        app.repo.add_member(id=ctx.author.id, name=ctx.author.name)

        if auth_data := app.repo.get_authentication(app.repo.me(ctx)):
            return await function(ctx, auth_data, *args, **kwargs)

        if user := User.get(User.uid==ctx.author.id):
            auth_data = user.AuthData
            me = app.repo.me(ctx)
            app.repo.create_authentication(me, False)
            auth = app.repo.get_authentication(me)
            auth.set_username(auth_data.username) \
                .set_password(auth_data.password) \
                .set_session(auth_data.auth_token)
            return await function(ctx, auth_data, *args, **kwargs)

        await ctx.author.send("You haven't done talenta authentication yet.\nPlease initiate authentication with command `/auth`")
    return wrapper