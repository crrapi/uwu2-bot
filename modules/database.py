import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
import time
import asyncio
import asyncpg
from datetime import datetime
from datetime import timedelta

class database:
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(database(bot))