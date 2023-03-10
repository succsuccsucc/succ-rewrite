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
        embed_help = discord.Embed(title="âšī¸ Help!",
            color=color_info)
        
        # "headpat" and "test" must always be at the bottom!
        embed_help.add_field(name="đ¸ pointless", value="https://www.youtube.com/watch?v=EcSzq_6W1QQ", inline=False)
        embed_help.add_field(name="đ¸ leaderboard/lb", value="Get a list of scores collected by each player!", inline=False)
        embed_help.add_field(name="đ¸ inventory/inv [username]", value="Check you or someone's inventory!", inline=False)
        embed_help.add_field(name="đ¸ item <item>", value="Get info on an item!", inline=False)
        embed_help.add_field(name="đ¸ craft <item> [count]", value="Craft items into another item!", inline=False)
        embed_help.add_field(name="đ¸ shop", value="Browse all items in the shop!", inline=False)
        embed_help.add_field(name="đ¸ buy <item> [amount]", value="Buy something from the shop!", inline=False)
        embed_help.add_field(name="đ¸ trade <username> <item(s) to offer> <count of each item> <item(s) to request> <count of each item>", value="Trade items with someone! Separate items and counts with comma and a space.", inline=False)
        embed_help.add_field(name="đ¸ headpat", value="Give succ a headpat!", inline=False)
        embed_help.add_field(name="đ¸ test", value="Test bot status!", inline=False)
        embed_help.set_footer(text="đ¸ Commands start with / or ;")

        await ctx.send(embed=embed_help)

# Setup function
async def setup(bot):
    await bot.add_cog(HelpCog(bot))