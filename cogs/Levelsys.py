from discord.ext import commands
import json
import discord

with open('users.json', 'r') as f:
    users = json.load(f)
with open('mainBank.json', 'r') as f:
    bank = json.load(f)

class Levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.client.user:        
            await self.update_data(users, message.author)
            await self.add_experience(users, message.author, 2)
            await self.level_up(users, message.author, message.channel)

            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)

    @commands.command()
    async def profile(self, ctx, member: discord.Member):
        experience = users[f'{member.id}']['experience']
        level = users[f'{member.id}']['level']
        em = discord.Embed(color = 0x992d22, title ='Profile')
        em.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
        em.add_field(name='Level', value='Level: {}'.format(level), inline=True)
        em.add_field(name='XP', value = 'Experience: {}'.format(experience))
        await ctx.send(embed = em)


    async def update_data(self, users, user):
        if not f'{user.id}' in users:    
            users[f'{user.id}'] = {}
            users[f'{user.id}']['experience'] = 0
            users[f'{user.id}']['level'] = 1

    async def add_experience(self, users, user, exp):
        users[f'{user.id}']['experience'] += exp

    async def level_up(self, users, user, channel):
        experience = users[f'{user.id}']['experience']
        lvl_start = users[f'{user.id}']['level']
        lvl_end = int(experience ** (1/3))

        if lvl_end > lvl_start:
            await channel.send('{} has leveled up to level {}'.format(user.mention, lvl_end)) 
            users[f'{user.id}']['level'] = lvl_end


def setup(client):
    client.add_cog(Levelsys(client))