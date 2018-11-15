import discord
from discord.ext import commands
from discord.ext.commands import cooldown
from discord.ext.commands.cooldowns import BucketType
import time
import asyncio
import asyncpg
from datetime import datetime, timedelta
from random import randint
from random import choice
import psutil

colors = [0xe56b6b,0xdd5151,0xba3434,0xab1f1f,0x940808]
online = '<:online_status:506963324391653387>'
offline = '<:offline_status:506963324521414661>'
dnd = '<:dnd_status:506963324634791936>'
idle = '<:idle_status:506963324529803264>'

class misc:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Give someone a slap', brief='Slap', usage='slap [user]')
    async def slap(self, ctx, *, user: discord.Member):
        embed = discord.Embed(colour=choice(colors))
        embed.set_author(name=f"{ctx.author.name} slapped {user.name}! Ouch!")
        embed.set_image(url="https://media.giphy.com/media/RXGNsyRb1hDJm/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command(description='Give someone a hug! Awwww', brief='Hug', usage='hug [user]')
    async def hug(self, ctx, *, user: discord.Member):
        embed = discord.Embed(colour=choice(colors))
        embed.set_author(name=f"{ctx.author.name} gave {user.name} hug! How cute!")
        embed.set_image(url="https://media.giphy.com/media/lXiRKBj0SAA0EWvbG/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command(aliases=['pong'],description='Check the bots latency to Discord Websockets',brief='Check the bots ping',usage='ping')
    async def ping(self, ctx):
        t_1 = time.perf_counter()
        await ctx.trigger_typing()
        t_2 = time.perf_counter()
        time_delta = round((t_2-t_1)*1000)
        await ctx.send(f':ping_pong: Websocket: {round(self.bot.latency*1000)} ms. Typing: {time_delta} ms')

    @commands.command(aliases=["avy"],description='Get a users or your avatar',usage='avatar [user]',brief='Get a users or your avatar')
    async def avatar(self, ctx,*,user:discord.Member=None):
        user = user or ctx.author
        embed = discord.Embed(colour=0x7289da,description=f"[Link]({user.avatar_url})")
        embed.set_author(name=f"{user.name}'s avatar",url=user.avatar_url)
        embed.set_image(url=user.avatar_url_as(static_format="png"))
        await ctx.send(embed=embed)

    @commands.command(aliases=['about'],description='Get stats about the bot',brief='Check bot stats',usage='info')
    async def info(self, ctx):
        cmds_used = await self.bot.pool.fetchval('''SELECT * FROM commands_used;''')
        delta_uptime = datetime.utcnow() - self.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()),3600)
        minutes, seconds = divmod(remainder,60)
        days, hours = divmod(hours,24)
        member_count = 0
        mem_usage = psutil.virtual_memory()[2]
        offline_members = set()
        idle_members = set()
        dnd_members = set()
        online_members = set()
        for g in self.bot.guilds:
            member_count += g.member_count
            for m in g.members:
                if m.status is discord.Status.offline:
                    offline_members.add(m.id)
                if m.status is discord.Status.idle:
                    idle_members.add(m.id)
                if m.status is discord.Status.dnd:
                    dnd_members.add(m.id)
                if m.status is discord.Status.online:
                    online_members.add(m.id)
        offline_count = len(offline_members)
        idle_count = len(idle_members)
        dnd_count = len(dnd_members)
        online_count = len(online_members)
        user_count = len(self.bot.users)
        embed = discord.Embed(color=0x7289da,description=
f'''
Staring at {len(self.bot.users)} users in {len(self.bot.guilds)} servers.
I am using {psutil.virtual_memory()[2]}% of my available memory and {psutil.cpu_percent()}% of my cpu
{cmds_used} commands have been used      
~~My VPS has been burning for~~ {days}d {hours}h {minutes}m {seconds}s
''')
        embed.set_author(name='Bot Stats')
        embed.add_field(name='Members',value=f'{online}{online_count} {idle}{idle_count} {dnd}{dnd_count} {offline}{offline_count}')
        embed.add_field(name='Uptime',value=f'{days}d {hours}h {minutes}m')
        embed.add_field(name='Info',value=f'Made in Python 3.6.6 with Discord.py[rewrite] {discord.__version__}. Made by mellowmarshe#0001. Bot version {self.bot.bot_version}')
        embed.add_field(name='Links',value='[Invite](https://discordapp.com/oauth2/authorize?client_id=508725128427995136&scope=bot&permissions=201718983)\n[DigitalOcean Referral](https://m.do.co/c/e9f223fd5a5c)\n[Source](https://github.com/Domterion/uwu2-bot)')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(misc(bot))