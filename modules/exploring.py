import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
import time
import asyncio
import asyncpg
from datetime import datetime, timedelta
from random import randint

class exploring:
    def __init__(self, bot):
        self.bot = bot
        self.task = self.bot.loop.create_task(self.waiter())

    def __unload(self):
        self.task.cancel()

    async def has_adventure(self,userid):
        user = await self.bot.pool.fetchrow("SELECT * FROM user_adventures WHERE user_id = $1;",userid)
        #end_time should be time delta of end time for adventure. If it equals the current time it should be done
        if user is not None:
            return user['end_time'] >= datetime.utcnow()

    async def set_adventure(self,userid):

        time = timedelta(hours=1) + datetime.utcnow()

        await self.bot.pool.execute('''
            INSERT INTO user_adventures (user_id,end_time)
            VALUES ($1,$2) 
            ON CONFLICT (user_id) DO UPDATE
            SET end_time = $2;
        ''',userid,time)

    async def waiter(self):
        while not self.bot.is_closed():
            await asyncio.sleep(5)
            rows = await self.bot.pool.fetchrow('SELECT * FROM user_adventures ORDER BY end_time DESC LIMIT 1;')
            if not rows:
                continue
            time = rows['end_time'] - datetime.utcnow()
            await asyncio.sleep(time.total_seconds())
            user = self.bot.get_user(rows['user_id'])
            deaths = randint(1,4)
            foes_killed = randint(45,320)
            uwus_earned = (foes_killed * 10) - (deaths * 50)
            await self.bot.pool.execute('''
                INSERT INTO user_stats ("user_id","uwus_from_adventure","foes_killed","total_deaths")
                VALUES ($1,$2,$3,$4) 
                ON CONFLICT (user_id) DO UPDATE
                SET uwus_from_adventure = user_stats.uwus_from_adventure + $2, foes_killed = user_stats.foes_killed + $3, total_deaths = user_stats.total_deaths + $4
            ''',rows['user_id'],uwus_earned,foes_killed,deaths)
            e = discord.Embed()
            e.set_author(name=f"Your uwulonian is back from their adventure")
            e.add_field(name='Adventure Stats',value=f"Foes killed - {foes_killed}\nDeaths - {deaths}(-50 per death)\nuwus Earned - {uwus_earned}")
            e.set_footer(text='Good luck on your next adventure!')
            try:
                await user.send(embed=e)
            except discord.Forbidden:
                pass
            await self.bot.pool.execute("DELETE FROM user_adventures WHERE user_id = $1",rows['user_id'])

    @commands.command(description='Set your uwulonian out on an adventure')
    async def adventure(self,ctx):
        user = await self.bot.pool.fetchrow("SELECT * FROM user_settings WHERE user_id = $1",ctx.author.id)
        if user is None:
            return await ctx.send("You don't have an uwulonian created.")
        if await self.has_adventure(userid=ctx.author.id):
            return await ctx.send("You already have an adventure. Wait for your uwulonian to return for a new adventure.")

        await self.set_adventure(userid=ctx.author.id)
        await ctx.send(f"Sending {user['user_name']} on an adventure! Your uwulonian will be back in an hour. Make sure your DMs are open so I can DM you once your uwulonian is back.")

def setup(bot):
    bot.add_cog(exploring(bot))