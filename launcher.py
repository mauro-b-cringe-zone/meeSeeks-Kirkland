from maubot import bot, main
from mauutils.secrete import TOKEN
import traceback, sys
from termcolor import cprint


initial_extensions = [
    'cogs.preguntas',
    'cogs.general',
    'cogs.musica',
    'cogs.creador',
    'cogs.fun.pikachu',
    'cogs.fun.google',
    'cogs.fun.anime',
    'cogs.fun.animequote',
    'cogs.fun.urban',
    'cogs.fun.img_man_avatar_url',
    'cogs.fun.social.wasted',
    'cogs.fun.social.kiss',
    'cogs.fun.social.wink',
    'cogs.fun.social.sleep',
    'cogs.fun.social.pat',
    'cogs.fun.social.shrug',
    'cogs.fun.social.pout',
    'cogs.fun.social.facepalm',
    'cogs.fun.social.cry',
    'cogs.bola8',
    'cogs.pasword',
    'cogs.fun.http_cmds.colors',
    'cogs.fun.http_cmds.animales',
    'cogs.fun.http_cmds.supreme',
    'cogs.fun.http_cmds.minecraft',
    'cogs.fun.hangman',
    'cogs.documentation',
    'cogs.juegos',
    'cogs.traducir_binario',
    'cogs.weather',
    'cogs.img_man',
    'cogs.fun.http_cmds.steam',
    'cogs.spotify.spotify',
    'cogs.economy.main',
    'cogs.fun.tts',
    'cogs.on_message',
    'cogs.help',
    'cogs.AFK',
    'cogs.fun.social.nuke',
    'cogs.moderacion',
    'cogs.lang.execucion',
    'cogs.tags.__main__'
]           

"""Para actualizar los requirements `pip freeze > requirements.txt`"""

if __name__ == "__main__":
    main()
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            cprint("[Cog] " + extension+' ...Hecho', 'green')
        except Exception as e:
            cprint(str(f'[Log] Se a fallado al cargar todas las extensiones {extension}.', file=sys.stderr), 'red')
            traceback.print_exc()


try:
    bot.run(TOKEN)
except Exception as e:
    cprint(f"[Log] Error en el login: {e}", 'red')