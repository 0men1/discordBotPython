import discord
import json
import random
from discord.ext import commands

with open('mainBank.json', 'r') as f:
    bank = json.load(f)

class economy(commands.Cog):
    def __init__(self, client):
        self.client = client
    


    #SETS UP BANK
    @commands.command()
    async def setupbank(self, ctx):
        if f'{ctx.author.id}' in bank:
            await ctx.send('You are already registered ✅')
        else:
            await self.add_bank(bank, ctx.author)
            await ctx.send('You are now registered')
        with open('mainBank.json', 'w') as f:
            json.dump(bank, f, indent=4)



    #REMOVES BANK
    @commands.command()
    async def removebank(self, ctx):
        if not f'{ctx.author.id}' in bank:
            await ctx.send('You were not registered')
        else:
            bank.pop(str(ctx.author.id))
        with open('mainBank.json', 'w') as f:
            json.dump(bank, f, indent=4)



    # BEG COMMAND
    @commands.command()
    async def beg(self, ctx):
        member = ctx.author.id
        await self.bank_check(ctx, bank, member)
        money = random.randint(0, 50)
        if money > 0:
            await self.add_money_wallet(bank, ctx.author, money)
            em = discord.Embed(color = 0x992d22)
            em.add_field(name='YAY', value='You begged so hard that you got {} 🪙'.format(money))
            await ctx.send(embed = em)
        else:
            em = discord.Embed(color = 0x992d22)
            em.add_field(name = 'Booo',value='Try begging harder. You got nothing')
            await ctx.send(embed = em)



    @commands.command()
    async def bank(self, ctx, member: discord.Member):
        if f'{member.id}' in bank:
            walletMoney = bank[f'{member.id}']['Wallet']
            bankMoney = bank[f'{member.id}']['Bank']
            em = discord.Embed(color = 0x992d22, name='The Bank')
            em.add_field(name='Wallet', value='{} 🪙'.format(walletMoney))
            em.add_field(name='Bank', value = '{} 🪙'.format(bankMoney))
            await ctx.send(embed = em)    



    @commands.command()
    async def deposit(self, ctx, *,amount:int):
        member = ctx.author.id        
        await self.bank_check(ctx, bank, member)
        if bank[f'{member}']['Wallet'] < amount:
            em = discord.Embed(color = 0x992d22, name='WARNING')
            em.add_field(name='ACTION NEEDED!', value = 'You do not have that much money in your wallet')
            await ctx.send(embed = em)
        else:
            bank[f'{member}']['Wallet'] -= amount
            bank[f'{member}']['Bank'] += amount
            with open('mainBank.json', 'w') as f:
                json.dump(bank, f, indent=4)
            em = discord.Embed(name='ACTION')
            em.add_field(name='ACTION', value = 'You have deposited {}🪙 into your bank'.format(amount))
            await ctx.send(embed = em)



    @commands.command()
    async def withdraw(self, ctx, *, amount:int):
        member  = ctx.author.id
        await self.bank_check(ctx, bank, member)
        if bank [f'{member}']['Bank'] < amount:
            em = discord.Embed(color = 0x992d22, name='WARNING')
            em.add_field(name='ACTION NEEDED!', value = 'You do not have that much money in your bank')
            await ctx.send(embed = em)
        else:
            bank[f'{member}']['Wallet'] += amount
            bank[f'{member}']['Bank'] -= amount
            with open('mainBank.json', 'w') as f:
                json.dump(bank, f, indent=4)
            em = discord.Embed(name='ACTION')
            em.add_field(name='ACTION', value = 'You have withdrawn {}🪙'.format(amount))
            await ctx.send(embed = em)



    async def bank_check(self, ctx, bank, user):
        if not f'{user}' in bank:
            await ctx.send('You are not registered')



    async def add_money_wallet(self, bank, user, amount):
        bank[f'{user.id}']['Wallet'] += amount
        with open('mainBank.json', 'w') as f:
            json.dump(bank, f, indent=4)

    async def add_bank(self, bank, user):
        if not f'{user.id}' in bank:    
            bank[f'{user.id}'] = {}
            bank[f'{user.id}']['Bank'] = 0
            bank[f'{user.id}']['Wallet'] = 0




def setup(client):
    client.add_cog(economy(client))
