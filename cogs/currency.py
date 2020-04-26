from random import randint
from random import choice

import discord
from .userdata.resources.files import Files
from .userdata.user import User
from discord.ext import commands
from datetime import datetime


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
        rstr = User.USER_LIST[ctx.author.id].use(item)
        await ctx.send(rstr)

    @commands.command()
    async def inv(self, ctx):
        rstr = User.USER_LIST[ctx.author.id].getinv()
        await ctx.send(rstr)

    # Later replace with some way of getting a pen and paper -> mix
    @commands.command()
    async def get_map(self, ctx):
        User.USER_LIST[ctx.author.id].add_inv('map')

    @commands.command()
    async def coins(self, ctx, other=None):
        if other is None:
            coins = User.USER_LIST[ctx.author.id].inv.coins
            await ctx.send(f"You have {coins} coins")
        else:
            coins = User.USER_LIST[int(other[3:-1])].inv.coins
            await ctx.send(f"They have {coins} coins")

    @commands.command()
    async def work(self, ctx):
        now_time = datetime.now().replace(microsecond=0)
        diff = 0

        ok = False
        if 'work' not in User.USER_LIST[ctx.author.id].wait.keys():
            ok = True
        else:
            last_time = datetime.strptime(User.USER_LIST[ctx.author.id].wait['work'], '%Y-%m-%d/%H:%M:%S')
            diff = (now_time - last_time).total_seconds()
            ok = diff >= 600

        if ok:
            User.USER_LIST[ctx.author.id].wait['work'] = str(now_time.strftime("%Y-%m-%d/%H:%M:%S"))
            lines = Files.read('sentences.txt')
            ans = lines[randint(0, len(lines) - 1)].rstrip('\n')
            line = 'Retype the following line: `' + ans + '`'
            await ctx.send(line)

            def check(m):
                return m.author == ctx.author

            try:
                answer = await self.client.wait_for('message', check=check, timeout=20.0)
            except:
                await ctx.send('You are too slow!')
                return

            if answer.content[1:] == ans[1:]:
                msg = 'Nice job! You earned 500 coins.'
                User.USER_LIST[ctx.author.id].inv.coins += 500
            else:
                msg = 'Bruh do you know how to type? Go back to middle school.'

            await ctx.send(msg)

        else:
            msg = "You have to wait a little before working.\n" + \
                  str((600 - int(diff)) // 60) + " minutes " + str(int(900 - diff) % 60) + \
                  " seconds until you can work again"
            await ctx.send(msg)

    @commands.command()
    async def search(self, ctx):
        now_time = datetime.now().replace(microsecond=0)
        diff = 0

        ok = False
        if 'search' not in User.USER_LIST[ctx.author.id].wait.keys():
            ok = True
        else:
            last_time = datetime.strptime(User.USER_LIST[ctx.author.id].wait['search'], '%Y-%m-%d/%H:%M:%S')
            diff = (now_time - last_time).total_seconds()
            ok = diff >= 1

        if ok:
            User.USER_LIST[ctx.author.id].wait['search'] = str(now_time.strftime("%Y-%m-%d/%H:%M:%S"))
            rint = randint(1, 12)
            if rint < 4:
                msg = 'Rip. You didnt find anything.'
            else:
                searchable_items = ['pen', 'cloth', 'woodenchest', 'paper']
                if rint < 10:
                    amt = randint(40, 60)
                    item = str(amt) + ' coins'
                    User.USER_LIST[ctx.author.id].inv.coins += amt
                else:
                    item = choice(searchable_items)
                    User.USER_LIST[ctx.author.id].inv.add_inv(item)
                    item = '1 ' + item
                msg = 'Wow. You have received ' + item

            await ctx.send(msg)

        else:
            msg = "You have to wait a little before searching again.\n" + \
                  str(int(25 - diff)) + " seconds until you can search again"
            await ctx.send(msg)


def setup(client):
    client.add_cog(Currency(client))
