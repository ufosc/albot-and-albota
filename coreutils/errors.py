import sys
import traceback
import math

import discord
from discord.ext import commands

from sql.sql import SQLCursor, SQLConnection
from coreutils.messages import track

class ALBotErrorHandlers:
    """ Handles errors """

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    def _construct_error_embed(self, command_name, error_name, error_text, full_command_string, full_backtrace=None):
        """ Constructs an embed for an error message """
        title = "⚠ An error was encountered while processing the {0} command".format(command_name)
        embed = discord.Embed(title=title, colour=discord.Colour(self.bot.embed_colour), description="**{0}**: ```{1}```".format(error_name, str(error_text)))
        embed.set_footer(text="Report bugs at https://github.com/ufosc/albot-and-albota")
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
            embed.add_field(name='Press \u2733', value='for full error backtrace', inline=False)
        
        return embed
                
    def _construct_unknown_command_embed(self, error_text, full_text):
        title = "❓ Invalid command."
        embed = discord.Embed(title=title, colour=discord.Colour(self.bot.embed_colour), description='```{0}```'.format(error_text))
        embed.set_footer(text="Use {0}help for a list of commands.".format(self.bot.command_prefix))
        embed.add_field(name="While processing the command:", value="``{0}``".format(full_text), inline=False)

        return embed

    async def on_command_error(self, ctx, error):
        """ Handle command errors
          " Note that this uses the SQL database to store full backtrace
          " messages, so that users can click a reaction button to
          " expand the error message.
        """
        if type(error) == discord.ext.commands.MissingPermissions:
            """ Use a separate embed for "insufficient permissions" errors """
            await ctx.message.add_reaction('⛔')
            embed = discord.Embed(title='⛔ Insufficient Permissions', colour=discord.Colour(self.bot.embed_colour), description="You are not permitted to run the command ``{0}``".format(ctx.message.content))
            embed.add_field(name="Reason:", value=str(error))
            msg = await ctx.send(content='', embed=embed)
            await track(msg, ctx.author)
        else:
            embed = None
            if not ctx.command:
                embed = self._construct_unknown_command_embed(str(error), ctx.message.content)
            else:
                embed = self._construct_error_embed(ctx.command.name, str(type(error)), str(error), ctx.message.content)

            await ctx.message.add_reaction('⚠')
            msg = await ctx.send(content='', embed=embed)
            await track(msg, ctx.author)
            if not ctx.command:
                return
            await msg.add_reaction('\u2733')
            with SQLCursor(self.db) as cur:
                bt_string = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
                print('ALBot encountered an error:\n{0}'.format(bt_string))
                cur.execute('INSERT INTO error_messages (message_id, channel_id, command_name, error_name, error_text, full_backtrace, full_command_string) VALUES (?,?,?,?,?,?,?);',(msg.id, msg.channel.id, ctx.command.name, str(type(error)), str(error), bt_string, ctx.message.content))

    async def on_raw_reaction_add(self, payload):
        """ Checks reactions and expands error messages when necessary. """
        if payload.user_id == self.bot.user.id:
            return
        elif payload.emoji.name == '\u2733':
            row = None
            with SQLCursor(self.db) as cur:
                cur.execute('SELECT command_name, error_name, error_text, full_command_string, full_backtrace FROM error_messages WHERE message_id=? AND channel_id=?;',(payload.message_id, payload.channel_id))
                row = cur.fetchone()
            if not row:
                return
                
            to_edit = await self.bot.get_channel(payload.channel_id).get_message(payload.message_id)
            new_embed = self._construct_error_embed(row[0],row[1],row[2],row[3],row[4])
            await to_edit.edit(content='⚠ Command error ⚠',embed=new_embed)

    async def on_raw_reaction_remove(self, payload):
        """ Contracts error messages on reaction remove """
        if payload.user_id == self.bot.user.id:
            return
        if payload.emoji.name == '\u2733':
            row = None
            with SQLCursor(self.db) as cur:
                cur.execute('SELECT command_name, error_name, error_text, full_command_string, full_backtrace FROM error_messages WHERE message_id=? AND channel_id=?;',(payload.message_id, payload.channel_id))
                row = cur.fetchone()
            if not row:
                return

            to_edit = await self.bot.get_channel(payload.channel_id).get_message(payload.message_id)
            new_embed = self._construct_error_embed(row[0],row[1],row[2],row[3])
            await to_edit.edit(content='⚠ Command error ⚠',embed=new_embed)

def setup(bot):
    bot.add_cog(ALBotErrorHandlers(bot, SQLConnection()))
