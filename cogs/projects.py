import discord
from discord.ext import commands

class Projects:
    '''Commands dealing with the different projects we are working on'''

    def __init__(self, bot):
        self.bot = bot
    

    async def muddy(self, ctx):
        """Add the muddy swamp role to the user"""
        role = get(ctx.message.server.roles, name="muddy-swamp")
        await self.bot.add_roles(ctx.message.author, role)
        await self.bot.say("Get out of my swamp!")
        with open('get-out-of-my-swamp.jpg', 'rb') as f:
            await self.bot.send_file(ctx.message.channel, f)

    async def website(self, ctx):
        """Add the website role to the user"""
        role = get(ctx.message.server.roles, name="club-website")
        await self.bot.add_roles(ctx.message.author, role)
        await self.bot.say("HTML is my favorite programming language.")

    async def mvw(self, ctx):
        """Add the marston vs west role to the user"""
        role = get(ctx.message.server.roles, name="marston-vs-west")
        await self.bot.add_roles(ctx.message.author, role)
        await self.bot.say("Newell is the best 24/7 library. Don't @ me")

    @commands.command(pass_context=True)
    async def join(self, ctx, *, roleName: str):
        """Add a role to a user"""
        if roleName.lower() in ["muddy", "muddy swamp", "muddyswamp", "muddy-swamp", "MUD"]:
            await mudd(ctx)
        elif roleName.lower() in ["website", "club site", "club website", "clubwebsite", "clubsite"]:
            await website(ctx)
        elif roleName.lower() in ["mvw", "marstonvswest", "marston vs west", "marston v west"]:
            await mvw(ctx)

    @commands.command()
    async def list(self):
        """Print the list of the current projects we are working on."""
        embed=discord.Embed(title="Muddy Swamp", url="https://github.com/ufosc/MuddySwamp", description="A UF themed python MUD game.", color=0x00630c)
        embed.add_field(name="Join using", value="!join muddyswamp", inline=True)
        await self.bot.say(embed=embed)

        embed=discord.Embed(title="Marston Vs West", url="https://github.com/ufosc/marston-vs-west", description="A HTML5 smashbros-esque game fitting our libraries against each other.", color=0xff0036)
        embed.add_field(name="Join using", value="!join mvw", inline=True)
        await self.bot.say(embed=embed)
        
        embed=discord.Embed(title="Club Website", url="https://github.com/ufosc/club-website", description="Our club website made using basic HTML, CSS, and JS.", color=0x00ecff)
        embed.add_field(name="Join using", value="!join clubsite", inline=True)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Projects(bot))
