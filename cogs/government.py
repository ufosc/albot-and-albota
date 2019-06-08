import discord
import typing
from discord.ext import commands

from database.database import SQLCursor, SQLConnection
# TODO: store Officer objects locally during bot lifespan to avoid excess database querying

class Government(commands.Cog, name='Government'):
    """Handles all of the UFOSC government related commands and querying."""

    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    # Valid positions types. TODO: Consider changing to an enum type.
    positions = ['social_chair', 'external_relations', 'secretary', 'server_admin']

    @commands.group(invoke_without_command=True, name='eboard')
    @commands.guild_only()
    async def government(self, ctx):
        """The root command for managing and checking government/officer information."""
        await ctx.message.channel.send(
                    'List of useable commands for the parent command: **eboard**\n\n**eboard seats** - shows a list of all government positions and their corresponding officers.\n\n**eboard position \"<position>\"** - shows the current officer that fills this position and a description of the position.')

    @government.group(invoke_without_command=True)
    @commands.guild_only()
    async def seats(self, ctx):
        """The seats subcommand displays the government positions and their corresponding descriptions."""
        positions = await self.query_positions()
        msg = ''
        for position in positions:
            msg += position['position'].replace('_', " ").capitalize() + ' - '
            try:
                if ',' in position['officer']:
                    officers = [str(ctx.message.guild.get_member(int(member_id))) for member_id in position['officer'].split(',')]
                    msg += ', '.join(officers) + '\n'
                else:
                    msg += (str(ctx.message.guild.get_member(int(position['officer']))) if position['officer'] is not None and position['officer'].strip() is not 'Vacant' else 'Vacant') + '\n'
            except KeyError as e:
                msg += 'Vacant\n'
        if msg is not '':
            await ctx.send(msg)

    @government.group(invoke_without_command=True)
    @commands.guild_only()
    async def admin(self, ctx):
        """The admin root command meant to handle all admin subcommands."""
        if ctx.message.author.top_role.name.lower() == 'officer':
                await ctx.message.channel.send('List of useable commands for the parent command: **admin**\n\n **eboard admin auto** - updates the new seats given current election data.\n\n**eboard admin set <position> <User#0000>** - assigns a position to target user.\n\n**eboard admin remove <position> <User#0000>** - remove a target user from their position.\n\n**eboard admin list** - lists the positions in the SQLite table.')

    @government.group(name='position')
    @commands.guild_only()
    async def show_occupants(self, ctx, position=''):
        pos = position.title()
        position = position.replace(' ', '_')
        if position.lower() in self.positions:
            with SQLCursor(self.db) as cur:
                cur.execute('SELECT description, officer FROM govt_info WHERE position = ?;', (position,))
                row = cur.fetchone()
                if row:
                    plural = False
                    if row[1] is not None and ',' in row[1]:
                        officers = [str(ctx.message.guild.get_member(int(member_id))) for member_id in row[1].split(',')]
                        officers = ', '.join(officers)
                        plural = True
                    else:
                        officers = (str(ctx.message.guild.get_member(int(row[1]))) if row[1] is not None and row[1].strip() is not '' else 'Vacant')
                    description = row[0]
                    await ctx.message.channel.send('The current _{}: _{}_'.format(pos + ('s_ are' if plural else '_ is'), officers))
                    if description is not None and description.strip() is not '':
                        await ctx.message.channel.send('Description: \n```{}```'.format(description))
        else:
            await ctx.channel.send('Invalid position. Here is a list of valid positions: ' + ', '.join(self.positions).replace('_', ' '))

    @admin.group()
    @commands.guild_only()
    async def list(self, ctx):
        if ctx.message.author.top_role.name.lower() == 'officer':
            await ctx.message.channel.send('The list of positions in the SQLite table: ' + ', '.join(self.positions))
        else:
            await ctx.message.channel.send('Hey! You do not have permission to do that.')

    @admin.group()
    @commands.guild_only()
    async def clear(self, ctx):
        """Clears all officers from their positions in the SQLite table."""
        if ctx.message.author.top_role.name.lower() == 'officer':
            with SQLCursor(self.db) as cur:
                cur.execute('UPDATE govt_info SET officer = Null;')
                await ctx.message.channel.send('Successfully cleared all officers from all positions in the SQLite table.')
        else:
            await ctx.message.channel.send('Hey! You do not have permission to do that.')

    @admin.group()
    @commands.guild_only()
    async def auto(self, ctx):
        """Automatically update roles and officer positions based on election results."""
        if ctx.message.author.top_role.name.lower() == 'officer':
            await ctx.message.channel.send('Still working on integration with the election results. Maybe have a command to link to an elections database?')
        else:
            await ctx.message.channel.send('Hey! You do not have permission to do that.')

    @admin.group()
    @commands.guild_only()
    async def description(self, ctx, pos ='', desc=''):
        if ctx.message.author.top_role.name.lower() == 'officer':
            if pos.strip() is not '':
                with SQLCursor(self.db) as cur:
                    cur.execute('UPDATE govt_info SET description = ? WHERE position = ?;', (desc, pos))
                    if desc.strip() is '':
                        await ctx.message.channel.send('Successfully cleared the description for position: **{}**'.format(pos))
                    else:
                        await ctx.message.channel.send('Successfully set a description for position: **{}**\n\nThe description is as follows:\n```{}```'.format(pos, desc))
            else:
                await ctx.message.channel.send('Invalid format, try: **eboard admin description <position> \"<desc>\"**')
        else:
            await ctx.message.channel.send('Hey! You do not have permission to do that.')

    @admin.group()
    @commands.guild_only()
    async def set(self, ctx, position, user: discord.User):
        if ctx.message.author.top_role.name.lower() == 'officer':
            member_id = user.id
            if position is None or member_id is None:
                await ctx.message.channel.send('Invalid command format, try: `eboard admin set <position> <@User#0000>`')
            else:
                with SQLCursor(self.db) as cur:
                    cur.execute('SELECT officer FROM govt_info WHERE position = ?;', (position,))
                    row = cur.fetchone()
                    if row:
                        officers = ','.join(row) if row[0] is not None else ''
                        if str(member_id) in officers:
                            return
                        officers += (',' if officers.strip() is not '' else '') + '{0}'.format(str(member_id))
                    else:
                        officers = str(member_id)

                    cur.execute('UPDATE govt_info SET officer = ? WHERE position = ?;', (officers, position))
                    await ctx.message.channel.send('Successfully added **{}** to the **{}** position.'.format(str(user), position))
        else:
            await ctx.message.channel.send('Hey! You do not have permission to do that.')

    @admin.group()
    @commands.guild_only()
    async def remove(self, ctx, position, user: discord.User):
        member_id = user.id
        if ctx.message.author.top_role.name.lower() == 'officer':
            with SQLCursor(self.db) as cur:
                cur.execute('SELECT officer FROM govt_info WHERE position = ?;', (position,))
                row = cur.fetchone()
                if row:
                    officers = ','.join(row) if row[0] is not None else ''
                    if officers.strip() != '':
                        officers = officers.replace(str(member_id) + ',', '').replace(str(member_id), '')
                        if len(officers.split(',')) == 1:
                            officers = officers.replace(',', '')
                        elif officers[len(officers) - 1:len(officers)] == ',':
                            officers = officers[0:len(officers) - 1]
                        cur.execute('UPDATE govt_info SET officer = ? WHERE position = ?;', (officers, position))
                        await ctx.message.channel.send('Successfully removed **{}** from the **{}** position.'.format(str(user), position))
        else:
            await ctx.message.channel.send('Hey! You do not have permission to do that.')

    async def query_position(self, position):
        """Return all of the officers for a corresponding position as a string list separated by commas."""
        with SQLCursor(self.db) as cur:
            cur.execute('SELECT officer FROM govt_info WHERE position=?', (position,))
            row = cur.fetchone()
            if row:
                return row[0] if not None else ''

    async def query_positions(self):
        """Returns an array of positions and corresponding descriptions."""
        values = [{} for _ in range(4)]
        counter = 0
        with SQLCursor(self.db) as cur:
            for pos in self.positions:
                cur.execute('SELECT position, description, officer FROM govt_info WHERE position=?', (pos,))
                row = cur.fetchone()
                if row:
                    values[counter] = {'position': row[0] if len(row) >= 1 else 'NULL',
                                       'description': row[1] if row[1] is not None else '',
                                       'officer': row[2] if row[2] is not None else 'Vacant'}
                else:
                    values[counter] = {}
                counter += 1
        return values


def initialize():
    """Initializes the table with non-null 'position' columns."""
    sql_db = SQLConnection()
    with SQLCursor(sql_db) as cur:
        cur.execute('SELECT position from govt_info')
        row = cur.fetchone()
        for pos in Government.positions:
            if row is None or len(row) != len(Government.positions):
                cur.execute('INSERT OR IGNORE INTO govt_info (position) VALUES (?);', (pos,))


def setup(bot):
    bot.add_cog(Government(bot, SQLConnection()))
    initialize()
