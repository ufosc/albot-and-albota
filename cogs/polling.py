import asyncio
import discord
import asyncio
from discord.ext import commands

voting_emojis = ["0\u20e3", "1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3",
"5\u20e3", "6\u20e3", "7\u20e3", "8\u20e3", "9\u20e3"]

class Polling(commands.Cog, name='Polling'):
    """To allow users to vote with emojis"""
    def __init__(self, bot):
        self.bot = bot

    async def determinewinner(self, ctx, poll):
        """Who won the poll?"""
        poll = await ctx.channel.fetch_message(poll.id)
        occurences = []
        highest = 0

        for reaction in poll.reactions:
            if reaction.count - 1 > highest:
                highest = reaction.count - 1
                occurences = [reaction.emoji]
            elif reaction.count - 1 == highest:
                occurences.append(reaction.emoji)

        if len(occurences) > 1:
            message = "The winners are: "
            for occurence in occurences:
                message += occurence + " "
            await ctx.send(message)
        else:
            await ctx.send("The winner is " + occurences[0])


    #Absolute free for all poll
    @commands.command()
    async def simplepoll(self, ctx, title, *options):
        """[public] !simplepoll "title" option0 option1... option9"""

        if len(options) < 1:
            await ctx.send("Not enough options. You must have at least 1 option.")
            return
        elif len(options) > 10:
            await ctx.send("Too many options. You can only have 10 options.")
            return

        message = "[UNLIMITED VOTING]\n"
        message += "__**" + title + "**__" + "\n" + "Please react to this message with your vote\n\n"
        counter = 0

        for option in options:
            message += voting_emojis[counter] + " " + option + "\n" 
            counter += 1

        message = await ctx.send(message)

        for x in range(counter):
            await message.add_reaction(voting_emojis[x])

    #Timed poll that will automatically declare a winner
    @commands.command()
    async def timepoll(self, ctx, time, title, *options):
        """[public] !timepoll time (in minutes) "title" option0 option1... option9"""

        #Input validation
        if time.isdigit() is False:
            await ctx.send("Time is not an int specifying time in minutes! Please reformat!")
            return
        elif int(time) < 1:
            await ctx.send("Time must be at least 1 minute! Please reformat!")
            return
        elif len(options) < 1:
            await ctx.send("Not enough options. You must have at least 1 option.")
            return
        elif len(options) > 10:
            await ctx.send("Too many options. You can only have 10 options.")
            return

        #Convert time to minutes
        time *= 60 #comment out this line for testing

        #Currently not enforcced
        message = "[ONE VOTE]\n"
        message += "__**" + title + "**__" + "\n" + "Please react to this message with your vote\n\n"
        counter = 0

        for option in options:
            message += voting_emojis[counter] + " " + option + "\n" 
            counter += 1

        message = await ctx.send(message)

        for x in range(counter):
            await message.add_reaction(voting_emojis[x])

        await asyncio.sleep(int(time))

        await self.determinewinner(ctx, message)

def setup(bot):
    bot.add_cog(Polling(bot))
