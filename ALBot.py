import discord
from discord.utils import get
from discord.ext import commands
import config

'''Cogs to load when the bot first starts'''
startup_cogs = [
    "coreutils.messages",
    "coreutils.errors",
    "cogs.helloworld",
    "cogs.memes",
    "cogs.projects",
    "cogs.admin",
    "cogs.music",
    "cogs.compile"
]

bot_url = 'https://discordapp.com/api/oauth2/authorize?client_id={0}&scope=bot&permissions=0'

bot = commands.Bot(command_prefix="!", description="ALBot (A Lame Bot)", case_insensitive=True, command_not_found="Invalid command: {}")
bot.embed_colour = 0x00529b # make a universal color available for use in embeds

class ALBotCore:
    """ Basic functionality """
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        """Print the bots information on connect"""
        global bot_url
        print('Logged in as "{name}" with id {id}'.format(name=bot.user.name,id=bot.user.id))
        print('Invite URL: {iurl}'.format(iurl=bot_url.format(self.bot.user.id)))
        print('-----')
        await bot.change_presence(activity=discord.Game(name="Destroying propritary software"))
    
bot.add_cog(ALBotCore(bot))

if __name__ == "__main__":
    for extension in startup_cogs:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(config.ALBOT_TOKEN)
