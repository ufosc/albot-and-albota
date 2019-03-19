import discord
import random
from discord.ext import commands

import cogs.util

class Memes(commands.Cog, name='Memes'):
    """All meme related commands"""
    def __init__(self, bot):
        self.bot = bot
        self.playing_strings = []
        with open('cogs/playing_strings.txt', 'r') as f:
            self.playing_strings = f.read().splitlines()

    @commands.command()
    async def orange(self, ctx):
        """Responds to the classic football chant "Orange" "Blue"""
        await ctx.send("BLUE!")

    @commands.command()
    async def blue(self, ctx):
        """Responds to the classic football chant "Orange" "Blue"""
        await ctx.send("ORANGE!")

    @commands.command()
    async def about(self, ctx):
        """Prints information about the bots."""
        await ctx.send("We are your benevolent dictators. Fear us.")
        await ctx.send(file=discord.File('alligator.jpg'))

    @commands.command()
    @commands.check(cogs.util.is_officer_check)
    async def randplaying(self, ctx):
        """Randomly changes the playing text"""
        new_playing = random.choice(self.playing_strings)
        await self.bot.change_presence(activity=discord.Game(name=new_playing))
        await ctx.send('I am now {}'.format(new_playing))

    @commands.command()
    @commands.check(cogs.util.is_officer_check)
    async def setplaying(self, ctx, *, playing: str):
        """Lets an officer set the playing text"""
        await self.bot.change_presence(activity=discord.Game(name=playing))

    @commands.command()
    async def say(self, ctx, *, phrase : str):
        """Has the bot say something"""
        await ctx.send(phrase)

    async def on_guild_channel_create(self, channel):
        """Messages "First" when a channel is created"""
        await channel.send('First')

def setup(bot):
    bot.add_cog(Memes(bot))
