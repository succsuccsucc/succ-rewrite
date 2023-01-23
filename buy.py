# buy.py
# Cog for "buy" command
# Buy an item from the shop

import discord
from discord import app_commands
from discord.ext import commands

import os

from transactions import find_item, item_count, edit_user, curr_count, find_emoji
from config import color_failure, color_info, color_success

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Dict to translate "currency" attribute of item to currency item name
curr_dict = {
    "G": "Gold Ingot",
    "A": "Amethyst"
}
# Dict to translate currency type into emoji
emoji_dict = {
    "G": find_item("Gold Ingot")['emoji'],
    "A": find_item("Amethyst")['emoji']
}

class BuyButton(discord.ui.View):
    def __init__(self, *, timeout=180, item="", emoji="", currency="", total_price=0, count=1, original_embed=None, ctx=None):
        super().__init__(timeout=timeout)
        self.item = item
        self.emoji = emoji
        self.currency = currency
        self.total_price = total_price
        self.count = count
        self.original_embed = original_embed
        self.ctx = ctx

    @discord.ui.button(label="Buy",style=discord.ButtonStyle.green)
    async def buy_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.ctx.author.id:
            # Remove buy button
            await interaction.response.edit_message(embed=self.original_embed, view=None)
            # Check if user has enough balance
            if item_count(self.ctx.author.id, self.ctx.guild.id, curr_dict[self.currency]) >= self.total_price:
                # Make transaction
                edit_user(self.ctx.author.id, self.ctx.guild.id, curr_dict[self.currency], -(self.total_price))
                edit_user(self.ctx.author.id, self.ctx.guild.id, self.item, self.count)

                # Send confirmation message
                embed_bought = discord.Embed(title="🛍️ Bought!",
                    description=f"{self.emoji} {self.item}: {self.count}",
                    color=color_success)
                
                embed_bought.add_field(name="💸 Paid",
                    value=f"{emoji_dict[self.currency]} {self.total_price}",
                    inline=False)
                embed_bought.add_field(name="🏦 Balance",
                    value=curr_count(self.ctx.author.id, self.ctx.guild.id),
                    inline=False)
            
                await interaction.channel.send(embed=embed_bought)
            
            else:
                embed_buy_fail = discord.Embed(title="🚫 Failed to buy!",
                    description="You don't have enough currency!",
                    color=color_failure)
                await interaction.channel.send(embed=embed_buy_fail)
        
        else:
            await interaction.response.send_message(content="🚫 Impostor! You are not the one who knocked.")

class BuyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.guild_only()
    @commands.hybrid_command()
    async def buy(self, ctx, item, count=1):
        item_entry = find_item(item)
        if item_entry is not None:
            item = item_entry['name']

            if item_entry['type'] == "shop":
                # Send buying dialog
                embed_buy = discord.Embed(title="🛍️ You're about to buy",
                    description=item,
                    color=color_info)
                embed_buy.set_thumbnail(url=find_emoji(item_entry['emoji']))
                # Item info
                embed_buy.add_field(name=item_entry['description'],
                    value=item_entry['detail'],
                    inline=False)
                embed_buy.add_field(name="💧 Unit Price", 
                    value=f"{emoji_dict[item_entry['currency']]} {item_entry['price']}",
                    inline=True)
                embed_buy.add_field(name="📚 Count",
                    value=count,
                    inline=True)
                embed_buy.add_field(name="🌊 Total Price",
                    value=f"{emoji_dict[item_entry['currency']]} {item_entry['price'] * count}",
                    inline=True)
                
                await ctx.send(embed=embed_buy, 
                    view=BuyButton(item=item,
                        emoji=item_entry['emoji'],
                        currency=item_entry['currency'], 
                        total_price=(item_entry['price'] * count), 
                        count=count,
                        original_embed=embed_buy,
                        ctx=ctx
                    )
                )
            
            else:
                await ctx.send("⚠️ Item not in shop!")

        else:
            await ctx.send("⚠️ Item doesn't exist!")
# Setup function
async def setup(bot):
    await bot.add_cog(BuyCog(bot))