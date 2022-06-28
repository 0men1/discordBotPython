import discord
from discord.ext import commands
from platform import platform
from riotwatcher import LolWatcher

apiKey = 'RGAPI-e33bbbdc-706c-45e7-b921-daba0b6c9e36'
watcher = LolWatcher(apiKey)

class valorantMatch(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def profileLeague(self, ctx):
        summoner = 'Still Stunned'

        val = watcher.summoner.by_name('NA1', summoner)

        await ctx.send(val)


def setup(client):
    client.add_cog(valorantMatch(client))