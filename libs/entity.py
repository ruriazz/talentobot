import discord
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union
from libs.enums import TalentaAuthStep, Activity
from discord.ext import commands


class DiscordMember(BaseModel):
    id: int
    name: str


class TalentaAuthData(BaseModel):
    username: Optional[str]         = Field(init=False, default=None)
    password: Optional[str]         = Field(init=False, default=None)
    auth_token: Optional[str]       = Field(init=False, default=None)
    steps: List[TalentaAuthStep]    = Field(init=False, default=[])

    def set_username(self, val: str) -> "TalentaAuthData":
        self.username = val
        return self

    def set_password(self, val: str) -> "TalentaAuthData":
        self.password = val
        return self

    def set_session(self, val: str) -> "TalentaAuthData":
        self.auth_token = val
        return self

    def next_step(self) -> "TalentaAuthData":
        vals = sorted([i.value for i in self.steps])
        if not vals or vals[-1] == TalentaAuthStep.AUTHENTICATED.value:
            return self

        vals.append(vals[-1]+1)
        self.steps = [TalentaAuthStep.from_value(i) for i in vals]
        return self

    def step_complete(self) -> bool:
        return bool(self.steps and self.steps[-1] == TalentaAuthStep.AUTHENTICATED)


class Repository(BaseModel):
    members: Dict[int, DiscordMember]           = {}
    authentication: Dict[int, TalentaAuthData]  = {}
    activity: Dict[int, Activity]               = {}

    def add_member(self, **kwargs) -> "Repository":
        if not self.members.get(kwargs['id']):
            self.members[kwargs['id']] = DiscordMember(**kwargs)
        return self

    def create_authentication(self, user: DiscordMember) -> "Repository":
        self.authentication[user.id] = self.authentication.get(user.id) or TalentaAuthData()
        self.authentication[user.id].steps = [TalentaAuthStep.INIT]
        return self

    def me(self, ctx: commands.Context) -> DiscordMember:
        return self.members[ctx.author.id]

    def get_authentication(self, user: DiscordMember) -> Optional[TalentaAuthData]:
        return self.authentication.get(user.id)
    
    def my_activity(self, ctx: Union[commands.Context, discord.Message]) -> Optional[Activity]:
        user = self.members[ctx.author.id]
        return self.activity.get(user.id)
    
    def do_activity(self, ctx: Union[commands.Context, discord.Message], activity: Activity) -> "Repository":
        user = self.members[ctx.author.id]
        self.activity[user.id] = activity
        return self
    
    def clear_activity(self, ctx: Union[commands.Context, discord.Message]) -> "Repository":
        user = self.members[ctx.author.id]
        del self.activity[user.id]
        return self