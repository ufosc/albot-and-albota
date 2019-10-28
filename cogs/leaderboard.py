import asyncio
import datetime

from discord.ext import commands

from github import Github
from config import GITHUB_TOKEN, LEADERBOARD

import discord
from discord.ext import commands
from database.database import SQLConnection, SQLCursor

# TODO: Generate an embeded image for top contributors
# TODO: Save info in the db
# TODO: Allow members to register their github login so that they will be @'d
# TODO: Track commits not on main branch
# TODO: In progress git integration, incomplete work

class Leaderboard(commands.Cog, name='Leaderboard'):
    """Handles GitHub leaderboard tracking for GitHub users."""

    def __init__(self, bot, db, git):
        self.bot = bot
        self.db = db
        self.git = git

    @commands.command()
    async def leaderboard(self, ctx):
        """Get top contributors of the month"""
        active_projects = ['club-website', 'muddyswamp', 'albot-and-albota', 'AskAGator', 'seg-fault', 'SiLGA']

        org = self.git.get_organization('ufosc')
        repos = []

        async with ctx.typing():
            for project in active_projects:
                repos.append(org.get_repo(project))

            topContributors = []
            for repo in repos:
                lastMonth = datetime.datetime.now() - datetime.timedelta(weeks=4)
                commits = repo.get_commits(since=lastMonth)

                repoContributors = []
                contributorList = []
                for commit in commits:
                    contributorList.append(commit.author.login)
                    if commit.author.login not in repoContributors:
                        repoContributors.append(commit.author.login)

                topContributor = ""
                contributions = 0
                for contributor in repoContributors:
                    count = contributorList.count(contributor)
                    if count > contributions:
                        topContributor = contributor
                        contributions = count

                if contributions is 0:
                    topContributors.append(("Nobody :(", 0))
                else:
                    topContributors.append((topContributor, contributions))

            message = "**Top Contributions This Month:**\n\n"
            i = 0
            for contributor in topContributors:
                repo = active_projects[i]
                message += "__**" + repo + "**__: **" + str(contributor[0]) + "** with " + str(contributor[1]) + " commits to dev!\n"
                i += 1

            message += "\nThank you for your hard work!"

        await ctx.send(message)
                

def setup(bot):
    git = Github(GITHUB_TOKEN)
    bot.add_cog(Leaderboard(bot, SQLConnection(), git))
