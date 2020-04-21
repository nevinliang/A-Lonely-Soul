import discord
from discord.ext import commands


class HelpMenus(commands.Cog):


    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print('HelpMenus cog is ready.')


    # Commands
    @commands.command()
    async def help(self, ctx, *, question=None):
        if question == None:
            await ctx.send(f'Help Menu')
        else:
            bot = self.client.get_cog(question.capitalize())
            if bot is not None:
                await ctx.send(bot.help())
                

def setup(client):
    client.add_cog(HelpMenus(client))
