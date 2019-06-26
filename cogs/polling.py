import asyncio
import discord
import asyncio
from discord.ext import commands

voting_emojis = ["0\u20e3", "1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3",
"5\u20e3", "6\u20e3", "7\u20e3", "8\u20e3", "9\u20e3"]

class Polling(commands.Cog, name='Voting'):
    """To allow users to vote with emojis"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx, time, title, *options):
        """[public] !poll time "title" option0 option1... option9"""

        message = "[PUBLIC POLL]\n"
        message += "__**" + title + "**__" + "\n" + "Please react to this message with your vote\n\n"
        counter = 0

        if len(options) < 1:
            await ctx.send("Not enough options. You must have at least 1 option.")
            return
        elif len(options) > 10:
            await ctx.send("Too many options. You can only have 10 options.")
            return

        for option in options:
            message += voting_emojis[counter] + " " + option + "\n" 
            counter += 1

        message = await ctx.send(message)

        for x in range(counter):
            await message.add_reaction(voting_emojis[x])

        time = int(time)
        await asyncio.sleep(time)

        await ctx.send("Here are the reactions to the message:")
        votes = message.reactions
        i = 0
        await ctx.send(len(message.reactions))
        while i < len(message.reactions):
            await ctx.send("hit")
            await ctx.send(votes[i].emoji + " " + votes[i].count)

    @commands.command()
    async def vote(self, ctx, title, *options):
        """[private] !vote "title" option0 option1... option9"""
        message = "[PRIVATE VOTE]\n"
        message += "__**" + title + "**__" + "\n" + "Please react to this message with your vote\n\n"
        counter = 0
        for option in options:
            message += voting_emojis[counter] + " " + option + "\n" 
            counter += 1      
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Polling(bot))
