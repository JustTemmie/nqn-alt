import discord
from discord.ext import commands, tasks
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import (
    CommandNotFound,
    BadArgument,
    MissingRequiredArgument,
    CommandOnCooldown,
    cooldown,
    BucketType,
)
import random
from datetime import datetime
import time

IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Sorry, something unexpected went wrong.")
            # raise

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            # await ctx.send("Sorry, I couldn't find that command")
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(
                f"One or more of the required arguments are missing, perhaps the help command could help you out? {ctx.prefix}help (command)"
            )

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(
                f"That command is on {str(exc.cooldown.type).split('.')[-1]} cooldown. Please try again in {exc.retry_after:,.2f} seconds.",
                delete_after=(exc.retry_after + 0.7),
            )

        #      elif isinstance(exc.original, HTTPException):
        #          await ctx.send("Unable to send message.")

        elif hasattr(exc, "original"):
            # raise exc  # .original

            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have the permission to do that.")

            else:
                raise exc.original

        else:
            raise exc

    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        
        data = ctx.content
        data = data.replace(":", "-startwe-", 1)
        data = data.replace(":", "-endwe-", 1)
        start = data.find("-startwe-")
        end = data.find("-endwe-")
        substring = data[start+9:end]
        #print(data)

        #print(substring)
        print(start)
        print(end-9 + len(substring))
        data = ctx.content
        if len(data) > end-9 + len(substring):
            data = data[0: start:] + data[end-9 + 1::]
        await ctx.channel.send(data)

        try:
            custom_emoji = discord.utils.get(ctx.channel.guild.emojis, name=substring)
            await ctx.channel.send(custom_emoji)
        except:
            pass

def setup(bot):
    bot.add_cog(events(bot))
