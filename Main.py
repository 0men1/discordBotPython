import discord
from discord.ext import commands
import json
import os

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix, intents = discord.Intents.all())

client.remove_command("help")

os.chdir(r'/Users/HomenHoma/MyCodingProjects/Discordpy/discordBotPython')

with open('users.json', 'r') as f:
    users = json.load(f)
with open('mainBank.json', 'r') as f:
    bank = json.load(f)
with open('prefixes.json','r') as f:
    prefixes = json.load(f)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')    


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('cog loaded!')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('cog unloaded')

@client.command()
async def reload(ctx, extension):
    if ctx.message.author.guild_permissions.administrator:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send('cog reloaded')
    else:
        await ctx.send('You cannot run this command')


#---------------------------------------------------------------ON GUILD JOIN/REMOVE ------------------------------------------------------------------------
@client.event
async def on_guild_join(guild):
    prefixes[str(guild.id)] = '!'
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

#------------------------------------------------BOT SETTINGS ------------------------------------------------

@client.event
async def on_ready():
    print('Logged on as', client.user)
    print('Bot is ready')

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='bot-bitch')
    await channel.send(f"Welcome to the discord {member.mention}")
    await member.send("Welcome to the bubby's server!")

@client.event
async def on_member_remove(member):
    if f'{member.id}' in bank:
        bank.pop(str(f'{member.id}'))

        with open('mainBank.json', 'w') as f:
            json.dump (bank, f, indent=4)

    if f'{member.id}' in users:
        users.pop(str(f'{member.id}'))
        with open('users.json', 'w') as f:
            json.dump(users, f, indent = 4)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

#---------------------------------------------------------------------------- END ---------------------------------------------------------
client.run('NTMzNDc3MDI1NDQ5NzcxMDMx.GdycIt.OkPeENaPlywFu0HMJzYw4CijzS5o3XVIpkAr_s')