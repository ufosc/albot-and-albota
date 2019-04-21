from discord.ext import commands
from database.database import SQLCursor, SQLConnection


class Government(commands.Cog, name='Government'):
    """Handles all of the UFOSC government related commands and querying."""
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    # Valid positions types. TODO: Consider changing to an enum type.
    positions = ['social_chair', 'external_relations', 'secretary', 'server_admin']

    @commands.group(invoke_without_command=True, name='govt')
    # means that it will run this code if you just do "!example"
    async def government(self, ctx):
        await ctx.send("works!")

    @government.command()
    async def list(self, ctx):
        """The list subcommand displays the government positions and their corresponding descriptions."""
        positions = await self.query_positions()
        msg = ''
        for position in positions:
            if position[0] is not (None or ''):
                msg += position['position'] + ' - ' + position['officer']
        if msg is not '':
            ctx.send(msg)

    async def query_positions(self):
        """Returns an array of positions and corresponding descriptions."""
        positions = []
        counter = 0
        with SQLCursor(self.db) as cur:
            for pos in self.positions:
                cur.execute('SELECT position, description, officer FROM govt_info WHERE position=?', pos)
                row = cur.fetchone()
                if row:
                    positions[counter] = {'position': row[0] if row[0] is not None else 'NULL', 'description': row[1] if row[1] is not None else '', 'officer': row[2] if row[2] is not None else 'Vacant'}
                else:
                    positions[counter] = {}
                counter += 1
        return positions
