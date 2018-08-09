import discord
from discord.utils import get
import config

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')
    await client.change_presence(activity=discord.Game(name="Contributing to open source"))

client.run(config.ALBOTA_TOKEN)
