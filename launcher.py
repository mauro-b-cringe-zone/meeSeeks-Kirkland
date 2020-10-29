from dotenv import load_dotenv
load_dotenv(verbose=True)

import traceback, sys
from termcolor import cprint
import os       
from time import sleep

"""Para actualizar los requirements `pip freeze > requirements.txt`"""


def preparar():
    from maubot import bot, main
    from mauutils.secrete import TOKEN
    try:
        for filename in os.listdir('./cogs/economy'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.economy.{filename[:-3]}')
                cprint(str("[Cog] " + 'cogs.economy.'+filename[:-3]+' ...Hecho'), 'green')
        for filename in os.listdir('./cogs/eventos'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.eventos.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.eventos.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/fun'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.fun.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.fun.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/fun/social'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.fun.social.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.fun.social.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/fun/http_cmds'):
            if filename.endswith('.py') and filename.startswith("cmd_"):
                bot.load_extension(f'cogs.fun.http_cmds.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.fun.http_cmds.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/imgs'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.imgs.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.imgs.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/general'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.general.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.general.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/lang'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.lang.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.lang.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/moderacion'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.moderacion.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.moderacion.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/musica'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.musica.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.musica.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/spotify'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.spotify.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.spotify.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('./cogs/tags'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.tags.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.tags.'+filename[:-3]+' ...Hecho', 'green')
        bot.load_extension(f'help.help')
        cprint("[Help] " + 'help.help ...Hecho', 'yellow')
    except Exception as e:
        cprint(str(f'[Log] Se a fallado al cargar todas las extensiones cogs.+{filename[:-3]}.', file=sys.stderr), 'red')
        traceback.print_exc()

    try:
        sleep(1)
        os.system("cls")
        main()
        # cprint(f"\n\nTOKEN:  {TOKEN}", 'blue')
        bot.run(f"{TOKEN}")
        # "Maubot>  "
    except Exception as e:
        cprint(f"[Log] Error en el login: {e}", 'red')

class Consola():
    def __init__(self, comando):
        self.comando = comando
        self.preparar = preparar

    def pip(self, pack):
        os.system(f"pip install {pack}")

    def procesar_comandos(self):
        if self.comando == "":
            return True
        elif self.comando == "empezar" or self.comando == "run":
            self.preparar()
        elif self.comando == "cls" or self.comando == "clear":
            for i in range(10):
                print("\n")
        elif self.comando.startswith("pip"):
            mod = comando.split("pip")
            self.pip(mod[1])
        elif self.comando == "exit" or self.comando == "salir":
            print("\nSi quieres salir del programa deverias de poner \"exit()\"\n")
        elif self.comando == "instalar":
            os.system("pip install -r requirements.txt")
            cprint("\n\nAHORA VE HA '.example.env' Y RELLENA TODO LO NECESARIO Y YA DE PASO CAMBIA EL .example.env A .env \n\n", "green")
        elif self.comando == "exit()":
            exit(0)
        else:
            cprint("\nAyuda:\n-> exit()\n-> pip <modulo>\n-> cls (clear)\n-> run (empezar)\n-> instalar\n", "green")

if __name__ == "__main__":
    while True:
        comando = input("Maubot> ")

        Consola(comando).procesar_comandos()