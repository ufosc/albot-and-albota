import discord
from discord.ext import commands
from discord.utils import get

import cogs.CONSTANTS as CONSTANTS


class Projects(commands.Cog, name='Projects'):
    """Commands dealing with the different projects we are working on"""

    def __init__(self, bot):
        self.bot = bot

    async def alumnus(self, ctx):
        """"Add the Alumnus role to the user"""
        if ctx.author.roles and (len(ctx.author.roles) > 1):
            for role in ctx.author.roles:
                if role.name not in ["@everyone", "alumnus"]:
                    await self.leave_role(ctx, role)

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
        if roleName.lower() in CONSTANTS.ALUMNUS:
            await self.alumnus(ctx)
        elif roleName.lower() in CONSTANTS.MUDDY:
            await self.muddy(ctx)
        elif roleName.lower() in CONSTANTS.WEBSITE:
            await self.website(ctx)
        elif roleName.lower() in CONSTANTS.MVW:
            await self.mvw(ctx)
        elif roleName.lower() in CONSTANTS.ALBOT:
            await self.albot(ctx)

    @commands.command()
    async def leave(self, ctx, *, roleName: str):
        """Remove a given role from a user"""
        if roleName.lower() in CONSTANTS.ALUMNUS:
            role = discord.utils.get(ctx.guild.roles, name="alumnus")
        elif roleName.lower() in CONSTANTS.MUDDY:
            role = discord.utils.get(ctx.guild.roles, name="muddy-swamp")
        elif roleName.lower() in CONSTANTS.WEBSITE:
            role = discord.utils.get(ctx.guild.roles, name="club-website")
        elif roleName.lower() in CONSTANTS.MVW:
            role = discord.utils.get(ctx.guild.roles, name="marston-vs-west")
        elif roleName.lower() in CONSTANTS.ALBOT:
            role = discord.utils.get(ctx.guild.roles, name="bot-dev")

        await self.leave_role(ctx, role)

    async def leave_role(self, ctx, role):
        """Remove given users role """
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.send(f"Removed role from {role.name}")

    @commands.command()
    async def list(self, ctx):
        """Print the list of the current projects we are working on."""
        embed = discord.Embed(title="Muddy Swamp", url="https://github.com/ufosc/MuddySwamp",
                              description="A UF themed python MUD game.", color=0x00630c)
        embed.add_field(name="Join using", value="!join muddyswamp", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Marston Vs West", url="https://github.com/ufosc/marston-vs-west",
                              description="A HTML5 smashbros-esque game fitting our libraries against each other.",
                              color=0xff0036)
        embed.add_field(name="Join using", value="!join mvw", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Club Website", url="https://github.com/ufosc/club-website",
                              description="Our club website made using basic HTML, CSS, and JS.", color=0x00ecff)
        embed.add_field(name="Join using", value="!join clubsite", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Bot", url="https://github.com/ufosc/albot-and-albota",
                              description="A python based discord bot", color=0x808080)
        embed.add_field(name="Join using", value="!join bot", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Projects(bot))
