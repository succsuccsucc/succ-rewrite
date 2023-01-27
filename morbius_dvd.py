# morbius_dvd.py
# Usage of item "Morbius DVD"

import discord

import os

from transactions import edit_user, gold_emoji
from config import color_info

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class MorbButton(discord.ui.View):
    def __init__(self, *, timeout=3, embed_morb=None, morb_count=0, ctx=None):
        super().__init__(timeout=timeout)
        self.embed_morb = embed_morb
        self.morb_count = morb_count
        self.ctx = ctx

    @discord.ui.button(label="👆 Morb",style=discord.ButtonStyle.green)
    async def morb_button(self,interaction:discord.Interaction,button:discord.ui.Button):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(content='Impostor! You are not the one who knocked.', ephemeral=True)
            return
        
        self.morb_count += 1

        await interaction.response.send_message(content="Morb", delete_after=0)

    async def on_timeout(self):
        if self.morb_count < 7:
            edit_user(self.ctx.author.id, self.ctx.guild.id, "Gold Ingot", -7)
            await self.ctx.send(f"😔 Morb failed!\nYou lost {gold_emoji} 7.")
        else:
            edit_user(self.ctx.author.id, self.ctx.guild.id, "Gold Ingot", 7)
            await self.ctx.send(f"😎 Morb success!\nYou won {gold_emoji} 7.")
        return

async def morbius_dvd(ctx):
    embed_morb = discord.Embed(title="🦇 It's morbin' time!",
        description="Mash the MORB BUTTON to morb!",
        color=color_info)
    
    embed_morb.set_image(url="https://cdn.discordapp.com/attachments/805744932975280158/1011650783730733166/unknown.png")

    await ctx.send(embed=embed_morb, 
        view=MorbButton(embed_morb=embed_morb,
            ctx=ctx
        )
    )