import json
from enum import Enum

import requests
from discord.ext import commands

from config import BACKEND_KEY
from utils import userutil
from utils import validation


class Events(commands.Cog, name="Events"):
    def __init__(self, bot):
        self.bot = bot

    # modify this uri for testing, typically localhost
    API_ENDPOINT = "https://opensource.club/api/events/"

    class RequestType(Enum):
        EVENT_CREATE = 'createEvent',
        EVENT_SIGNIN = 'eventSignin',

        def get_permission_required(self):
            if self == self.EVENT_CREATE:
                return userutil.Permission.EVENT_CREATE
            elif self == self.EVENT_SIGNIN:
                return userutil.Permission.EVENT_SIGNIN

    def construct_uri(self, request_type: RequestType, **kwargs):
        """Returns a properly formatted URI for making HTTP requests."""
        return f'{self.baseUri}{request_type.value}'

    @commands.group(invoke_without_command=True, name="event")
    @commands.guild_only()
    async def event(self, ctx):
        await ctx.message.author.send(userutil.Permission.get_user_descriptions(ctx.message.author))

    @event.group(invoke_wihtout_command=True)
    @commands.guild_only()
    async def create(self, ctx, eventcode=None, eventname=None, starttime=None, endtime=None, desc='No description.'):
        if userutil.is_officer(ctx.message.author):
            data = {
                'api_key': BACKEND_KEY,
                'eventcode': eventcode,
                'eventname': eventname,
                'starttime': starttime,
                'endtime': endtime,
                'desc': desc
            }
            if validation.validate_post_body(data):
                endpoint_create = f'{self.API_ENDPOINT}{self.RequestType.EVENT_CREATE.value}'
                res = requests.post(url=endpoint_create, data=data)
                res_data = res.json()
                ctx.message.author.send(json.dumps(res_data))


def setup(bot):
    bot.add_cog(Events(bot))
