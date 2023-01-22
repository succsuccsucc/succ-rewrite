# bot.py
import discord
from discord import app_commands
from discord.ext import commands

import os
import asyncio
from dotenv import load_dotenv

import config

# Fixes runtime error: asyncio.run() cannot be called from a running event loop
import nest_asyncio
nest_asyncio.apply()

# Change working directory to wherever bot.py is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# load bot token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix=";", intents=intents, activity=discord.Game(name="Subway Surfers"), help_command=None)

# Load cogs (extensions)
initial_extensions = ['test', 'help',  # base commands
    'pointless', 'leaderboard', 'item', 'inventory', 'craft']  # pointless commands
# Load extensions listed above
async def load_extensions():
    for extension in initial_extensions:
        await bot.load_extension(extension)

# On ready event
# Display bot guilds
@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild(s):\n'
            f'{guild.name}(id: {guild.id})'
        )

# Helper functions start
# Get user object from a ping
async def get_user_object(ping):
    if not ping:
        return None
    else:
        try:
            user_id = ping[2 : -1]
        except:
            return None

    user = await bot.fetch_user(user_id)
    return user
# Helper functions end

# Text commands start
# "sync" command
# Syncs command tree with Discord
@commands.guild_only()
@bot.command()
async def sync(ctx):
    if ctx.author.id == 740098404688068641:
        await bot.tree.sync()
        await ctx.send("Commands synced!")
    else:
        await ctx.send("Impostor! You are not the chosen one!")

@commands.guild_only()
@bot.hybrid_command()
async def headpat(ctx):
    await ctx.send("You gave sphere a headpat. They seem happy.")
    await ctx.send("https://tenor.com/bLeZU.gif")
# Text commands end

# Error handling
@bot.event
async def on_command_error(ctx, error):
    # Wrong command
    if isinstance(error, commands.CommandNotFound):
        return
    # Command on cooldown
    elif isinstance(error, commands.CommandOnCooldown):
        cooldown = round(error.retry_after)
        if error.retry_after > 60:
            cooldown_m = int(cooldown / 60)
            cooldown_s = int(cooldown % 60)
            await ctx.send(f'⏳ Command on cooldown!\nTry again after `{cooldown_m}m {cooldown_s}s`.')
        else:
            await ctx.send(f'⏳ Command on cooldown!\nTry again after `{cooldown}s`.')
    
# Launch bot
async def main():
    async with bot:
        await load_extensions()
        bot.run(TOKEN)

asyncio.run(main())