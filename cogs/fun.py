import discord
import random
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    def help(self):
        return "FUN HELP MENU"

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


def setup(client):
    client.add_cog(Fun(client))
