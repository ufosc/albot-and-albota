import asyncio
import datetime

import discord
from discord.ext import commands

import cogs.CONSTANTS as CONST


class Reminder(commands.Cog, name='Reminder'):
    """To remind officers and members about things"""

    def __init__(self, bot):
        self.bot = bot
        self.book_room_bg_task = self.bot.loop.create_task(self.book_room_reminder())

    async def book_room_reminder(self):
        """ Every week, on Wednesday at 16:00, this method sends a reminder
            message to all users in the provided channel, reminding them to
            book a room for casual coding.
        """
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(CONST.OFFICER_CHANNEL)
        # NOTE: weekday() returns an int from 0 (monday) to 6 (sunday)
        trigger_day = 2  # 2 = Wednesday

        while True:
            cur_time = datetime.datetime.now()
            day_delta = trigger_day - cur_time.weekday()
            if day_delta <= 0:
                day_delta += 7

            destination_time = cur_time.replace(
                hour=16,
                minute=0,
                second=0,
                microsecond=0
            ) + datetime.timedelta(day_delta, 0, 0)

            embed = discord.Embed(
                title="{info} Reminder".format(
                    info=CONST.REACTION_INFO
                ),
                colour=discord.Colour(CONST.EMBED_COLOR_STANDARD),
                description="Remember to book rooms for Casual Coding!",
            )

            embed.set_footer(text="This reminder will repeat at {nxt}.".format(
                nxt=destination_time.isoformat(" ")
            ))

            await channel.send("@everyone", embed=embed)
            await asyncio.sleep((destination_time - datetime.datetime.now()).seconds())


def setup(bot):
    bot.add_cog(Reminder(bot))
