import discord
import random
from discord.ext import commands

class Help(commands.Cog, name='Help'):
    """Commands related to help needed"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def question(self, ctx, *, q : str = ""):
        """ Forward a question to the officer chat
            Formats:
            !question
            !question [question to be answered]
        """
        member_name = ctx.message.author.name
        channel = self.bot.get_channel(436916990238785556)
        await channel.send("@everyone\n @"+member_name+" has a question!")
        if (q != ""):
            await channel.send("\""+q+"\"")
    

def setup(bot):
    bot.add_cog(Help(bot))
