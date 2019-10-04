import discord
from discord.utils import get
from discord.ext import commands

class Projects(commands.Cog, name='Projects'):
    """Commands dealing with the different projects we are working on"""
    def __init__(self, bot):
        self.bot = bot

    async def alumnus(self, ctx):
        """"Add the Alumnus role to the user"""
        role = discord.utils.get(ctx.guild.roles, name="alumnus")
        await ctx.author.add_roles(role)
        await ctx.send("Eway elcomway youway otay hetay alumni ounglay")
        await ctx.send(":thinking:")

    async def muddy(self, ctx):
        """Add the muddy swamp role to the user"""
        role = discord.utils.get(ctx.guild.roles, name="muddy-swamp")
        await ctx.author.add_roles(role)
        await ctx.send("Get out of my swamp!")
        await ctx.send(file=discord.File('get-out-of-my-swamp.jpg'))

    async def website(self, ctx):
        """Add the website role to the user"""
        role = get(ctx.guild.roles, name="club-website")
        await ctx.author.add_roles(role)
        await ctx.send("HTML is my favorite programming language.")

    async def mvw(self, ctx):
        """Add the marston vs west role to the user"""
        role = get(ctx.guild.roles, name="marston-vs-west")
        await ctx.author.add_roles(role)
        await ctx.send("Newell is the best 24/7 library. Don't @ me")

    async def albot(self, ctx):
        """Add the bot role to the user"""
        role = get(ctx.guild.roles, name="bot-dev")
        await ctx.author.add_roles(role)
        await ctx.send("I, for one, welcome our robot overlords")

    @commands.command()
    async def join(self, ctx, *, roleName: str):
        """Add a role to a user"""
        if roleName.lower() in ["alumni", "alumnus", "alumna", "alum", "stultus", "stulta"]:
            await self.alumnus(ctx)
        elif roleName.lower() in ["muddy", "muddy swamp", "muddyswamp", "muddy-swamp", "MUD"]:
            await self.muddy(ctx)
        elif roleName.lower() in ["website", "club site", "club website", "clubwebsite", "clubsite"]:
            await self.website(ctx)
        elif roleName.lower() in ["mvw", "marstonvswest", "marston vs west", "marston v west"]:
            await self.mvw(ctx)
        elif roleName.lower() in ["bot", "albot"]:
            await self.albot(ctx)

    @commands.command()
    async def list(self, ctx):
        """Print the list of the current projects we are working on."""
        embed=discord.Embed(title="Muddy Swamp", url="https://github.com/ufosc/MuddySwamp", description="A UF themed python MUD game.", color=0x00630c)
        embed.add_field(name="Join using", value="!join muddyswamp", inline=True)
        await ctx.send(embed=embed)

        embed=discord.Embed(title="Marston Vs West", url="https://github.com/ufosc/marston-vs-west", description="A HTML5 smashbros-esque game fitting our libraries against each other.", color=0xff0036)
        embed.add_field(name="Join using", value="!join mvw", inline=True)
        await ctx.send(embed=embed)

        embed=discord.Embed(title="Club Website", url="https://github.com/ufosc/club-website", description="Our club website made using basic HTML, CSS, and JS.", color=0x00ecff)
        embed.add_field(name="Join using", value="!join clubsite", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Bot", url="https://github.com/ufosc/albot-and-albota", description="A python based discord bot", color=0x808080)
        embed.add_field(name="Join using", value="!join bot", inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Projects(bot))
