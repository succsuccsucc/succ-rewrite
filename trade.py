# trade.py
# Cog for "trade" command
# Trade items with another user

import discord
from discord import app_commands
from discord.ext import commands

import os

from transactions import find_item, item_count, edit_user
from bot import get_user_object
from config import color_info, color_success, color_failure

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class TradeResponse(discord.ui.View):
    def __init__(self, *, timeout=180, target_user=None, offer_emojis=[], take_emojis=[], offers={}, takes={}, original_embed=None, ctx=None):
        super().__init__(timeout=timeout)
        self.target_user = target_user
        self.offer_emojis = offer_emojis
        self.take_emojis = take_emojis
        self.offers = offers
        self.takes = takes
        self.original_embed = original_embed
        self.ctx = ctx
    
    @discord.ui.button(label="👍 Accept", style=discord.ButtonStyle.green)
    async def accept_button(self,interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.target_user.id:
            # Remove trade response buttons
            await interaction.response.edit_message(embed=self.original_embed, view=None)

            # Check if initiator has enough items
            for key, value in self.offers.items():
                if item_count(self.ctx.author.id, interaction.guild.id, key) >= value:
                    continue
                else:
                    embed_trade_fail_item = discord.Embed(title="⚠️ Trade failed!",
                        description="The person trading with you doesn't have the items!",
                        color=color_failure)
                    await interaction.channel.send(embed=embed_trade_fail_item)
                    return
            # Check if target has enough items
            for key, value in self.takes.items():
                if item_count(interaction.user.id, interaction.guild.id, key) >= value:
                    continue
                else:
                    embed_trade_fail_item = discord.Embed(title="⚠️ Trade failed!",
                        description="You don't have the items!",
                        color=color_failure)
                    await interaction.channel.send(embed=embed_trade_fail_item)
                    return
            
            # Make transaction
            # Remove offered items from initiator
            # Give offered to target
            # Remove requested from target
            # Give requested to initiator
            for key, value in self.offers.items():
                edit_user(self.ctx.author.id, interaction.guild.id, key, -value)
                edit_user(interaction.user.id, interaction.guild.id, key, value)
            for key, value in self.takes.items():
                edit_user(interaction.user.id, interaction.guild.id, key, -value)
                edit_user(self.ctx.author.id, interaction.guild.id, key, value)
            
            # Compose confirmation message
            embed_trade_success = discord.Embed(title="🤝 Trade success!",
                color=color_success)
            await interaction.channel.send(embed=embed_trade_success)
        
        else:
            await interaction.response.send_message(content="🚫 Impostor! You are not the one who knocked.", ephemeral=True)

    @discord.ui.button(label="✋ Reject", style=discord.ButtonStyle.red)
    async def reject_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        if interaction.user.id == self.target_user.id:
            # Remove trade response buttons
            await interaction.response.edit_message(embed=self.original_embed, view=None)

            # Compose confirmation message
            embed_trade_fail_reject = discord.Embed(title="⚠️ Trade failed!",
                description="You rejected the trade offer!",
                color=color_failure)
            await interaction.channel.send(embed=embed_trade_fail_reject)
        
        else:
            await interaction.response.send_message(content="🚫 Impostor! You are not the one who knocked.", ephemeral=True)

class TradeCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.guild_only()
    @commands.hybrid_command()
    async def trade(self, ctx, target, offer, offer_count, take, take_count):
        # Get object of user to trade with
        target_user = await get_user_object(target)
        if target_user is None:
            await ctx.send("⚠️ User not found!")
            return

        # Convert arguments into lists of items
        offer_list = list(map(find_item, offer.split(", ")))
        take_list = list(map(find_item, take.split(", ")))
        if not (None in offer_list or None in take_list) :  # Check if all items specified exist
            # Copy emojis into another list for easy access
            offer_emojis = [item['emoji'] for item in offer_list]
            take_emojis = [item['emoji'] for item in take_list]
            offer_list = [item['name'] for item in offer_list]
            take_list = [item['name'] for item in take_list]
        else:
            await ctx.send("⚠️ Check your item(s)!")
            return

        # Convert arguments into lists of count of each item
        offer_count_list = offer_count.split(", ")
        take_count_list = take_count.split(", ")
        try:
            offer_count_list = list(map(int, offer_count_list))
            take_count_list = list(map(int, take_count_list))
        except ValueError:
            await ctx.send("⚠️ Check your item count(s)!")
            return

        # Combine items and counts into dict
        offers = dict(zip(offer_list, offer_count_list))
        takes = dict(zip(take_list, take_count_list))

        # Compose trade offer embed
        embed_trade_offer = discord.Embed(title="🚢 Wants to trade!",
            color=color_info)
        embed_trade_offer.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        embed_trade_offer.add_field(name="👤 With", value=target, inline=False)

        # Write up list of items offered
        offer_field = ""
        for i in range(len(offer_list)):
            offer_field += f"{offer_emojis[i]} {offer_list[i]}: {offer_count_list[i]}\n"
        embed_trade_offer.add_field(name="📥 Their offer", value=offer_field, inline=True)

        # Write up list of items requested
        take_field = ""
        for j in range(len(take_list)):
            take_field += f"{take_emojis[j]} {take_list[j]}: {take_count_list[j]}\n"
        embed_trade_offer.add_field(name="📤 Their request", value=take_field, inline=True)

        # Actually send the embed
        await ctx.send(embed=embed_trade_offer,
            view=TradeResponse(
                target_user=target_user,
                offer_emojis=offer_emojis,
                take_emojis=take_emojis,
                offers=offers,
                takes=takes,
                original_embed=embed_trade_offer,
                ctx=ctx
            )
        )

# Setup function
async def setup(bot):
    await bot.add_cog(TradeCog(bot))
