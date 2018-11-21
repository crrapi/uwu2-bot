import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
import time
import asyncio
import asyncpg
from datetime import datetime
from utils import errorhandler

class marriage:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        if await self.bot.pool.fetchrow("SELECT * FROM user_settings WHERE user_id = $1", ctx.author.id):
           return True

        raise(errorhandler.hasUwU(ctx))

    @commands.command(descritpion="Marry your lover")
    async def marry(self,ctx,lover: discord.Member=None):
        async with self.bot.pool.acquire() as conn:
            if lover is None or lover is ctx.author:
                return await ctx.send("Trying to marry yourself...")
            if await conn.fetchrow("SELECT * FROM user_settings WHERE user_id = $1",lover.id) is None:
                return await ctx.send(f"{lover.name} does not have a uwulonian.")
            if await conn.fetchrow("SELECT * FROM marriages WHERE user1_id = $1 OR user2_id = $1 OR user1_id = $2 OR user2_id = $2", ctx.author.id, lover.id):
                return await ctx.send("Either you or the person you are trying to marry is already married...")

            msg = await ctx.send(f"""{lover.name} would you like to marry {ctx.author.name}. Reply "I do" to marry. Reply "No" to decline the marriage. This will timeout after 30 seconds.""")
            def check(amsg):
                return amsg.author == lover
            try:
                choice = await self.bot.wait_for('message', timeout=30, check=check)
            except asyncio.TimeoutError:
                return await msg.edit(content="Marriage timed out.")

            if choice.content == "I do":
                await conn.execute("INSERT INTO marriages (user1_id,user2_id) VALUES ($1,$2)", ctx.author.id, lover.id)
                await msg.delete()
                return await ctx.send(f"UwU! {lover.mention} has accepted {ctx.author.mention}'s proposal!")
            if choice.content == "No":
                await msg.delete()
                return await ctx.send(f"{ctx.author.mention} your lover ({lover.mention}) declined your marriage! There's a million fish in the sea though.")
            else:
                await msg.edit(content="Invalid choice")

    @commands.command(description="Divorce...")
    async def divorce(self,ctx):
        async with self.bot.pool.acquire() as conn:
            if await conn.fetchrow("SELECT * FROM marriages WHERE user1_id = $1 OR user2_id = $1",ctx.author.id) is None:
                return await ctx.send("You can't divorce someone your not married to.")

            await self.bot.pool.execute("DELETE FROM marriages WHERE user1_id = $1 OR user2_id = $1", ctx.author.id)
            await ctx.send(":broken_heart:")

def setup(bot):
    bot.add_cog(marriage(bot))