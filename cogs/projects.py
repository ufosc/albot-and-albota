import discord
from discord.ext import commands
from discord.utils import get

import cogs.CONSTANTS as CONSTANTS


class Projects(commands.Cog, name='Projects'):
    """Commands dealing with the different projects we are working on"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def alumnus(self, ctx):
        """"Add the Alumnus role to the user"""
        if ctx.author.roles and (len(ctx.author.roles) > 1):
            roles = [role for role in ctx.author.roles if role.name in CONSTANTS.PROJECT_ROLES]
            await self.leave_all_roles(ctx, roles)

        role = discord.utils.get(ctx.guild.roles, name="alumnus")
        await ctx.author.add_roles(role)
        await ctx.send("Eway elcomway youway otay hetay alumni ounglay")
        await ctx.send(":thinking:")

    async def bot(self, ctx):
        """Add the bot-dev role to the user"""
        role = discord.utils.get(ctx.guild.roles, name=CONSTANTS.BOT_ROLE)
        await ctx.author.add_roles(role)
        await ctx.send("I, for one, welcome our robot overlords")

    async def muddy(self, ctx):
        """Add the muddy swamp role to the user"""
        role = discord.utils.get(ctx.guild.roles, name=CONSTANTS.MUDDY_ROLE)
        await ctx.author.add_roles(role)
        await ctx.send("Get out of my swamp!")
        await ctx.send(file=discord.File('get-out-of-my-swamp.jpg'))

    async def website(self, ctx):
        """Add the website role to the user"""
        role = get(ctx.guild.roles, name=CONSTANTS.WEBSITE_ROLE)
        await ctx.author.add_roles(role)
        await ctx.send("HTML is my favorite programming language.")

    async def albot(self, ctx):
        """Add the bot role to the user"""
        role = get(ctx.guild.roles, name=CONSTANTS.BOT_ROLE)
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
        elif roleName.lower() in CONSTANTS.ALBOT:
            await self.albot(ctx)
        elif roleName.lower() in CONSTANTS.FAULT:
            await self.fault(ctx)
        elif roleName.lower() in CONSTANTS.GRAPHICS:
            await self.graphics(ctx)

    @commands.command()
    async def leave(self, ctx, *, roleName: str = None):
        """Remove a given role from a user"""
        try:
            if roleName is not None:
                if roleName.lower() in CONSTANTS.ALUMNUS:
                    role = discord.utils.get(ctx.guild.roles, name=CONSTANTS.ALMUNI_ROLE)
                elif roleName.lower() in CONSTANTS.MUDDY:
                    role = discord.utils.get(ctx.guild.roles, name=CONSTANTS.MUDDY_ROLE)
                elif roleName.lower() in CONSTANTS.WEBSITE:
                    role = discord.utils.get(ctx.guild.roles, name=CONSTANTS.WEBSITE_ROLE)
                elif roleName.lower() in CONSTANTS.MVW:
                    role = discord.utils.get(ctx.guild.roles, name=CONSTANTS.MVW_ROLE)
                elif roleName.lower() in CONSTANTS.ALBOT:
                    role = discord.utils.get(ctx.guild.roles, name=CONSTANTS.BOT_ROLE)
                await self.leave_role(ctx, role)
            else:
                roles = [role for role in ctx.author.roles if role.name != "@everyone"]
                await self.leave_all_roles(ctx, roles)
        except UnboundLocalError:
            await ctx.send(f"{roleName} role doesn't exist")

    async def leave_role(self, ctx, role):
        """Remove given users role """
        if role in ctx.author.roles:
            await ctx.author.remove_roles(role)
            await ctx.send(f"Removed role from {role.name}")

    async def leave_all_roles(self, ctx, roles):
        """Remove all given roles"""
        for role in roles:
            await self.leave_role(ctx, role)

    @commands.command()
    async def list(self, ctx):
        """Print the list of the current projects we are working on."""
        embed = discord.Embed(title="Muddy Swamp", url="https://github.com/ufosc/MuddySwamp",
                              description="A UF themed python MUD game.", color=0x00630c)
        embed.add_field(name="Join using", value="!join muddyswamp", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Club Website", url="https://github.com/ufosc/club-website",
                              description="Our club website made using basic HTML, CSS, and JS.", color=0x00ecff)
        embed.add_field(name="Join using", value="!join clubsite", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Bot", url="https://github.com/ufosc/albot-and-albota",
                              description="A python based discord bot", color=0x808080)
        embed.add_field(name="Join using", value="!join bot", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Seg Fault", url="https://github.com/ufosc/seg-fault",
                              description="A python based discord bot", color=0xff0036)
        embed.add_field(name="Join using", value="!join fault", inline=True)
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Projects(bot))
