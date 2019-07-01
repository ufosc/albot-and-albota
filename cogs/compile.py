import discord
from discord.ext import commands
import requests
import json

from CONSTANTS import OFFICER_ROLE

class Compile(commands.Cog, name='Compile'):

    def __init__(self, bot):
        self.bot = bot
        self.complangs = []
        self.is_debug = False

    @commands.command(name="complangs")
    async def compile_langs(self, ctx):
        """Get the languages and ids for compiling code"""
        if len(self.complangs) == 0:
            langs = requests.get("https://api.judge0.com/languages")

            for lang in langs.json():
                self.complangs.append("{} | {}\n".format(lang['id'], lang['name']))

        response_text = "ID | Name\n"
        for lang in self.complangs:
            response_text += lang
        await ctx.send(response_text)

    @commands.command(name="compile")
    async def _compile(self, ctx, lang_id : int, *, program : str):
        """Compiles and runs code using the judge0 api"""
        payload = {'source_code' : program, 'language_id' : lang_id}
        headers = {'Content-Type': "application/json"}
        r = requests.post("https://api.judge0.com/submissions/?base64_encoded=false&wait=true", data=json.dumps(payload), headers=headers)

        response = r.json()
        if r.status_code == 201:
            if not self.is_debug:
                response = response['stdout']
            await ctx.send("Program ran sucessfully with output:\n\n```\n{}\n```".format(json.dumps(response, sort_keys=True, indent=4)))
        else:
            await ctx.send("Program failed with output:\n\n```json\n{}\n```".format(json.dumps(response, sort_keys=True, indent=4)))

    @commands.command(name="compdebug")
    @commands.has_role(OFFICER_ROLE)
    async def debug_compile(self, ctx):
        """Toggles whether to print the full compile output"""
        self.is_debug = not self.is_debug
        await ctx.send("is_debugging = {}".format(self.is_debug))

def setup(bot):
    bot.add_cog(Compile(bot))
