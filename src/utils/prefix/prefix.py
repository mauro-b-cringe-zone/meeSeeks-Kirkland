import json
from os import environ as env
from discord.ext import commands

def get_prefix(bot, message):
    """
    Tendremos que coger los prefijos cadavez que esta funcion se llame
    necesitamos pasar el mensage para ver el mensage del servidor

    Si el mensage es de un servidor:
    :return: El array con los prefijos ['?', '!', 'm.'] y con el prefijo personalizado
    
    Si es un mensage directo

    :return: $
    """
    if message.guild is not None:
        try:
            msg = str(message.content)
            id = str(f'<@!{bot.user.id}>')
            if id in msg or msg in f"<@!{bot.user.id}> prefijos":
                return ["$", '?', '!', 'm.']
            with open(env["JSON_DIR"] + 'prefix.json', 'r') as f:
                prefixes = json.load(f)
            if not str(message.guild.id) in prefixes:
                prefixes[str(message.guild.id)] = "$"
                with open(env["JSON_DIR"] + 'prefix.json', 'w') as f:
                    json.dump(prefixes, f) 
                return [prefixes[str(message.guild.id)], '?', '!', 'm.']
            base = [prefixes[str(message.guild.id)], '?', '!', 'm.']
            return commands.when_mentioned_or(base)(bot, message)
        except Exception as e:
            print(e)
            return ['$', '?', '!', 'm.']
    else:
        return "$" # Si no esta en un servidor retornar el prefjio "$"
