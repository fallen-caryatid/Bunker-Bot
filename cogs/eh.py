import discord
import traceback
import sys

from bot import BunkerBot
from context import BBContext
from discord.ext import commands


class eh(commands.Cog):

    def __init__(self, bot: BunkerBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: BBContext, error: Exception):
        """
        The event triggered when an error is raised while invoking a command.

        Parameters
        ------------
        ctx: BBContext
            The context for the command invocation
        error: Exception
            The Exception raised
        """

        await ctx.release_connection()

        if ctx.command and ctx.command.has_error_handler:
            return

        if ctx.cog and ctx.cog.has_error_handler():
            return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.', delete_after=10)

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Whoa slow down buddy! Retry in **{round(error.retry_after)}** seconds.', delete_after=10)
        
        elif isinstance(error, commands.UserInputError):
            await ctx.send(str(error), delete_after=10)

        elif isinstance(error, commands.CheckFailure):
            print(error.args)
            await ctx.tick(False)
        
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(eh(bot))
