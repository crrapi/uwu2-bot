from discord.ext import commands
import discord
from utils import errorhandler
import asyncpg

staff_ids = [246938839720001536, 300088143422685185]

class owner:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        if ctx.author.id in staff_ids:
           return True

        raise(errorhandler.IsStaff(ctx))

    @commands.command(hidden=True)
    async def plonk(self,ctx,user_id):
        await self.bot.pool.execute("DELETE FROM user_settings WHERE user_id = $1",user_id)
        await self.bot.pool.execute("DELETE FROM user_timers WHERE user_id = $1",user_id)

        await ctx.send('Done')

    @commands.group(invoke_without_command=True, description="Does nothing without a subcommand")
    async def patreon(self, ctx):
        await ctx.send("owo")

    @patreon.command(hidden=True)
    async def set(self,ctx,user_id:int):
        try:
            await self.bot.pool.execute("INSERT INTO p_users (user_id) VALUES ($1)",user_id)
            await ctx.send("Done")
        except asyncpg.UniqueViolationError:
            return await ctx.send(f"{user_id} is already a Patron")

    @patreon.command(hidden=True)
    async def remove(self,ctx,user_id:int):
        await self.bot.pool.execute("DELETE FROM p_users WHERE user_id = $1",user_id)
        await ctx.send("Done")

def setup(bot):
    bot.add_cog(owner(bot))