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
                    relevant_message = await self.bot.get_channel(payload.channel_id).get_message(payload.message_id)
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


def setup(bot):
    bot.add_cog(ALBotMessageDeletionHandlers(bot, SQLConnection()))
