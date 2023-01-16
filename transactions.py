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
def new_profile(lb, id):
    new_user = {
        "id": id,
        "score": 0,
        "inventory": {}
    }
    lb.append(new_user)
    return lb

# Find inventory of user in leaderboard
def find_user(id):
    lb = open_lb()
    user = next((item for item in lb if item["id"] == id), None)

    if user == None:
        lb = new_profile(lb, id)
        user = next((item for item in lb if item["id"] == id), None)
    
    return lb, user

# Edit score/inventory of user
def edit_user(id, item, amount):
    lb, user = find_user(id)
    
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