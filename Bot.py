import discord
import os
from discord.ext import commands


client = commands.Bot(command_prefix='reap ')
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="reap help"))
    print('Bot is ready.')


@client.event
async def on_member_join(member):
    print(f'{member} has joined this server.')


@client.event
async def on_member_remove(member):
    print(f'{member} has left this server.')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


@client.command()
async def invite(ctx):
    embed = discord.Embed(title="INVITE LINK",
                       url='https://discordapp.com/api/oauth2/authorize?client_id=687476783297462312&permissions=8&scope=bot',
                       description='DM an admin for premium!')
    embed.set_image(url='https://i.ibb.co/YLn9RRL/Blob-Reaper-copy2.png')
    await ctx.channel.send(embed=embed)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run('Njg3NDc2NzgzMjk3NDYyMzEy.XptoYA.GMui_0mrbz3U4bKH1xJtdopoP7I')
