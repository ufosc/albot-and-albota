import discord
import random
import datetime
import asyncio
from discord.ext import commands

class Reminder(commands.Cog, name='Reminder'):
    """To remind officers and members about things"""
    def __init__(self, bot):
        self.bot = bot
        self.book_room_bg_task = self.bot.loop.create_task(self.book_room_reminder())
    
    async def book_room_reminder(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(436916990238785556)
        while True:
            current_day_of_the_week = (str)(datetime.date.today().strftime("%A"))
            #print (current_day_of_the_week)
            if current_day_of_the_week == "Wednesday" or current_day_of_the_week == "Thursday":
                await channel.send("@everyone Reminder to book rooms!")
                # ideally, the bot would send the reminder on Wednesdat 12am, 
                # but to account for when the bot starts running,
                # the time below is 2 minutes less than 1 week,
                # this allows the time to be slowly adjusted every week until it reaches 12am
                await asyncio.sleep(604680) # a little less than a week
            else:
                # this line will run twice every week once 
                # the time is stabilized as mentioned above
                await asyncio.sleep(60) # check every 1 minute

def setup(bot):
    bot.add_cog(Reminder(bot))
