import discord
import random

from .userdata.resources.files import Files
from discord.ext import commands
from random import choice, randint


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self, command):
        if command is None:
            embed = discord.Embed(title="FUN COMMANDS")
            embed.description = "`8ball`, `roast`, `rankhot`, `howhot`, `rankthot`, `howthot`"
        else:
            embed = discord.Embed(title=command)
            if command == '8ball' or command == '_8ball':
                embed.description = '`reap 8ball <question>`: answers any mysterious question you ask it'
            elif command == 'roast':
                embed.description = '`reap roast/joke <user>`: roasts who you tag (or yourself if you dont tag anyone)'
            elif command == 'rankhot' or command == 'howhot':
                embed.description = '`reap rankhot/howhot [<user>]`: ranks hotness from a scale of 0 - 100'
            elif command == 'rankthot' or command == 'howthot':
                embed.description = '`reap rankthot/howthot [<user>]`: ranks thottiness from a scale of 0 - 100'
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog is ready.')

    # Commands
    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain',
                     'It is decidedly so',
                     'Without a doubt',
                     'Yes - definitely',
                     'You may rely on it',
                     'As I see it, yes',
                     'Most likely',
                     'Reply hazy, try again',
                     'Better not tell you now',
                     'Cannot predict now',
                     'Concentrate and ask again',
                     "Don't count on it",
                     'My reply is no',
                     'Outlook not so good',
                     'Very doubtful',
                     'Definitely not']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

    @commands.command()
    async def roast(self, ctx, *, target: discord.User = None):
        if target is None:
            msg = "You're so dumb, you decided to roast yourself! Tag someone you dumb prick."
        else:
            msg = target.display_name + ", "
            lines = Files.read('roasts.txt')
            msg += choice(lines).rstrip('\n')
        await ctx.send(msg)

    @commands.command(aliases=['howhot'])
    async def rankhot(self, ctx, *, target: discord.User = None):
        percent = randint(0, 100)
        if target is None:
            msg = "You are " + str(percent) + " percent hot."
        else:
            msg = target.display_name + " is " + str(percent) + " percent hot."
        await ctx.send(msg)

    @commands.command(aliases=['howthot'])
    async def rankthot(self, ctx, *, target: discord.User = None):
        percent = randint(0, 100)
        if target is None:
            msg = "You are " + str(percent) + " percent thot."
        else:
            msg = target.display_name + " is " + str(percent) + " percent thot."
        await ctx.send(msg)


def setup(client):
    client.add_cog(Fun(client))
