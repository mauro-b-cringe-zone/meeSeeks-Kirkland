from maubot import bot, main
from mauutils.secrete import TOKEN
import traceback, sys
from termcolor import cprint


initial_extensions = [
    # ACTUALIZAR LOS ROUTES
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