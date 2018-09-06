import discord
from discord.utils import get
from discord.ext import commands
import config

client = discord.Client()

class Welcome:
    '''To automatically welcome new members to the server'''

    def __init__(self, bot):
        self.bot = bot

    @client.event
    async def on_member_join(self, member):
        fmt = '''Welcome {0.mention}! \nFeel free to use \"!question\" to let us know if you have any questions \nAnd you can also use \"!help\" to find out about what you can do with our Discord bot ALBot :D '''

        for channel in member.guild.channels:
            if channel.name == 'general':
                await channel.send(fmt.format(member))


def setup(bot):
    bot.add_cog(Welcome(bot))
