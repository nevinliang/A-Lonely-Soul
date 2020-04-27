import discord
from discord.ext import commands
from discord.ext import tasks
from random import choice
from .userdata.user import User


class World(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Game vars
        self.world = None  # 25x25 world map
        self.w_size = 25

    def help(self, command):
        if command is None:
            embed = discord.Embed(title="WORLD COMMANDS")
            embed.description = "`move`, `pos`, `position`, `coordinates`, `at`, `matrix`, `map`, `grid`, `create`, " \
                                "`mix`, `brew`, `make`, `forge`"
        else:
            embed = discord.Embed(title=command)
            if command == 'move':
                embed.description = '`reap move <direction=right, left, up, down>`: moves in a direction on the map'
            elif command == 'pos' or command == 'position' or command == 'coordinates' or command == 'at':
                embed.description = '`reap pos/position/coordinates/at`: gets your coordinates on the world map'
            elif command == 'matrix':
                embed.description = '`reap matrix`: gets the entire world map'
            elif command == 'map' or command == 'grid':
                embed.description = '`reap map/grid`: gets your small map position of nearby areas'
            elif command in ['create', 'mix', 'brew', 'make', 'forge']:
                embed.description = '`reap create/mix/brew/make/forge: forge new items'
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        for server in self.client.guilds:
            self.world = self.init_world()
            members = [str(i.id) for i in server.members]
            for i in server.members:
                User(i.id)  # create instance stored in User class
        self.update_map.start()
        print('World cog is ready.')

    # Helper functions
    def init_world(self):
        choices = '.....m.........m........M$'
        return [[choice(choices) for i in range(self.w_size)] for j in range(self.w_size)]

    def has_map(self, id):
        return 'map' in User.USER_LIST[id].inv.list.keys()

    def user_map(self, id):
        [x, y] = User.USER_LIST[id].pos
        pstr = 'YOUR USER MAP\n==============\n'
        for i in range(max(0, x - 3), min(self.w_size, x + 4)):
            for j in range(max(0, y - 3), min(self.w_size, y + 4)):
                pstr += ('X' if (i == x and j == y) else self.world[i][j]) + ' '
            pstr += '\n'
        return pstr

    def interact(self, id):
        [x, y] = User.USER_LIST[id].pos
        if self.world[x][y] == '$':
            choices = 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwiiiiiiiiiiiiiiiigggggddf'
            chest_map = {'w': 'wooden', 'i': 'iron', 'g': 'gold', 'd': 'diamond', 'f': 'fire'}
            chest = chest_map[choice(choices)]
            if self.world[x][y] == '$':
                qstr = f'You have discovered a {chest} chest!'
                User.USER_LIST[id].add_inv(chest + 'chest')
                return qstr
            self.world[x][y] = '.'
        else:
            return None

    # Commands
    @commands.command(aliases=['step'])
    async def move(self, ctx, direction=None):
        if self.has_map(ctx.author.id):
            if direction is None:
                await ctx.send("Specify a direction dumbass.")
            else:
                User.USER_LIST[ctx.author.id].move(direction)
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
            [x, y] = User.USER_LIST[ctx.author.id].pos
            await ctx.send(f'({x}, {y})')
        else:
            await ctx.send("You don't have access to the hidden world yet.")

    @commands.command()
    async def matrix(self, ctx):
        if self.has_map(ctx.author.id):
            pstr = 'THE WORLD MATRIX\n=================\n'
            for i in range(self.w_size):
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

        item1 = await self.client.wait_for('message', timeout=30.0)
        item2 = await self.client.wait_for('message', timeout=30.0)

        val = User.USER_LIST[ctx.author.id].mix([item1.content, item2.content])
        if val is not None:
            await ctx.send('You have created a ' + val)
        else:
            await ctx.send('That is not a valid recipe')

    @tasks.loop(seconds=3600)
    async def update_map(self):
        self.world = self.init_world()


def setup(client):
    client.add_cog(World(client))
