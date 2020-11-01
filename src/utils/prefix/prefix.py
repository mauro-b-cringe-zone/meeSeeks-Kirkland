import json

def get_prefix(bot, message):
    with open('./src/json/prefix.json', 'r') as f:
        prefixes = json.load(f)
    base = [prefixes[str(message.guild.id)], '?', '!', 'm.']
    return base


def eliminar_prefix(guild):
    with open('./src/json/prefix.json', 'r') as f:
        prefixes = json.load(f)
    
    del prefixes[str(guild.id)]

    with open('./src/json/prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)