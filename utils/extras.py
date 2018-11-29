import asyncio
from datetime import datetime
from discord.ext import commands


async def sleep_time(dt: datetime):
    time = (dt - datetime.utcnow()).total_seconds()
    await asyncio.sleep(time)
    return True