import discord
from discord.ext import commands

import cogs.util

class Admin:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(cogs.util.is_officer_check)
    async def load(self, ctx, extension_name : str):
        '''Loads an extension.'''
        try:
            if extension_name.startswith("cogs."):
                self.bot.load_extension(extension_name)
            else:
                self.bot.load_extension("cogs." + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))

    @commands.command(hidden=True)
    @commands.check(cogs.util.is_officer_check)
    async def unload(self, ctx, extension_name : str):
        """Unloads an extension."""
        if extension_name.startswith("cogs."):
            self.bot.unload_extension(extension_name)
        else:
            self.bot.unload_extension("cogs." + extension_name)
        await ctx.send("{} unloaded.".format(extension_name))

    @commands.command(hidden=True)
    @commands.check(cogs.util.is_officer_check)
    async def reload(self, ctx, extension_name : str):
        '''Unloads and then loads an extension'''
        try:
            if extension_name.startswith("cogs."):
                self.bot.unload_extension(extension_name)
                self.bot.load_extension(extension_name)
            else:
                self.bot.unload_extension("cogs." + extension_name)
                self.bot.load_extension("cogs." + extension_name)
        except (AttributeError, ImportError) as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} reloaded.".format(extension_name))

def setup(bot):
    bot.add_cog(Admin(bot))
