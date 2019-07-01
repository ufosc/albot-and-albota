import asyncio
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


class ALBotMessageClear(commands.Cog, name='Message Clear'):
    """Functions for handling message deletion in channels"""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role(CONSTANTS.OFFICER_ROLE)
    @commands.command()
    async def clear(self, ctx, a_number):
        # Checks if number is positive int
        if not a_number.isdigit() or not int(a_number) > 0:
            await ctx.channel.send(content="Please input a number larger than zero")
            return

        # checks the message reaction to see if the user confirms or cancels the command and returns True or False respectively
        async def confirms(self, ctx, user, bot_msg):
            while True:

                def check(reaction: discord.Reaction, adder: discord.User) -> bool:
                    return adder == user and reaction.message.id == bot_msg.id

                reaction, adder = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)

                if reaction.emoji == "✅":
                    return True
                elif reaction.emoji == "❌":
                    return False

        # checks user permissions to see if they can manage messages in the channel
        if self.bot.get_channel(ctx.channel.id).permissions_for(ctx.author).manage_messages:
            user = ctx.channel.last_message.author
            user_msg = ctx.channel.last_message

            # warns the user and confirms the clear command
            await ctx.channel.send("WARNING: You are about to delete {} messages, are you sure you want to do this?".format(a_number))
            bot_msg = ctx.channel.last_message

            #adds reactions to the bot message
            reactions = ["✅","❌"]
            for emoji in reactions:
                await bot_msg.add_reaction(emoji)

            # Waits 30s for a user reaction and continues only if they respond with ❌ or ✅
            try:
                cont = await confirms(self, ctx, user, bot_msg)
            except asyncio.TimeoutError:
                await bot_msg.delete()
                await ctx.channel.send('Clear command Timeout')
                return

            # Cancels the command and deletes the bot message
            if not cont:
                await bot_msg.delete()
                await ctx.channel.send(content='Clear command cancelled')
                return

            # deletes bot message, user msg, then loops through channel deleting messages
            await bot_msg.delete()
            await user_msg.delete()
            async for message in ctx.channel.history(limit=int(a_number)):
                if not message.pinned:
                    await message.delete()
                    await asyncio.sleep(0.4)
            await ctx.channel.send(content='@{} Successfully deleted {} messages'.format(ctx.author, int(a_number)))

def setup(bot):
    bot.add_cog(ALBotMessageDeletionHandlers(bot, SQLConnection()))
    bot.add_cog(ALBotFactorialHandler(bot))
    bot.add_cog(ALBotMessageClear(bot))
