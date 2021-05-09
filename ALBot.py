import logging
import discord
from discord.ext import commands

import config

"""Cogs to load when the bot first starts"""
startup_cogs = [
    "cogs.messages",
    "cogs.errors",
    "cogs.helloworld",
    "cogs.memes",
    "cogs.projects",
    "cogs.admin",
    "cogs.music",
    "cogs.welcome",
    "cogs.help",
    "cogs.reminder",
    "cogs.government",
    "cogs.tally",
    # "cogs.leaderboard"
]

# list the access token in your config.py
# Use the GitHub Apps API and show the current milestones for all the current active projects. Show the top
# contributor of the week/month/semester and a little leaderboard based on commits/adds/subs. Also list some help
# wanted and good first issue issues for people to jump on. Also show the issues that people are assigned,
# with an @ for their discord username.

bot_url = 'https://discordapp.com/api/oauth2/authorize?client_id={0}&scope=bot&permissions=0'

bot = commands.Bot(command_prefix="!", description="ALBot (A Lame Bot)", case_insensitive=True,
                   command_not_found="Invalid command: {}")


@bot.event
async def on_ready():
    """Print the bots information on connect"""
    global bot_url
    print('Logged in as "{name}" with id {id}'.format(name=bot.user.name, id=bot.user.id))
    print('Invite URL: {iurl}'.format(iurl=bot_url.format(bot.user.id)))
    await bot.change_presence(activity=discord.Game(name="Destroying propritary software"))


def setup_logging():
    logging.basicConfig(filename='albot.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    setup_logging()
    for extension in startup_cogs:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(config.ALBOT_TOKEN)
