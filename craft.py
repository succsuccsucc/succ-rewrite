# craft.py
# Cog for "craft" command
# Craft items into another item

import discord
from discord import app_commands
from discord.ext import commands

import os

from transactions import find_item, item_count, edit_user
from config import color_success, color_failure

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class CraftCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.guild_only()
    @commands.hybrid_command()
    async def craft(self, ctx, item, count=1):
        item_entry = find_item(item)
        if item_entry is not None:
            item = item_entry['name']
         
            if item_entry['type'] == "craft":
                for key, value in item_entry['ingredients'].items():
                    # Check if user have enough ingredients
                    if item_count(ctx.author.id, ctx.guild.id, key) >= value * count:
                        continue
                    else:
                        embed_craft_fail = discord.Embed(title="🚫 Craft failed!",
                            description="You don't have the required ingredients!",
                            color=color_failure)
                        await ctx.send(embed=embed_craft_fail)
                        return
                
                # Make transaction (looping twice, seems not efficient enough?)
                # Text fields for confirmation message, prepared here for efficiency
                ing_field = ""
                for key, value in item_entry['ingredients'].items():
                    ing_field += f"{find_item(key)['emoji']} {key}: {value * count}\n" # Text field for confirmation message
                    # Actual transaction: Deduct ingredients
                    edit_user(ctx.author.id, ctx.guild.id, key, -(value * count))
                # Give product
                edit_user(ctx.author.id, ctx.guild.id, item, count)
                crafted_field = f"{item_entry['emoji']} {item}: {count}" # Text field for confirmation message

                # Send confirmation message (looping 3 times now yay)
                embed_craft = discord.Embed(title="⚒️ Craft success!",
                    color=color_success)
                embed_craft.add_field(name="📥 Ingredients", value=ing_field, inline=True)
                embed_craft.add_field(name="📤 Crafted", value=crafted_field, inline=True)

                await ctx.send(embed=embed_craft)
                
            else:
                await ctx.send("⚠️ Item is uncraftable!")
        
        else:
            await ctx.send("⚠️ Item doesn't exist!")
    
# Setup function
async def setup(bot):
    await bot.add_cog(CraftCog(bot))  