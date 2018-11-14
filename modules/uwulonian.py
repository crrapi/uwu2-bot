import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
import time
import asyncio
import asyncpg
from datetime import datetime, timedelta
from random import randint

class uwulonian:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Get an uwulonians or your stats')
    async def stats(self,ctx,user: discord.Member=None):
        user = user or ctx.author
        uwulonian_name = await self.bot.pool.fetchrow("SELECT * FROM user_settings WHERE user_id = $1",user.id)
        uwulonian = await self.bot.pool.fetchrow("SELECT * FROM user_stats WHERE user_id = $1",user.id)
        if uwulonian is None:
            return await ctx.send("You or the user doesn't have an uwulonian created.")

        e = discord.Embed(colour=0x7289da)

        e.add_field(name=f"Stats for {uwulonian_name['user_name']}",value=f"""Foes killed - {uwulonian['foes_killed']}\nDeaths - {uwulonian['total_deaths']}\nuwus - {uwulonian['uwus_from_adventure']}""")
        e.add_field(name='Time created',value=f"""{uwulonian_name['time_created'].strftime("%x at %X")}""")
        await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(uwulonian(bot))