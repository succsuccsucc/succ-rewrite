# use.py
# Cog for "use" command
# Use an item

import discord
from discord import app_commands
from discord.ext import commands

import os

from transactions import find_item, item_count

from train_ticket import train_ticket
from morbius_dvd import morbius_dvd

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class UseCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.guild_only()
    @commands.hybrid_command()
    async def use(self, ctx, item):
        item_entry = find_item(item)
        if item_entry is not None:
            item = item_entry['name']
        
            usable_items = {
                "Train Ticket": train_ticket,
                "Morbius DVD": morbius_dvd
            }

            if item in usable_items:
                # Check if user has the item
                if item_count(ctx.author.id, ctx.guild.id, item) > 0:
                    await usable_items[item](ctx)
                else:
                    await ctx.send("🚫 You don't have the item!")
            else:
                await ctx.send("⚠️ Item is not usable!")
        
        else:
            await ctx.send("⚠️ Item doesn't exist!")

# Setup function
async def setup(bot):
    await bot.add_cog(UseCog(bot))  