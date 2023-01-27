# transactions.py
import os
import json
import random
import re

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Open the leaderboard file for editing
def open_lb():
    lb = open('data/pointless_leaderboard.json', encoding='utf-8')
    lb = json.load(lb)
    return lb

# Open list of items
def open_items():
    items = open('data/pointless_items.json', encoding='utf-8')
    items = json.load(items)
    return items

# Save the edited leaderboard to the file
def save_lb(lb):
    # Sort the leaderboard by user score
    lb.sort(key=lambda x: x['score'], reverse=True)
    outfile = open('data/pointless_leaderboard.json', 'w', encoding='utf-8')
    json.dump(lb, outfile, indent = 4)
    return lb

# Add a new user to the leaderboard
# Only called when the user is not on leaderboard already
def new_profile(lb, id, guild_id):
    new_user = {
        "id": id,
        "guilds": [guild_id],
        "score": 0,
        "inventory": {
            "Gold Ingot": 0,
            "Amethyst": 0
        }
    }
    lb.append(new_user)
    return lb

# Find inventory of user in leaderboard
def find_user(id, guild_id):
    lb = open_lb()
    user = next((item for item in lb if item["id"] == id), None)

    # Create new profile for user if they're not found in the leaderboard
    if user == None:
        lb = new_profile(lb, id, guild_id)
        user = next((item for item in lb if item["id"] == id), None)
    
    # Add current guild to user's guild list if guild not registered to user yet
    if guild_id not in user['guilds']:
        user['guilds'].append(guild_id)
    
    return lb, user

# Edit score/inventory of user
def edit_user(id, guild_id, item, amount):
    lb, user = find_user(id, guild_id)
    
    if item == 'score':
        user['score'] += amount
        if user['score'] < 0:
            user['score'] = 0
    else:
        if item not in user['inventory']:
            user['inventory'][item] = 0

        user['inventory'][item] += amount
        if user['inventory'][item] < 0:
            user['inventory'][item] = 0
    
    save_lb(lb)

# Draw item (for "pointless")
def draw_item():
    items = open_items()
    collectibles = [f for f in items if f['type'] == 'collect']

    population = [tuple(d.values()) for d in collectibles]
    weights = [e['rarity'] for e in collectibles]

    chosen = random.choices(population=population, weights=weights, k=1)[0]
    return chosen[0], chosen[1]

# Check number of specific item owned by a user
def item_count(id, guild_id, item):
    lb, user = find_user(id, guild_id)

    if item not in user['inventory']:
        return 0
    else:
        return user['inventory'][item]

# Find the entry for an item from the list of items
def find_item(item):
    items = open_items()

    item = next((i for i in items if i['name'].upper() == item.upper()), None)
    return item

# Find the image URL for a custom emoji
def find_emoji(emoji):
    # Extract emoji ID
    emoji_id = re.findall('\d+', emoji)[0]
    # Determine if emoji is animated
    if emoji[1] == 'a':
        url = f"https://cdn.discordapp.com/emojis/{emoji_id}.gif"
    else:
        url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"
    return url

# Get currency count of a user
def curr_count(id, guild_id):
    lb, user = find_user(id, guild_id)

    gold_count = user['inventory']['Gold Ingot']
    amethyst_count = user['inventory']['Amethyst']

    gold_emoji = find_item('Gold Ingot')['emoji']
    amethyst_emoji = find_item('Amethyst')['emoji']

    return f"{gold_emoji} {gold_count} | {amethyst_emoji} {amethyst_count}"

# Get maximum page of a list
def max_page(list, page_size):
    idx = int(len(list) / page_size)
    # Edge case: if queue length is 0
    if len(list) == 0:
        pass
    # Edge case: if queue length is non-zero multiple of 5
    elif len(list) % page_size == 0:
        idx -= 1
    return idx