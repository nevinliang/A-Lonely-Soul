import discord
from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, command):
        if command is None:
            embed = discord.Embed(title="MODERATION COMMANDS")
            embed.description = "`ping`, `purge`, `clear`, `kick`, `ban`, `unban`"
        else:
            embed = discord.Embed(title=command)
            if command == 'ping':
                embed.description = '`reap ping`: gets the ping time to the bot'
            elif command == 'purge' or command == 'clear':
                embed.description = '`reap purge/clear [<amount>=5]`: purges a number of messages from the channel'
            elif command == 'kick':
                embed.description = '`reap kick <user>`: kicks user from the server'
            elif command == 'ban':
                embed.description = '`reap ban <user>`: bans user from the server'
            elif command == 'unban':
                embed.description = '`reap unban <user>: unbans them from the server'
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation cog is ready.')

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['clear'])
    async def purge(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention}')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention}')

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return


def setup(client):
    client.add_cog(Moderation(client))
