import discord
from discord.ext import commands


class EmojiPolling(commands.Cog, name='Emoji Polling'):
    """Functions for taking emoji polls"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx):
        ctx.channel.send('Poll created')


def setup(bot):
    bot.add_cog(EmojiPolling(bot))
