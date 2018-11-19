import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
import time
import asyncio
import asyncpg
from datetime import datetime

class create:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Create a new uwulonian.')
    async def create(self,ctx):
        if await self.bot.pool.fetchrow("SELECT * FROM user_settings WHERE user_id = $1",ctx.author.id):
            return await ctx.send('You already have a uwulonian created.')

        def check(amsg):
            return amsg.author == ctx.author
        name_set = await ctx.send('Please enter your uwulonians name. This will timeout after 30 seconds.')
        try:
            name = await self.bot.wait_for('message', timeout=30, check=check)
        except asyncio.TimeoutError:
            return await name_set.edit(content='Create timed out')

        if len(name.content) > 60 or len(name.content) < 3:
            return await name_set.edit("Invalid name. Names can't be longer then 60 chars or less than 3 chars.")

        try:
            await self.bot.pool.execute('INSERT INTO user_settings ("user_id","user_name") VALUES ($1,$2);',ctx.author.id,name.content)
        except asyncpg.UniqueViolationError:
            return await ctx.send(f"{name.content} is already used. Please try again with a different name.")
        await self.bot.pool.execute('INSERT INTO user_stats ("user_id","uwus","foes_killed","total_deaths","current_xp","current_level") VALUES ($1,$2,$3,$4,$5,$6);',ctx.author.id,0,0,0,0,0)
        await name_set.delete()
        await ctx.send(f"Success! Made uwulonian with name `{name.content}`".replace('@','@\u200b'))

def setup(bot):
    bot.add_cog(create(bot))