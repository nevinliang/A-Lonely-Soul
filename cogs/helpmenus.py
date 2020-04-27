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
    async def help(self, ctx, question=None, command=None):
        if question is None:
            e = discord.Embed(title='HELP MENU')
            e.description = ':tools: Moderation\n`reap help moderation`\n\n' + \
                            ':grinning: Fun\n`reap help fun`\n\n' + \
                            ':earth_americas: World\n`reap help world`\n\n' \
                            ':moneybag: Currency\n`reap help currency`'
            await ctx.send(embed=e)
        else:
            bot = self.client.get_cog(question.capitalize())
            if bot is not None:
                await ctx.send(embed=bot.help(command))


def setup(client):
    client.add_cog(HelpMenus(client))
