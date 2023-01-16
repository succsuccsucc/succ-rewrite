# help.py
# Cog for "help" command
# Show list of commands and usages

import discord
from discord import app_commands
from discord.ext import commands

from config import color_info

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    @commands.hybrid_command()
    async def help(self, ctx):
        embed_help = discord.Embed(title="ℹ️ Help!",
            color=color_info)
        
        # "test" must always be at the bottom!
        embed_help.add_field(name="pointless", value="https://www.youtube.com/watch?v=EcSzq_6W1QQ", inline=False)
        embed_help.add_field(name="leaderboard/lb", value="Get a list of scores collected by each player!", inline=False)
        embed_help.add_field(name="test", value="Test bot status!", inline=False)

        embed_help.set_footer(text="🌸 Commands start with / or ;")

        await ctx.send(embed=embed_help)

# Setup function
async def setup(bot):
    await bot.add_cog(HelpCog(bot))