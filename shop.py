# shop.py
# Cog for "shop" command
# Show shop items

import discord
from discord import app_commands
from discord.ext import commands

import os

from transactions import open_items, find_item, curr_count, max_page
from config import color_info

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Declare number of entries per page in shop display
page_size = 5

# Compose list of items to be shown (filter from main items list)
def compose_shop():
    items = open_items()
    shop_items = [d for d in items if d['type'] == "shop"]
    return shop_items

def compose_embed(shop_items, page, ctx):
    embed_shop = discord.Embed(title="🛒 Shop",
        color=color_info)
    
    try:
        shop_slice = shop_items[5 * page: 5 * page + 5]
    except IndexError:
        shop_slice = shop_items[5 * page: -1]
    
    for item in shop_slice:
        item_field = f"{item['emoji']} {item['name']}    "
        if item['currency'] == "G":
            curr_emoji = find_item("Gold Ingot")['emoji']
        else:
            curr_emoji = find_item("Amethyst")['emoji']
        item_field += f"{curr_emoji} {item['price']}"

        embed_shop.add_field(name=item_field,
            value=item['description'],
            inline=False)
    
    # Show player balance
    embed_shop.add_field(name="\u200b",
        value=curr_count(ctx.author.id, ctx.guild.id),
        inline=False)
    
    # Show reminders
    embed_shop.add_field(name="😠 Item icons aren't showing!",
        value='Enable "Use External Emojis" permission for the "everyone" role in this channel. [Source](https://www.reddit.com/r/Discord_Bots/comments/pj7iex/slash_commands_not_showing_external_emoji/)',
        inline=False)

    # Show page number
    embed_shop.set_footer(text=f'🌸 Use "buy <item>" to buy something or learn more!\n📖 {page + 1}/{max_page(shop_items, page_size) + 1}')

    return embed_shop

class Page(discord.ui.View):
    def __init__(self, *, timeout=180, shop_items=[], page=0, ctx=None):
        super().__init__(timeout=timeout)
        self.shop_items = shop_items
        self.page = page
        self.ctx = ctx
    
    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.gray)
    async def previous_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        if self.page <= 0:
            await interaction.response.send_message("🚫 You are already at the first page!", ephemeral=True)
        else:
            self.page -= 1
            await interaction.response.edit_message(embed=compose_embed(self.shop_items, self.page, self.ctx), view=self)
    
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.gray)
    async def next_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        if self.page >= max_page(self.shop_items, page_size):
            await interaction.response.send_message("🚫 You are already at the last page!", ephemeral=True)
        else:
            self.page += 1
            await interaction.response.edit_message(embed=compose_embed(self.shop_items, self.page, self.ctx), view=self)

class ShopCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.guild_only()
    @commands.hybrid_command()
    async def shop(self, ctx):
        shop_items = compose_shop()
        embed_shop = compose_embed(shop_items, 0, ctx)
        await ctx.send(embed=embed_shop, view=Page(shop_items=shop_items, page=0, ctx=ctx))

# Setup function
async def setup(bot):
    await bot.add_cog(ShopCog(bot))