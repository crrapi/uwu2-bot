import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
import time
import asyncio
import asyncpg
from datetime import datetime
from utils import errorhandler
import secrets

heads = '<:uwuheads:517079577072238624>'
tails = '<:uwutails:517081802246979616>'

class uwus:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        if await self.bot.pool.fetchrow("SELECT * FROM user_settings WHERE user_id = $1", ctx.author.id):
           return True

        raise(errorhandler.hasUwU(ctx))

    @commands.command(aliases=['coinflip'])
    async def coin(self, ctx, choice, amount:int):
        async with self.bot.pool.acquire() as conn:
            user_amount = await conn.fetchrow("SELECT * FROM user_stats WHERE user_id = $1", ctx.author.id)
            choice = choice.lower()
            if amount < 50 or amount >= 100000:
                return await ctx.send("You may not bet less then 50 uwus or more than 100000 on a coinflip")
            if choice != "heads" and choice != "tails":
                return await ctx.send("Please only use heads or tails")
            if amount >= user_amount['uwus']:
                return await ctx.send("You don't have the funds to bet that much")

            status = await ctx.send("Flipping the coin...")
            await asyncio.sleep(3)
            await status.delete()
            side = secrets.choice(["heads", "tails"])
            if side == "heads":
                emote = heads
            else:
                emote = tails

            if choice == side:
                await conn.execute("UPDATE user_stats SET uwus = user_stats.uwus + $1 WHERE user_id = $2", amount, ctx.author.id)
                return await ctx.send(f"{emote} You won {amount} uwus!")
            else:
                await conn.execute("UPDATE user_stats SET uwus = user_stats.uwus - $1 WHERE user_id = $2", amount, ctx.author.id)
                return await ctx.send(f"{emote} You lost.")

def setup(bot):
    bot.add_cog(uwus(bot))