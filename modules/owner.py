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
        await ctx.message.add_reaction("\N{OK HAND SIGN}")

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


def setup(bot):
    bot.add_cog(owner(bot))