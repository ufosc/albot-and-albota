import asyncio

from github import PaginatedList
from github import Github

import config
import discord
from discord.ext import commands
from database.database import SQLConnection, SQLCursor
from datetime import datetime

class Leaderboard(commands.Cog, name='Leaderboard'):
    """Handles GitHub leaderboard tracking for GitHub users."""
    def __init__(self, bot, db, git):
        self.bot = bot
        self.db = db
        self.git = git
        # This is the leaderboard channel id, please configure in config.py
        self.channel = self.bot.get_channel(int(config.LEADERBOARD_ID))
        loop = asyncio.get_event_loop()
        self.r = loop.create_task(self.initialize())

    active_projects = ['club-website', 'muddyswamp', 'albot-and-albota', 'AskAGator', 'club-back-end', 'marston-vs-west', 'club-admin-portal']

    async def initialize(self):
        while True:
            org = self.git.get_organization('ufosc')
            contributors = []
            for project in self.active_projects:
                events = org.get_repo(project).get_events()
                await self.limit_events(events)
                # print([branch.commit.commit.html_url for branch in repo.get_branches()])
                # date = datetime(year=datetime.today().year, month=datetime.today().month, day=1)
                # commits = repo.get_commits(since=date, until=datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, hour=datetime.today().hour, minute=datetime.today().minute))
                # [contributors.append(str(commit.commit.html_url)) for commit in commits if str(commit.commit.author.name) not in contributors]
            # print(str([contributor for contributor in contributors]))
             # update leaderboard every hour (3600)
        return self

    async def limit_events(self, events: PaginatedList) -> PaginatedList:
        date = datetime(year=datetime.today().year, month=datetime.today().month, day=1)
        current = datetime(year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, hour=datetime.today().hour, minute=datetime.today().minute)
        limited_events = []
        for event in events:
            print('Event Type: ' + event.type)
            if event.type is 'PushEvent' and date > event.created_at and event.created_at <= current:
                []


def setup(bot):
    git = Github(config.GITHUB_TOKEN)
    bot.add_cog(Leaderboard(bot, SQLConnection(), git))

