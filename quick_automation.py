import re

# Read your current fighter_database.py as a string
with open('fighter_database.py', 'r', encoding='utf-8') as f:
    data = f.read()

# Regex to match each fighter entry
pattern = re.compile(r'"([^"]+)": Fighter\("([^"]+)", "([^"]+)", (\d+), (\d+), (\d+), (\d+)\)')

fighters = {}
for match in pattern.finditer(data):
    key, name, division, power, speed, grappling, popularity = match.groups()
    fighters[key] = {
        "name": name,
        "division": division,
        "power": int(power),
        "speed": int(speed),
        "grappling": int(grappling),
        "popularity": int(popularity)
    }

# Now you can write this to a JSON file
import json
with open('fighters.json', 'w', encoding='utf-8') as f:
    json.dump(fighters, f, indent=2)