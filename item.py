# item.py
# Cog for "item" command
# Get info for an item

import discord
from discord import app_commands
from discord.ext import commands

import os

from transactions import item_count, find_item
from config import color_info

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class ItemCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.guild_only()
    @commands.hybrid_command()
    async def item(self, ctx, item):
        entry = find_item(item)
        
        if item is not None:
            count_owned = item_count(ctx.author.id, ctx.guild.id, item)

            embed_item = discord.Embed(title=entry['name'],
                description=entry['description'],
                color=color_info)
            embed_item.add_field(name="Description", value=entry['detail'], inline=False)

            type_dict = {
                "collect": "Normal",
                "craft": "Crafted",
                "shop": "Shop",
                "discontinued": "Discontinued"
            }
            embed_item.add_field(name="Type", value=type_dict[entry['type']], inline=True)

            if entry['type'] == "craft":
                ingredient_field = ""
                for key, value in entry['ingredients'].items():
                    in_emoji = find_item(key)['emoji']
                    ingredient_field += f"{in_emoji} {key}: {value}"
                embed_item.add_field(name="Ingredients", value=ingredient_field, inline=True)
            elif entry['type'] == "shop":
                curr_dict = {
                    "G": "Gold Ingot",
                    "A": "Amethyst"
                }
                embed_item.add_field(name="Price", value=f"{find_item(curr_dict[entry['currency']])['emoji']} {entry['price']}", inline=True)
            
            embed_item.add_field(name="You have", value=str(count_owned), inline=False)

            await ctx.send(embed=embed_item)
        else:
            await ctx.send("⚠️ Item does not exist!")
    
# Setup function
async def setup(bot):
    await bot.add_cog(ItemCog(bot))