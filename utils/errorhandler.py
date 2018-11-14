import traceback
import sys
from discord.ext import commands
import discord


class errorhandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        errors = (commands.NoPrivateMessage, commands.CommandInvokeError, commands.UserInputError)
        error = getattr(error, 'original', error)

        if isinstance(error, errors):
            await ctx.send(error)
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"Invalid argument. Did you type it correct?")
        if isinstance(error, commands.TooManyArguments):
            await ctx.send(f"Too many arguments. Try less?")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"A required argument is missing. Ya sure you read the command description?")
        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f"{ctx.command} is disabled.")
        else:
            print(error)


def setup(bot):
    bot.add_cog(errorhandler(bot))