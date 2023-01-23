# inventory.py
# Cog for "inventory" command
# Show inventory of user

import discord
from discord import app_commands
from discord.ext import commands

import typing

import os

from transactions import open_items, find_user, curr_count, max_page
from bot import get_user_object
from config import color_info

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Declare number of entries per page in inventory display
page_size = 5

# Compose list(page) of items to be shown
def compose_inv(items, profile):
    shown = []
    for item in items:
        if item['name'] in profile['inventory']:
            new_show = {
                "name": item['name'],
                "emoji": item['emoji'],
                "count": profile['inventory'][item['name']],
                "desc": item['description']
            }
            shown.append(new_show)

    return shown

# Compose inventory display
def compose_embed(shown, page, user, ctx):
    embed_inv = discord.Embed(title="🗄️ Inventory",
        description=curr_count(user.id, ctx.guild.id),
        color=color_info)
    embed_inv.set_author(name=user.display_name, icon_url=user.display_avatar.url)

    try:
        shown_slice = shown[5 * page: 5 * page + 5]
    except IndexError:
        shown_slice = shown[5 * page: -1]

    for item in shown_slice:
        embed_inv.add_field(name=f"{item['emoji']} {item['name']}: {item['count']}",
            value=item['desc'],
            inline=False)
    
    embed_inv.add_field(name="\u200b", value="\u200b", inline=False) 
    embed_inv.add_field(name="😠 Item icons aren't showing!",
        value='Enable "Use External Emojis" permission for the "everyone" role in this channel. [Source](https://www.reddit.com/r/Discord_Bots/comments/pj7iex/slash_commands_not_showing_external_emoji/)',
        inline=False)
    embed_inv.add_field(name="🌸 This bot is in early development!",
        value="Player progress may be edited or removed without warning.",
        inline=False)
    
    embed_inv.set_footer(text=f"📖 {page + 1}/{max_page(shown, page_size) + 1}")

    return embed_inv

# Compose page flip buttons
class Page(discord.ui.View):
    def __init__(self, *, timeout=180, shown=[], page=0, user=None, ctx=None):
        super().__init__(timeout=timeout)
        self.shown = shown
        self.page = page
        self.user = user
        self.ctx = ctx

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.gray)
    async def previous_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        if self.page <= 0:
            await interaction.response.send_message("🚫 You are already at the first page!", ephemeral=True)
        else:
            self.page -= 1
            await interaction.response.edit_message(embed=compose_embed(self.shown, self.page, self.user, self.ctx), view=self)

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.gray)
    async def next_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        if self.page >= max_page(self.shown, page_size):
            await interaction.response.send_message("🚫 You are already at the last page!", ephemeral=True)
        else:
            self.page += 1
            await interaction.response.edit_message(embed=compose_embed(self.shown, self.page, self.user, self.ctx), view=self)

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

            # # Show currency on top
            # embed_inv = discord.Embed(title="🗄️ Inventory",
            #     description=curr_count(user.id, ctx.guild.id),
            #     color=color_info)
            # embed_inv.set_author(name=user.display_name, icon_url=user.display_avatar.url)

            # for item in items:
            #     if item['name'] in profile['inventory']:
            #         item_name = item['name']
            #         embed_inv.add_field(name=f"{item['emoji']} {item_name}: {profile['inventory'][item_name]}",
            #             value=item['description'],
            #             inline=False)

            # embed_inv.add_field(name="\u200b", value="\u200b", inline=False)
            
            # embed_inv.add_field(name="😠 Where are my items?",
            #     value="Your progress will be migrated from succ once the rewrite is ready!",
            #     inline=False)
            # embed_inv.add_field(name="🌸 This bot is in early development!",
            #     value="Player progress may be edited or removed without warning.",
            #     inline=False)

            shown = compose_inv(items, profile)
            await ctx.send(embed=compose_embed(shown, 0, user, ctx),
                view=Page(shown=shown, page=0, user=user, ctx=ctx))
        else:
            await ctx.send("⚠️ Invalid username!") 

# Setup function
async def setup(bot):
    await bot.add_cog(InventoryCog(bot))