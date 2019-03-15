import discord
from discord.ext import commands
import os

class HelloWorld(commands.Cog, name='Hello World'):
    """Discord.py Cog for printing the hello world code for different languages"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx, lang : str):
        """Prints the hello world source for any language defined in cogs/helloworld"""
        for fName in os.listdir("cogs/helloworld"):
            if fName == (lang.lower() + ".txt"):
                with open("cogs/helloworld/{}".format(fName), 'r') as f:
                    await ctx.send(f.read())

    @commands.command()
    async def hellolangs(self, ctx):
        """Prints all the languages that there are helloworld's for"""
        langs = ''
        for fName in os.listdir("cogs/helloworld"):
            langs += fName.replace('.txt','') + '\n'
        await ctx.send(langs)

def setup(bot):
    bot.add_cog(HelloWorld(bot))
