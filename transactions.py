# transactions.py
import os
import json

# Change working directory to wherever this is in
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Open the leaderboard file for editing
def open_lb():
    lb = open('data/pointless_leaderboard.json', encoding='utf-8')
    lb = json.load(lb)
    return lb

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