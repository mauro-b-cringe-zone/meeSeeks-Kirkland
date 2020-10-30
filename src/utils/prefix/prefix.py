import json

def get_prefix(bot, message):
    with open('./src/json/prefix.json', 'r') as f:
        prefixes = json.load(f)
    base = [prefixes[str(message.guild.id)], '?', '!', 'm.']
    return base