# leaderboard.py
# Cog for "leaderboard" command
# Display leaderboard
import discord
from discord import app_commands
from discord.ext import commands

import os

from transactions import open_lb
from config import color_info

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class LeaderboardCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.guild_only()
    @commands.hybrid_command(aliases=['lb'])
    async def leaderboard(self, ctx):
        lb_file = open_lb()
        lb = [d for d in lb_file if ctx.guild.id in d['guilds']]

        embed_lb = discord.Embed(title="📜 Leaderboard",
            description="Get points by pressing the pointless button!",
            color=color_info)
        
        rank_field = ""
        name_field = ""
        score_field = ""
        for i in range(len(lb)):
            # Add player rank to rank field
            if i <= 2:
                medals = ['🥇 1', '🥈 2', '🥉 3']
                rank_field += medals[i]
            else:
                rank_field += str(i + 1)
            rank_field += "\n"

            # Add player username to name field
            name_field += f"<@{lb[i]['id']}>\n"

            # Add player score to score field
            score_field += str(lb[i]['score']) + "\n"
        
        embed_lb.add_field(name="Rank", value=rank_field, inline=True)
        embed_lb.add_field(name="Username", value=name_field, inline=True)
        embed_lb.add_field(name="Score", value=score_field, inline=True)

        embed_lb.set_footer(text=f"👤 {len(lb)}")

        await ctx.send(embed=embed_lb)

# Setup function
async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))   