from discord.ext import commands


class Welcome(commands.Cog, name="Welcome"):
    """To automatically welcome new members to the server"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        fmt = """Welcome {0.mention}! \nFeel free to use \"!question\" to let us know if you have any questions \nAnd
        you can also use \"!help\", all in the #bot-spam channel to find out about what you can do with our Discord
        bot ALBot :D """
        dm_channel = member.dm_channel
        if dm_channel is None:
            await member.create_dm()
        dm_channel = member.dm_channel
        await dm_channel.send(fmt.format(member))


def setup(bot: commands.Bot):
    bot.add_cog(Welcome(bot))
