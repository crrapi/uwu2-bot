import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
from utils import errorhandler
import asyncpg

beta_servers = [513888506498646052]

class beta:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        if ctx.guild.id in beta_servers:
           return True

        raise(errorhandler.isBeta(ctx))

    @commands.command()
    async def trivia(self,ctx):
        await ctx.send('Test')


def setup(bot):
    bot.add_cog(beta(bot))