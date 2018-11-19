from discord.ext import commands
import discord


class owner:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command(hidden=True)
    async def load(self, ctx, *, ext):
        try:
            self.bot.load_extension(ext)
        except BaseException as e:  # filter BaseException for SystemExit
            return await ctx.send(f"```py\n{type(e).__name__}: {e}\n```")
        await ctx.send(f"{ext} loaded.")

    @commands.command(hidden=True)
    async def unload(self, ctx, *, ext):
        self.bot.unload_extension(ext)
        await ctx.send('Done')

    @commands.command(hidden=True, aliases=['kys', 'exit'])
    async def die(self, ctx):
        await ctx.send("Bye cruel world...")
        await self.bot.logout()

    @commands.command(hidden=True, name="reload")
    async def _reload(self, ctx, *, ext):
        try:
            self.bot.unload_extension(ext)
            self.bot.load_extension(ext)
            await ctx.send(f"**Successfully reloaded {ext}**")
        except BaseException as e:
            await ctx.send(f"```py\n{type(e).__name__}: {e}")

    @commands.command(hidden=True, name='delete')
    async def _delete(self,ctx,user_id,true=None):
        await self.bot.pool.execute("DELETE FROM user_settings WHERE user_id = $1",user_id)
        if true is None:
            await self.bot.pool.execute("DELETE FROM user_timers WHERE user_id = $1",user_id)

        await ctx.send('Done')

    @commands.command(hidden=True,name='pset')
    async def _pset(self,ctx,user_id:int):
        await self.bot.pool.execute("INSERT INTO p_users (user_id) VALUES ($1)",user_id)
        await ctx.send("Done")

    @commands.command(hidden=True,name='premove')
    async def _premove(self,ctx,user_id:int):
        await self.bot.pool.execute("DELETE FROM p_users WHERE user_id = $1",user_id)
        await ctx.send("Done")

def setup(bot):
    bot.add_cog(owner(bot))