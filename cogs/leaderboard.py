import asyncio
import datetime

from github import PaginatedList
from github import Github

from config import GITHUB_TOKEN
from cogs.CONSTANTS import LEADERBOARD

import discord
from discord.ext import commands
from database.database import SQLConnection, SQLCursor

class Leaderboard(commands.Cog, name='Leaderboard'):
    """Handles GitHub leaderboard tracking for GitHub users."""
    def __init__(self, bot, db, git):
        self.bot = bot
        self.db = db
        self.git = git
        # This is the leaderboard channel id, please configure in config.py
        self.channel = self.bot.get_channel(LEADERBOARD)
        # loop = asyncio.get_event_loop()
        # self.r = loop.create_task(self.initialize())

    # async def initialize(self):
    #     while True:
    #         org = self.git.get_organization('ufosc')
    #         contributors = []
    #         for project in self.active_projects:
    #             events = org.get_repo(project).get_events()
    #             await self.limit_events(events)
    #             # print([branch.commit.commit.html_url for branch in repo.get_branches()])
    #             # date = datetime(year=datetime.today().year, month=datetime.today().month, day=1)
    #             # commits = repo.get_commits(since=date, until=datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, hour=datetime.today().hour, minute=datetime.today().minute))
    #             # [contributors.append(str(commit.commit.html_url)) for commit in commits if str(commit.commit.author.name) not in contributors]
    #         # print(str([contributor for contributor in contributors]))
    #          # update leaderboard every hour (3600)
    #     return self

    # async def limit_events(self, events: PaginatedList) -> PaginatedList:
    #     date = datetime(year=datetime.today().year, month=datetime.today().month, day=1)
    #     current = datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, hour=datetime.today().hour, minute=datetime.today().minute)
    #     limited_events = []
    #     for event in events:
    #         print('Event Type: ' + event.type)
    #         if event.type is 'PushEvent' and date > event.created_at and event.created_at <= current:
    #             []

    @commands.command()
    async def leaderboard(self, ctx):
        """Get top contributors of the month"""
        active_projects = ['club-website', 'muddyswamp', 'albot-and-albota', 'AskAGator']

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

                topContributors.append((topContributor, contributions))

            message = "**Top Contributions This Month:**\n\n"
            i = 0
            for contributor in topContributors:
                repo = active_projects[i]
                message += "__**" + repo + "**__: *" + str(contributor[0]) + "* with " + str(contributor[1]) + " commits to dev!\n"
                i += 1

            message += "\nThank you for your hard work!"

        await ctx.send(message)
                

def setup(bot):
    git = Github(GITHUB_TOKEN)
    bot.add_cog(Leaderboard(bot, SQLConnection(), git))

