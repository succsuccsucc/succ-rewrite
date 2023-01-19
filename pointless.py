# pointless.py
# Cog for "pointless" command
# Pointless button

import discord
from discord import app_commands
from discord.ext import commands

import os
import random

from transactions import edit_user, draw_item

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Pointless button
class PointlessButton(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="Button", disabled=False, style=discord.ButtonStyle.gray)
    async def pointless_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        # Disable command if button is already disabled (someone pressed already)
        if button.disabled == True:
            return
        
        button.disabled = True

        await interaction.response.edit_message(view=self, content=f"👆 <@{interaction.user.id}> pressed the button!")
        edit_user(interaction.user.id, interaction.guild_id, 'score', 1)

        # Draw item
        if random.randint(0, 1) == 1:
            item_name, item_emoji = draw_item()
            if item_name == "Gold Ingot":
                edit_user(interaction.user.id, interaction.guild_id, item_name, 5)
                await interaction.channel.send(f"They got 5 {item_emoji} `{item_name}`!")
            else:
                edit_user(interaction.user.id, interaction.guild_id, item_name, 1)
                await interaction.channel.send(f"They got 1 {item_emoji} `{item_name}`!")
            

class PointlessCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    
    @commands.cooldown(1, 900, commands.BucketType.guild)
    @commands.guild_only()
    @commands.hybrid_command()
    async def pointless(self, ctx):
        await ctx.send("**POINTLESS**\n**BUTTON**\nWarning: Pointless", view=PointlessButton())

# Setup function
async def setup(bot):
    await bot.add_cog(PointlessCog(bot))