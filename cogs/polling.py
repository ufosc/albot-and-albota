import asyncio
import discord
import asyncio
from discord.ext import commands

from database.database import SQLCursor, SQLConnection

voting_emojis = ["0\u20e3", "1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3",
"5\u20e3", "6\u20e3", "7\u20e3", "8\u20e3", "9\u20e3"]

class Polling(commands.Cog, name='Polling'):
    """To allow users to vote with emojis"""
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command()
    async def createpoll(self, ctx, title, *options):
        """[public] !poll "title" option0 option1... option9"""

        if len(options) < 1:
            await ctx.send("Not enough options. You must have at least 1 option.")
            return
        elif len(options) > 10:
            await ctx.send("Too many options. You can only have 10 options.")
            return

        message = "[PUBLIC POLL]\n"
        message += "__**" + title + "**__" + "\n" + "Please react to this message with your vote\n\n"
        counter = 0

        for option in options:
            message += voting_emojis[counter] + " " + option + "\n" 
            counter += 1

        message = await ctx.send(message)

        with SQLCursor(self.db) as cursor:
            """Insert the poll info the db"""
            cursor.execute('INSERT INTO poll_info (poll_title, message_id, channel_id, user_id, results) VALUES (?, ?, ?, ?, ?);',
            (title, message.id, message.channel, ctx.author, "Pending"))

        for x in range(counter):
            await message.add_reaction(voting_emojis[x])

def setup(bot):
    bot.add_cog(Polling(bot, SQLConnection()))
