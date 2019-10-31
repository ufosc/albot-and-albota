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

    async def bot(self, ctx):
        """Add the bot-dev role to the user"""
        role = discord.utils.get(ctx.guild.roles, name="bot-dev")
        await ctx.author.add_roles(role)
        await ctx.send("I, for one, welcome our robot overlords")

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

    async def fault(self, ctx):
        """Add the seg-fault role to the user"""
        role = get(ctx.guild.roles, name="seg-fault")
        await ctx.author.add_roles(role)
        await ctx.send("Segmentation fault (core dumped)")

    async def graphics(self, ctx):
        """Add graphics-accelerator role to the user"""
        role = get(ctx.guild.roles, name="graphics-accelerator")
        await ctx.author.add_roles(role)
        await ctx.send("Accelerating... Accelerating... Accelerating...")

    @commands.command()
    async def join(self, ctx, *, roleName: str):
        """Add a role to a user"""
        if roleName.lower() in ["alumni", "alumnus", "alumna", "alum", "stultus", "stulta"]:
            await self.alumnus(ctx)
        elif roleName.lower() in ["bot", "albot", "al bot"]:
            await self.bot(ctx)
        elif roleName.lower() in ["muddy", "muddy swamp", "muddyswamp", "muddy-swamp", "MUD"]:
            await self.muddy(ctx)
        elif roleName.lower() in ["website", "club site", "club website", "clubwebsite", "clubsite"]:
            await self.website(ctx)
        elif roleName.lower() in ["fault", "seg-fault", "segfault", "seg fault", "seg", "sf", "s-f"]:
            await self.fault(ctx)
        elif roleName.lower() in ["graphics", "graphics accelerator", "graphics-accelerator", "g-a", "accelerator", "silga"]:
            await self.graphics(ctx)

    @commands.command()
    async def list(self, ctx):
        """Print the list of the current projects we are working on."""
        embed = discord.Embed(title="Bot", url="https://github.com/ufosc/albot-and-albota", description="A python based discord bot", color=0x808080)
        embed.add_field(name="Join using", value="!join bot", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Club Website", url="https://github.com/ufosc/club-website", description="Our club website made using basic HTML, CSS, and JS.", color=0x00ecff)
        embed.add_field(name="Join using", value="!join clubsite", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Graphics Accelerator", url="https://github.com/ufosc/SiLGA", description="Simple Lightweight Graphics Accelerator (SiLGA)", color=0x7F6000)
        embed.add_field(name="Join using", value="!join graphics", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Muddy Swamp", url="https://github.com/ufosc/MuddySwamp", description="A UF themed python MUD game.", color=0x00630c)
        embed.add_field(name="Join using", value="!join muddyswamp", inline=True)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="Seg Fault", url="https://github.com/ufosc/seg-fault", description="Horror-based coding game made with the Unity engine", color=0xff0036)
        embed.add_field(name="Join using", value="!join fault", inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Projects(bot))
