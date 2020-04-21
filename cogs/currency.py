import discord
from .userdata.user import User
from discord.ext import commands


class Currency(commands.Cog):


    def __init__(self, client):
        self.client = client


    def help(self):
        return "CURRENCY HELP MENU"


    @commands.Cog.listener()
    async def on_ready(self):
        print('Currency cog is ready.')


    # Commands
    @commands.command()
    async def use(self, ctx, item):
        rstr = User.USERLIST[ctx.author.id].use(item)
        await ctx.send(rstr)


    @commands.command()
    async def inv(self, ctx):
    	rstr = User.USERLIST[ctx.author.id].getinv()
    	await ctx.send(rstr)


    # Later replace with some way of getting a pen and paper -> mix
    @commands.command()
    async def get_map(self, ctx):
    	User.USERLIST[ctx.author.id].add_inv('map')
                

def setup(client):
    client.add_cog(Currency(client))
