import discord
from discord.ext import commands


class ServerFunctions(commands.Cog):
    def __init__(self, client):
        self.client = client
            
    @commands.command()
    async def ban(self, ctx, member:discord.Member, *,reason):
        await member.ban(reason = reason)
        em = discord.Embed(color = 0x992d22)
        em.add_field(name='🚫BANNED🚫', value=f'Banned {member.mention}')
        await ctx.send(embed = em)


    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                em = discord.Embed(color = 0x992d22)
                em.add_field(name='UNBANNED', value=f'Unbanned {member.mention}')
                await ctx.send(embed = em)
                return


    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(color = 0x992d22, title ='HELP', description="Explanation of everything I can do")
        embed.set_author(name = ctx.author.display_name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="Ping", value="This will return pong", inline=True)
        embed.add_field(name="ban (user)", value="This will ban a member of your server. You must include a reason. \n EXAMPLE: !ban @user (reason)", inline=True)
        embed.add_field(name="unban (user)", value="This will unban a member of your server. You must include a reason. \n EXAMPLE:!unban DJ Z #9329", inline=True)
        embed.add_field(name="setGame or game or changeGame", value="This will change the game that I am playing at this current moment. \n EXAMPLE: !setGame Valorant or !game Valorant or !changeGame valorant", inline=True)
        embed.add_field(name="avatar or av", value="Checks the avatar of the mentioned user \n EXAMPLE: !av @DJ Z or !avatar @DJ Z")
        await ctx.send(embed = embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member):
        embed= discord.Embed(color = 0x992d22, title="Avatar")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed = embed)


def setup(client):
    client.add_cog(ServerFunctions(client))