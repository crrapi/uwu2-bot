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

    async def has_timer(self,user_id,type:int):
        user = await self.bot.pool.fetchrow("SELECT * FROM user_timers WHERE user_id = $1 AND timer_type = $2;",user_id,type)
        #end_time should be time delta of end time for adventure. If it equals the current time it should be done
        if user is not None:
            return True #user['end_time'] >= datetime.utcnow()

    async def set_timer(self,user_id,time:int,type):

        time = timedelta(seconds=time) + datetime.utcnow()

        await self.bot.pool.execute('''
            INSERT INTO user_timers (user_id,end_time,timer_type)
            VALUES ($1,$2,$3) 
        ''',user_id,time,type)

    async def waiter(self):
        while not self.bot.is_closed():
            await asyncio.sleep(5)
            rows = await self.bot.pool.fetchrow('SELECT * FROM user_timers ORDER BY end_time DESC LIMIT 1;')
            if not rows:
                continue
            time = rows['end_time'] - datetime.utcnow()
            await asyncio.sleep(time.total_seconds())
            e = discord.Embed()
            #0 is explore
            user = self.bot.get_user(rows['user_id'])
            if rows['timer_type'] is 0:
                deaths = randint(1,2)
                foes_killed = randint(10,120)
                xp = ((foes_killed * 10) - (deaths * 25)) / 2
                uwus_earned = (foes_killed * 10) - (deaths * 25)
                e.set_author(name=f"Your uwulonian is back from exploring")
                e.add_field(name='Explore Stats',value=f"Foes killed - {foes_killed}\nDeaths - {deaths}(-50 per death)\nXP Earned - {xp}\nuwus Earned - {uwus_earned}")
                e.set_footer(text='Good luck on your next exploration!')
            else:
                deaths = randint(1,4)
                foes_killed = randint(45,320)
                uwus_earned = (foes_killed * 10) - (deaths * 50)
                xp = ((foes_killed * 10) - (deaths * 50)) / 2
                e.set_author(name=f"Your uwulonian is back from their adventure")
                e.add_field(name='Adventure Stats',value=f"Foes killed - {foes_killed}\nDeaths - {deaths}(-50 per death)\nXP Earned - {xp}\nuwus Earned - {uwus_earned}")
                e.set_footer(text='Good luck on your next adventure!')
            await self.bot.pool.execute('''
            INSERT INTO user_stats (user_id,uwus,foes_killed,total_deaths,current_xp)
            VALUES ($1,$2,$3,$4,$5) 
            ON CONFLICT (user_id) DO UPDATE
            SET uwus = user_stats.uwus + $2, foes_killed = user_stats.foes_killed + $3, total_deaths = user_stats.total_deaths + $4, current_xp = user_stats.current_xp + $5
            ''',rows['user_id'],uwus_earned,foes_killed,deaths,xp)
            try:
                await user.send(embed=e)
            except discord.Forbidden:
                pass
            await self.bot.pool.execute("DELETE FROM user_timers WHERE user_id = $1 AND timer_type = $2",rows['user_id'],rows['timer_type'])

    @commands.command(description='Set your uwulonian out on an adventure')
    async def adventure(self,ctx):
        user = await self.bot.pool.fetchrow("SELECT * FROM user_settings WHERE user_id = $1",ctx.author.id)
        if user is None:
            return await ctx.send("You don't have an uwulonian created.")
        if await self.has_timer(user_id=ctx.author.id,type=1):
            return await ctx.send("You already have an adventure. Wait for your uwulonian to return for a new adventure.")

        await self.set_timer(user_id=ctx.author.id,time=3600,type=1)
        await ctx.send(f"Sending {user['user_name']} on an adventure! Your uwulonian will be back in an hour. Make sure your DMs are open so I can DM you once your uwulonian is back.")

    @commands.command(description='Make your uwulonian explore')
    async def explore(self,ctx):
        user = await self.bot.pool.fetchrow("SELECT * FROM user_settings WHERE user_id = $1",ctx.author.id)
        if user is None:
            return await ctx.send("You don't have an uwulonian created.")
        if await self.has_timer(user_id=ctx.author.id,type=0):
            return await ctx.send("Your uwulonian is already exploring. Wait for your uwulonian to return for a new exploration.")

        await self.set_timer(user_id=ctx.author.id,time=1800,type=0)
        await ctx.send(f"Sending {user['user_name']} to explore! Your uwulonian will be back in an hour. Make sure your DMs are open so I can DM you once your uwulonian is back.")

def setup(bot):
    bot.add_cog(exploring(bot))