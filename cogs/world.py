import discord
import os
from discord.ext import commands
from random import choice
from .userdata.user import User
from .userdata.inventory import Inv


class World(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Game vars
        self.world = None       # 25x25 world map

    def help(self):
        return "WORLD HELP MENU"

    @commands.Cog.listener()
    async def on_ready(self):
        for server in self.client.guilds:
            self.world = self.init_world()
            members = [str(i.id) for i in server.members]
            for i in server.members:
                User(i.id)      # create instance stored in User class
        print('World cog is ready.')


    # Helper functions
    def init_world(self):
        choices = '.....m.........m........M$'
        return [[choice(choices) for i in range(25)] for j in range(25)]


    def has_map(self, id):
        return 'map' in User.USERLIST[id].inv.list.keys()


    def user_map(self, id):
        [x, y] = User.USERLIST[id].pos
        pstr = 'YOUR USER MAP\n==============\n'
        for i in range(max(0, x - 3), min(20, x + 4)):
            for j in range(max(0, y - 3), min(20, y + 4)):
                pstr += ('X' if (i == x and j == y) else self.world[i][j]) + ' '
            pstr += '\n'
        return pstr


    def interact(self, id):
        [x, y] = User.USERLIST[id].pos
        if self.world[x][y] == '$':
            choices = 'wwwwwwwwwwwwwwwwiiiiiiii'
            chest_map = {'w':'wooden', 'i':'iron', 'g':'gold', 'd':'diamond', 'f':'fire'}
            chest = chest_map[choice(choices)]
            if self.world[x][y] == '$':
                qstr = f'You have discovered a {chest} chest!'
                User.USERLIST[id].add_inv(chest + 'chest')
                return qstr
        else:
            return None


    # Commands
    @commands.command(aliases=['step'])
    async def move(self, ctx, direction):
        if self.has_map(ctx.author.id):
            User.USERLIST[ctx.author.id].move(direction)
            qstr = self.interact(ctx.author.id)
            pstr = '`' + self.user_map(ctx.author.id) + '`'
            embed = discord.Embed(description=pstr, color=0x00ffff)
            await ctx.send(embed=embed)
            if qstr is not None:
                await ctx.send(qstr)	
        else:
            await ctx.send("You don't have access to the hidden world yet.")


    @commands.command(aliases=['position', 'coordinates', 'at'])
    async def pos(self, ctx):
        if self.has_map(ctx.author.id):
            [x, y] = User.USERLIST[ctx.author.id].pos
            await ctx.send(f'({x}, {y})')
        else:
            await ctx.send("You don't have access to the hidden world yet.")


    @commands.command()
    async def matrix(self, ctx):
        if self.has_map(ctx.author.id):
            pstr = 'THE WORLD MATRIX\n=================\n'
            for i in range(20):
                pstr += " ".join(self.world[i]) + '\n'
            pstr = '`' + pstr + '`'
            embed = discord.Embed(description=pstr, color=0x00ffff)
            await ctx.send(embed=embed)
        else:
            await ctx.send("You don't have access to the hidden world yet.")


    @commands.command(aliases=['grid'])
    async def map(self, ctx):
        if self.has_map(ctx.author.id):
            pstr = self.user_map(ctx.author.id)
            await ctx.send('`' + pstr + '`')
        else:
            await ctx.send("You don't have access to the hidden world yet.")


    @commands.command(aliases=['mix', 'brew', 'make', 'forge'])
    async def create(self, ctx):
        await ctx.send("What items would you like to use? Format: {item} {amount}")

        def check(m):
            return m.content[0] in Inv.ITEMS and m.content[1].isdigit()

        try:
            item1 = await self.client.wait_for('message', timeout=30.0)
            item2 = await self.client.wait_for('message', timeout=30.0)
        except:
            await ctx.send('There was something wrong with what you entered!')

        val = User.USERLIST[ctx.author.id].mix([item1.content, item2.content])
        if val is not None:
            await ctx.send('You have created a ' + val)
        else:
            await ctx.send('That is not a valid recipe')


def setup(client):
    client.add_cog(World(client))

