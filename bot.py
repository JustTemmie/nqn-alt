import os
import random
import logging
from time import time

import discord
from discord import Intents
from discord.ext import tasks, commands


from dotenv import load_dotenv

load_dotenv("keys.env")
TOKEN = os.getenv("DISCORD")

def get_prefix(bot, message):
    # try:
    # prefix = db[f"prefix_{message.guild.id}"]
    # return commands.when_mentioned_or(prefix)(bot, message)
    # except:
    return commands.when_mentioned_or("..")(bot, message)


bot = commands.Bot(command_prefix=(get_prefix), owner_ids=[368423564229083137]  , intents=Intents.all())

bot.remove_command("help")
bot.ready = False


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.idle,
        activity=discord.Activity(type=discord.ActivityType.watching, name="beaver  "),
    )
    if not bot.ready:

        guild_count = 0
        for guild in bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")
            guild_count = guild_count + 1

        print(f"{bot.user} is in " + str(guild_count) + " guild(s).")

        bot.ready = True


# loads cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run((TOKEN), bot=True, reconnect=True)
