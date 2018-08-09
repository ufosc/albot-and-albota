import discord
from discord.ext import commands

class Memes:
    '''All meme related commands'''
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def orange(self, ctx):
        '''Responds to the classic football chant "Orange" "Blue"'''
        await ctx.send("BLUE!")
    
    @commands.command()
    async def blue(self, ctx):
        '''Responds to the classic football chant "Orange" "Blue"'''
        await ctx.send("ORANGE!")

    @commands.command()
    async def about(self, ctx):
        '''Prints information about the bots.'''
        await ctx.send("We are your benevolent dictators. Fear us.")
        await ctx.send(file=discord.File('alligator.jpg'))

def setup(bot):
    bot.add_cog(Memes(bot))
