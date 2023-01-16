# test.py
# Cog for "test" command
# Test bot status
import discord
from discord import app_commands
from discord.ext import commands

import os

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class TestCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.guild_only()
    @commands.hybrid_command()
    async def test(self, ctx):
        await ctx.send("🍓")

async def setup(bot):
    await bot.add_cog(TestCog(bot))