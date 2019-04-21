import discord
from discord.ext import commands

import cogs.CONSTANTS as CONSTANTS
from database.database import SQLCursor, SQLConnection

class ALBotMessageDeletionHandlers(commands.Cog, name='Message Deletion Handlers'):
    """ Functions for handling tracked messages """
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """ Checks reactions and deletes tracked messages when necessary. """
        if payload.user_id == self.bot.user.id:
            return
        if payload.emoji.name == CONSTANTS.REACTION_DELETE:
            is_tracked = False
            sender_uid = None
            with SQLCursor(self.db) as cur:
                cur.execute("SELECT messid, sender_uid FROM tracked_messages WHERE messid=?", (payload.message_id,))
                row = cur.fetchone()
                if row:
                    is_tracked = True
                    sender_uid = row[1]

            if is_tracked:
                reacting_member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
                can_delete = self.bot.get_channel(payload.channel_id).permissions_for(reacting_member).manage_messages
                if payload.user_id == sender_uid or can_delete:
                    relevant_message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    await relevant_message.delete()

async def track(message, author=None):
    """ Marks a message in the database so that it will be automatically
        deleted if the sender or an admin reacts with the 'trash' emoji
    """
    await message.add_reaction(CONSTANTS.REACTION_DELETE)
    sql_db = SQLConnection()
    aid = 0
    if author:
        aid = author.id
    with SQLCursor(sql_db) as cur:
                cur.execute("INSERT INTO tracked_messages (messid, sender_uid, track_time) VALUES (?, ?, ?);", (message.id, aid, message.created_at))

class ALBotFactorialHandler(commands.Cog, name='Factorial Handler'):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        """Checks message for factorial format using regex."""
        if msg.author != self.bot.user:
            import re
            filtered_msg = re.findall('{(?:[0-9]|[1-8](?:[0-9]{1,2})?)!}', msg.content)
            if filtered_msg is not None:
                group_len = len(filtered_msg)
                factorial = 'Factorial: `{}! = {}`' if group_len == 1 else 'The following factorials were calculated as:```'
                import math
                if group_len > 1:
                    for i in range(0, group_len):
                        num = int((filtered_msg[i].split('!')[0])[1:])
                        product = math.factorial(num)
                        factorial += '\n\n{}! = {}'.format(num, product)
                    await msg.channel.send(factorial + '```')
                elif group_len == 1:
                    try:
                        num = int((filtered_msg[0].split('!')[0])[1:])
                        await msg.channel.send(factorial.format(num, math.factorial(num)))
                    except discord.HTTPException as e:
                        await msg.channel.send('Cannot post answer due to excessive character count! Maximum factorial allowed is `801!`.')
def setup(bot):
    bot.add_cog(ALBotMessageDeletionHandlers(bot, SQLConnection()))
