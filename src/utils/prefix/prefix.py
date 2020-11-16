import json
from os import environ as env
from discord.ext import commands
from termcolor import cprint

def get_prefix(bot, message):
    """
    Tendremos que coger los prefijos cadavez que esta funcion se llame
    necesitamos pasar el mensage para ver el mensage del servidor

    Si el mensage es de un servidor:
    :return: El array con los prefijos ['m.', 'm-'] y con el prefijo personalizado
    
    Si es un mensage directo

    :return: $@dl.@# (Algo dificil)
    """
    if message.guild is not None:
        try:
            msg = str(message.content)
            id = str(f'<@!{bot.user.id}>')
            if id == msg or msg == f"<@!{bot.user.id}> prefijos":
                return ['m.', 'm-', "$"]
            with open(env["JSON_DIR"] + 'prefix.json', 'r') as f:
                prefixes = json.load(f)
            if not str(message.guild.id) in prefixes:
                prefixes[str(message.guild.id)] = "$"
                with open(env["JSON_DIR"] + 'prefix.json', 'w') as f:
                    json.dump(prefixes, f) 
                return [prefixes[str(message.guild.id)], 'm.', 'm-']
            base = [prefixes[str(message.guild.id)], 'm.', 'm-']
            return commands.when_mentioned_or(*base)(bot, message)
        except Exception as e:
            cprint(f"{e}")
            return ['m.', 'm-', "$"]
    else:
        return "$@dl.@#" # Si no esta en un servidor retornar el prefjio "$@dl.@#" (Algo dificil)
