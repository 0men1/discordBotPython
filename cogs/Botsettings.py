import discord
import json
from discord.ext import commands

with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

class Botsettings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def changeprefix(self, ctx, prefix):
        if ctx.message.author.guild_permissions.administrator:
            prefixes[str(ctx.guild.id)] = prefix

            with open("prefixes.json", "w") as f:
                json.dump(prefixes,f, indent=4)

            await ctx.send(f"The prefix was changed to {prefix}")
        else:
            ctx.send(f"You cannot run that command")


    @commands.Cog.listener()
    async def on_message(self, message):
        mention = f'{self.client.user.id}'
        if mention in message.content:
            if message.mention_everyone is False:
                pre = prefixes[str(message.guild.id)]
                await message.channel.send(f'My prefix for this server is: {pre}')
        await self.client.process_commands(message)


    @commands.command(aliases=['game', 'changeGame'])
    async def setGame(self, ctx, *, message):
        if ctx.message.author.guild_permissions.administrator:
            await self.client.change_presence(activity = discord.Game(message))
            await ctx.send("Game has been set to "+message)
        else:
            await ctx.send("You cannot run that command")




def setup(client):
    client.add_cog(Botsettings(client))
