import config
import requests
from discord.ext import commands
from enum import Enum

class Query(Enum):
    GET_ORGANIZATION = """
    {
        organization(login:"ufosc") {
            members(first:10) {
                edges {
                    node {
                        name
                        avatarUrl
                    }
                }
            }
        }
    }
    """

class GitHub(commands.Cog,name="Git"):
    """The cog that handles the bulk of wrapping the GraphQL queries made to the GitHub v4 API."""
    def __init(self, bot):
        self.bot = bot

    headers = {"Authorization": "bearer {}".format(config.GITHUB_TOKEN)}

    def run(self, query: Enum):
        request = requests.post('https://api.github.com/graphql', json={'query': query.value}, headers=self.headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception('Failed to execute query with code {}. {}'.format(request.status_code, query.value))

    def get_organization_members(self):
        result = self.run(Query.GET_ORGANIZATION)
        print(result['data']['organization']['members'])


def setup(bot):
    bot.add_cog(GitHub(bot))
