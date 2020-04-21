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


    @commands.command()
    async def coins(self, ctx, other=None):
        if other is None:
            coins = User.USERLIST[ctx.author.id].inv.coins
            await ctx.send(f"You have {coins} coins")
        else:
            coins = User.USERLIST[int(other[3:-1])].inv.coins
            await ctx.send(f"They have {coins} coins")


    @commands.command()
    async def work(self, ctx):
        nowtime = datetime.now().replace(microsecond=0)
        ok = False
        if 'work' not in User.USERLIST[ctx.author.id].wait.keys():
            ok = True
        else:
            lasttime = datetime.strptime(User.USERLIST[ctx.author.id].wait['work'], '%Y-%m-%d/%H:%M:%S')
            diff = (nowtime - lasttime).total_seconds()
            ok = diff >= 600
        if ok:
            User.USERLIST[ctx.author.id].wait['work'] = str(nowtime.strftime("%Y-%m-%d/%H:%M:%S"))
            lines = Files.read("sentences.txt")
            rint = randint(0, len(lines) - 1)
            line = 'Retype the following line: `' + global_temp[author] + '`'
            try:
                answer = await self.client.wait_for('message', timeout=20.0)
            except:
                await ctx.send('You are too slow!')
                return
            if answer.content[1:] == line[1:]:
                msg = 'Nice job! You earned 500 coins.'
                User.USERLIST[ctx.author.id].coins += 500
            else:
                msg = 'Bruh do you know how to type? Go back to middle school.'
            await ctx.send(msg)
        else:
            msg = "You have to wait a little before working.\n" + \
                str((600 - int(diff)) // 60) + " minutes " + str(int(900 - diff) % 60) + \
                " seconds until you can work again"
        await ctx.send(msg)


def setup(client):
    client.add_cog(Currency(client))
