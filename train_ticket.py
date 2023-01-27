# train_ticket.py
# Usage of item "Train Ticket"

import discord

import os
import random

from transactions import edit_user
from config import color_info

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

async def train_ticket(ctx):
    scenarios = [
        {
            "name": "Cult Ritual",
            "description": "Hymns blasted from the speakers as the doors closed behind you. Everyone on the train started singing along. Someone in a purple cloak walked up to you and said, \"You are the sacrifice.\"",
            "result": "You died! 5 <:Gold_Ingot:1003537929525805197> Gold Ingots is deducted from your inventory.",
            "image": "https://cdn.discordapp.com/attachments/958651015064854551/1006102008362713188/Screenshot_20220803-160805.png",
            "transaction": ["Gold Ingot", -5]
        },
        {
            "name": "Amazon Warehouse",
            "description": "You stepped out of the train and saw stacks of books arranged on enormous shelves. You picked up a book out of curiosity. It says \"Nineteen Eighty-Four\" on the cover.",
            "result": "You forgot the book was still with you when you left. 1 <:Nineteen_EightyFour:1003653365361819648> Nineteen Eighty-Four is added to your inventory.",
            "image": "https://cdn.discordapp.com/attachments/958651015064854551/1006105290321690674/unknown.png",
            "transaction": ["Nineteen Eighty-Four", 1]
        },
        {
            "name": "Mine",
            "description": "The train rushed through winding tunnels and steep inclines, and dropped you off in a dimly lit cave. Miners stared at you like you're a polar bear in a shopping mall.",
            "result": "You saw something shiny in the corner. 5 <:Amethyst_Shard:1003994151307714601> Amethyst Shards are added to your inventory. The miners are now digging frantically in the same spot.",
            "image": "https://cdn.discordapp.com/attachments/958651015064854551/1006107901741510676/unknown.png",
            "transaction": ["Amethyst Shard", 5]
        },
        {
            "name": "125th Street",
            "description": "You fell asleep on the train. When you woke up, you found yourself in New York City. You slowly limp out the train, unable to feel your legs because you've been sitting for too long.",
            "result": "Other passengers mistook you as one of the beggars, and started handing you money. 7 <:Dollar_Coin:1004764584852324442> Dollar Coins are added to your inventory.",
            "image": "https://cdn.discordapp.com/attachments/958651015064854551/1006123653332729866/unknown.png",
            "transaction": ["Dollar Coin", 7]
        }
    ]

    # Draw chosen scenario
    chosen = random.choice(scenarios)

    # Do transaction
    edit_user(ctx.author.id, ctx.guild.id, chosen['transaction'][0], chosen['transaction'][1])

    # Compose confirmation message
    embed_ticket = discord.Embed(title=chosen['name'],
        description=chosen['description'],
        color=color_info
    )

    embed_ticket.add_field(name="🌸 Result",
        value=chosen['result'],
        inline=False
    )

    embed_ticket.set_image(url=chosen['image'])

    # Send confirmation message
    await ctx.send(embed=embed_ticket)