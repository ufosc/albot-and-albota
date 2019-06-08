import textwrap
import discord
from discord.ext import commands

from contextlib import redirect_stdout
import io

from cogs.CONSTANTS import OFFICER_ROLE

class Admin(commands.Cog, name='Admin'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.has_role(OFFICER_ROLE)
    async def load(self, ctx, extension_name : str):
        """Loads an extension."""
        try:
            if extension_name.startswith("cogs."):
                self.bot.load_extension(extension_name)
            else:
                self.bot.load_extension("cogs." + extension_name)
        except Exception as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} loaded.".format(extension_name))

    @commands.command(hidden=True)
    @commands.has_role(OFFICER_ROLE)
    async def unload(self, ctx, extension_name : str):
        """Unloads an extension."""
        if extension_name.startswith("cogs."):
            self.bot.unload_extension(extension_name)
        else:
            self.bot.unload_extension("cogs." + extension_name)
        await ctx.send("{} unloaded.".format(extension_name))

    @commands.command(hidden=True)
    @commands.has_role(OFFICER_ROLE)
    async def reload(self, ctx, extension_name : str):
        """Unloads and then loads an extension"""
        try:
            if extension_name.startswith("cogs."):
                self.bot.reload_extension(extension_name)
            else:
                self.bot.reload_extension("cogs." + extension_name)
        except Exception as e:
            await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
            return
        await ctx.send("{} reloaded.".format(extension_name))

    @commands.command(hidden=True)
    @commands.has_role(OFFICER_ROLE)
    async def whereami(self, ctx):
        await ctx.send("You are in {} with id {}".format(ctx.channel.name, ctx.channel.id))

    @commands.command(hidden=True, name="eval")
    @commands.is_owner()
    async def admin_eval(self, ctx, *, cmd : str):
        """Evaluates Python code only if the executor is hjarrell"""
        env = {
            'bot': self.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx
        }

        stdout = io.StringIO()

        indented_body = textwrap.indent(cmd, "    ")

        cmd_body = "async def __admin_eval():\n{}".format(indented_body)
        try:
            exec(cmd_body, env)
        except Exception as e:
            return await ctx.send("```py\n{0.__class__.__name__}: {0}\n```", e)

        try:
            with redirect_stdout(stdout):
                ret = await eval("__admin_eval()", env)
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send("```py\n{}{}\n```".format(value, e))
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    await ctx.send("```py\n{}\n```".format(value))
            else:
                await ctx.send("```py\n{}{}\n```".format(value, ret))

def setup(bot):
    bot.add_cog(Admin(bot))
