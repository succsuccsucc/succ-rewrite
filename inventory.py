# inventory.py
# Cog for "inventory" command
# Show inventory of user

import discord
from discord import app_commands
from discord.ext import commands

import typing

import os

from transactions import open_items, find_user, curr_count
from bot import get_user_object
from config import color_info

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class InventoryCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.guild_only()
    @commands.hybrid_command(aliases=['inv'])
    async def inventory(self, ctx, ping=None):
        if ping is None:
            user = self.bot.get_user(ctx.author.id)
        else:
            user = await get_user_object(ping)
        if user is not None:
            lb, profile = find_user(user.id, ctx.guild.id)
            items = open_items()

            # Show currency on top
            embed_inv = discord.Embed(title="🗄️ Inventory",
                description=curr_count(user.id, ctx.guild.id),
                color=color_info)
            embed_inv.set_author(name=user.display_name, icon_url=user.display_avatar.url)

            for item in items:
                if item['name'] in profile['inventory']:
                    item_name = item['name']
                    embed_inv.add_field(name=f"{item['emoji']} {item_name}: {profile['inventory'][item_name]}",
                        value=item['description'],
                        inline=False)

            embed_inv.add_field(name="\u200b", value="\u200b", inline=False)
            
            embed_inv.add_field(name="😠 Where are my items?",
                value="Your progress will be migrated from succ once the rewrite is ready!",
                inline=False)
            embed_inv.add_field(name="🌸 This bot is in early development!",
                value="Player progress may be edited or removed without warning.",
                inline=False)

            await ctx.send(embed=embed_inv)
        else:
            await ctx.send("⚠️ Invalid username!") 

# Setup function
async def setup(bot):
    await bot.add_cog(InventoryCog(bot))