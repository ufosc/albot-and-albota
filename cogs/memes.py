import asyncio
import discord
import random
import praw
from discord.ext import commands

from cogs.CONSTANTS import OFFICER_ROLE

class Memes(commands.Cog, name='Memes'):
    """All meme related commands"""
    def __init__(self, bot):
        self.bot = bot
        self.going_for_gold = False
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
    @commands.has_role(OFFICER_ROLE)
    async def randplaying(self, ctx):
        """Randomly changes the playing text"""
        new_playing = random.choice(self.playing_strings)
        await self.bot.change_presence(activity=discord.Game(name=new_playing))
        await ctx.send('I am now {}'.format(new_playing))

    @commands.command()
    @commands.has_role(OFFICER_ROLE)
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

    @commands.command()
    async def getkarma(self, ctx):
        """Makes the bot hungry for karma"""
        await ctx.send("You are enabling daily karma grabbing from /r/programmerhumor")
        self.going_for_gold = True
        await self.dailykarma()

    @commands.command()
    async def forgetkarma(self, ctx):
        """What's Reddit?"""
        await ctx.send("You are disabling daily karma grabbing from /r/programmerhumor")
        self.going_for_gold = False             
        
    async def dailykarma(self):
        """Steals the top Reddit post for the day from /r/ph"""
        channel = self.bot.get_channel(436915955348537346)
        while self.going_for_gold:
            reddit = praw.Reddit('bot1')
            for submission in reddit.subreddit('programmerhumor').hot(limit=5):
                picture_url = submission.url
                ending = picture_url[-4:]
                if ending == ".jpg":
                    comments = list(submission.comments)
                    mycomment = comments[0]
                    await channel.send(mycomment.body)
                    break
            await channel.send("I made this, give me karma")
            await channel.send(picture_url)
            await asyncio.sleep(86400)

def setup(bot):
    bot.add_cog(Memes(bot))
