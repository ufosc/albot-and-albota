import discord
from discord.utils import get
from discord.ext import commands
import config

'''Cogs to load when the bot first starts'''
startup_cogs = [
    "cogs.helloworld",
    "cogs.memes",
    "cogs.projects",
    "cogs.admin",
    "cogs.music",
    "cogs.compile",
    "cogs.welcome"
]

bot = commands.Bot(command_prefix="!", description="ALBot (A Lame Bot)", case_insensitive=True, command_not_found="Invalid command: {}")

@bot.event
async def on_ready():
    """Print the bots information on connect"""
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')
    await bot.change_presence(activity=discord.Game(name="Destroying propritary software"))

if __name__ == "__main__":
    for extension in startup_cogs:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(config.ALBOT_TOKEN)
