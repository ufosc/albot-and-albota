import discord
from discord.ext import commands
import requests
import json

class Compile:
    def __init__(self, bot):
        self.bot = bot
        self.complangs = []

    @commands.command(name="complangs")
    async def compile_langs(self, ctx):
        '''Get the languages and ids for compiling code'''
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
        '''Compiles and runs code using the judge0 api'''
        payload = {'source_code' : program, 'language_id' : lang_id}
        headers = {'Content-Type': "application/json"}
        r = requests.post("https://api.judge0.com/submissions/?base64_encoded=false&wait=true", data=json.dumps(payload), headers=headers)

        response = r.json()
        if r.status_code == 201:
            response = response['stdout']
            await ctx.send("Program ran sucessfully with output:\n\n```\n{}\n```".format(json.dumps(response, sort_keys=True, indent=4)))
        else:
            await ctx.send("Program failed with output:\n\n```json\n{}\n```".format(json.dumps(response, sort_keys=True, indent=4)))

def setup(bot):
    bot.add_cog(Compile(bot))