import discord
from discord.ext import commands
import os

class HelloWorld:
    '''Discord.py Cog for printing the hello world code for different languages'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, lang : str):
        '''Prints the hello world source for any language defined in cogs/helloworld'''
        for fName in os.listdir("cogs/helloworld"):
            if fName.startswith(lang.lower()):
                with open("cogs/helloworld/{}".format(fName), 'r') as f:
                    await self.bot.say(f.read())

def setup(bot):
    bot.add_cog(HelloWorld(bot))
