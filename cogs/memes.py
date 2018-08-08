import discord
from discord.ext import commands

class Memes:
    '''All meme related commands'''
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def orange(self):
        '''Responds to the classic football chant "Orange" "Blue"'''
        await self.bot.say("BLUE!")
    
    @commands.command()
    async def blue(self):
        '''Responds to the classic football chant "Orange" "Blue"'''
        await self.bot.say("ORANGE!")

    @commands.command(pass_context=True)
    async def about(self, ctx):
        '''Prints information about the bots.'''
        await self.bot.say("We are your benevolent dictators. Fear us.")
        with open('alligator.jpg', 'rb') as f:
            await self.bot.send_file(ctx.message.channel, f)


def setup(bot):
    bot.add_cog(Memes(bot))
