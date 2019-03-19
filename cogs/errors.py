import sys
import traceback
import math

import discord
from discord.ext import commands

import cogs.CONSTANTS as CONSTANTS
from database.database import SQLCursor, SQLConnection
from cogs.messages import track

class ALBotErrorHandlers(commands.Cog, name='Error Handler'):
    """ Handles errors """
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def _construct_error_embed(self, command_name, error_name, error_text, full_command_string, full_backtrace=None):
        title = "{err} An error was encountered while processing the {0} command".format(command_name, err=CONSTANTS.REACTION_ERROR)
        embed = discord.Embed(title=title, colour=discord.Colour(CONSTANTS.EMBED_COLOR_ERROR), description="**{0}**: ```{1}```".format(error_name, str(error_text)))
        embed.set_footer(text="Report bugs at {url}".format(url=CONSTANTS.ERROR_REPORT_URL))
        embed.add_field(name="While processing the command:", value="``{0}``".format(full_command_string), inline=False)
        if full_backtrace:
            itr = 1
            total_itrs = math.ceil(len(full_backtrace)/512)
            while len(full_backtrace) > 0:
                if len(full_backtrace) > 512:
                    embed.add_field(name="Backtrace ({0} of {1}):".format(itr, total_itrs), value="```{0}```".format(full_backtrace[:512]), inline=False)
                    full_backtrace = full_backtrace[512:]
                    itr = itr + 1
                else:
                    embed.add_field(name="Backtrace ({0} of {1}):".format(itr, total_itrs), value="```{0}```".format(full_backtrace), inline=False)
                    break
        else:
            embed.add_field(name='Press {expand}'.format(expand=CONSTANTS.REACTION_EXPAND), value='for full error backtrace', inline=False)

        return embed

    def _construct_unknown_command_embed(self, error_text, full_text):
        title = "{notfound} Invalid command.".format(notfound=CONSTANTS.REACTION_NOT_FOUND)
        embed = discord.Embed(title=title, colour=discord.Colour(CONSTANTS.EMBED_COLOR_ERROR), description='```{0}```'.format(error_text))
        embed.set_footer(text="Use {0}help for a list of commands.".format(self.bot.command_prefix))
        embed.add_field(name="While processing the command:", value="``{0}``".format(full_text), inline=False)

        return embed

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if type(error) == discord.ext.commands.MissingPermissions:
            await ctx.message.add_reaction(CONSTANTS.REACTION_DENY)
            embed = discord.Embed(title='{deny} Insufficient Permissions'.format(deny=CONSTANTS.REACTION_DENY), colour=discord.Colour(CONSTANTS.EMBED_COLOR_ERROR), description="You are not permitted to run the command ``{0}``".format(ctx.message.content))
            embed.add_field(name="Reason:", value=str(error))
            msg = await ctx.send(content='', embed=embed)
            await track(msg, ctx.author)
        else:
            embed = None
            if not ctx.command:
                embed = self._construct_unknown_command_embed(str(error), ctx.message.content)
            else:
                embed = self._construct_error_embed(ctx.command.name, str(type(error)), str(error), ctx.message.content)

            await ctx.message.add_reaction(CONSTANTS.REACTION_ERROR)
            msg = await ctx.send(content='', embed=embed)
            await track(msg, ctx.author)
            if not ctx.command:
                return
            await msg.add_reaction(CONSTANTS.REACTION_EXPAND)
            with SQLCursor(self.db) as cur:
                bt_string = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
                print('{bname} encountered an error:\n{0}'.format(bt_string, bname=CONSTANTS.BOT_NAME))
                cur.execute('INSERT INTO error_messages (message_id, channel_id, command_name, error_name, error_text, full_backtrace, full_command_string) VALUES (?,?,?,?,?,?,?);',(msg.id, msg.channel.id, ctx.command.name, str(type(error)), str(error), bt_string, ctx.message.content))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        elif payload.emoji.name == CONSTANTS.REACTION_EXPAND:
            row = None
            with SQLCursor(self.db) as cur:
                cur.execute('SELECT command_name, error_name, error_text, full_command_string, full_backtrace FROM error_messages WHERE message_id=? AND channel_id=?;',(payload.message_id, payload.channel_id))
                row = cur.fetchone()
            if not row:
                return

            to_edit = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            new_embed = self._construct_error_embed(row[0],row[1],row[2],row[3],row[4])
            await to_edit.edit(content='{err} Command error {err}'.format(err=CONSTANTS.REACTION_ERROR),embed=new_embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return
        if payload.emoji.name == CONSTANTS.REACTION_EXPAND:
            row = None
            with SQLCursor(self.db) as cur:
                cur.execute('SELECT command_name, error_name, error_text, full_command_string, full_backtrace FROM error_messages WHERE message_id=? AND channel_id=?;',(payload.message_id, payload.channel_id))
                row = cur.fetchone()
            if not row:
                return

            to_edit = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            new_embed = self._construct_error_embed(row[0],row[1],row[2],row[3])
            await to_edit.edit(content='{err} Command error {err}'.format(err=CONSTANTS.REACTION_ERROR),embed=new_embed)



def setup(bot):
    bot.add_cog(ALBotErrorHandlers(bot, SQLConnection()))
