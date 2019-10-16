import discord
from discord.ext import commands

from database.database import SQLCursor, SQLConnection

class Tally(commands.Cog, name="Tally"):
    ''' All functionality related to the goodbot/badbot tally'''

    votes = ["good", "bad"]

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        self.good = 0
        self.bad = 0

    @commands.command()
    async def goodbot(self, ctx):
        ''' Tells the bot he's a good bot! '''
        self.vote(True)
        await ctx.send("Thanks!")

    @commands.command()
    async def badbot(self, ctx):
        ''' Tells the bot he's a bad bot! '''
        self.vote(False)
        await ctx.send("Oof")

    def vote(self, good):
        ''' Votes goodbot if good is true, badbot if good is false '''
        vote = "good" if good else "bad"
        with SQLCursor(self.db) as cur:
            cur.execute("SELECT vote, tally FROM goodbot_badbot WHERE vote=?",(vote,))
            row = cur.fetchone()
            new_tally = row[1] + 1
            cur.execute("UPDATE goodbot_badbot SET tally=? WHERE vote=?",(new_tally,vote))

    @commands.command()
    async def tally(self, ctx):
        ''' Get the current goodbot/badbot tally '''
        with SQLCursor(self.db) as cur:
            cur.execute("SELECT vote, tally FROM goodbot_badbot")
            row = cur.fetchone()
            await ctx.send("{0}: {1}".format(str(row[0]),str(row[1])))
            row = cur.fetchone()
            await ctx.send("{0}: {1}".format(str(row[0]),str(row[1])))

def initialize():
    ''' Initializes the table with non-null 'vote' positions '''
    sql_db = SQLConnection()
    with SQLCursor(sql_db) as cur:
        cur.execute("SELECT vote from goodbot_badbot")
        row = cur.fetchone()
        for vote in Tally.votes:
            if row is None or len(row) != len(Tally.votes):
                cur.execute("INSERT OR IGNORE INTO goodbot_badbot VALUES (?, ?)", (vote, 0))

def setup(bot):
    bot.add_cog(Tally(bot,SQLConnection()))
    initialize()


        