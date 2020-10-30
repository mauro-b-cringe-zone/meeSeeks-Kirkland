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

    finally:
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
        self.comando = comando.lower()
        self.preparar = preparar
        self.comandos = [["empezar", "run"], ["cls", "clear"], "pip", ["exit", "salir", "exit()"], "instalar", "python", ["help", "ayuda"], "instrucciones"]

    def pip(self, pack):
        os.system(f"pip install {pack}")

    def python(self):
        os.system("python")

    def instrucciones(self, dir):
        cprint(f"\nTutorial de como usar Maubot\n\n1. Ve ha 'https://asciinema.org/a/P8nJyagpVvdjVmj1nPnKHCyHy' y sigue las instrucciones\n2. Rellena todo lo que necesites en {dir}.example.env rellenalo y camviale el nombre a .env\n3. ve ha {dir}\launcher.py \n4. Pon en la consola python launcher.py y despues pon 'run' \n", "green")

    def procesar_comandos(self, directorio):
        if self.comando == "":
            return True
        
        elif self.comando == self.comandos[0][0] or self.comando == self.comandos[0][1]:
            cprint("\nCTRL + C para parar el programa e iniciar la consola\n", "red")
            sleep(2)
            self.preparar()
        
        elif self.comando == self.comandos[1][0] or self.comando == self.comandos[1][1]:
            os.system("cls" or "clear")
        
        elif self.comando.startswith("pip"):
            mod = comando.split("pip")
            self.pip(mod[1])
        
        elif self.comando == self.comandos[3][0] or self.comando == self.comandos[3][1]:
            cprint("\nSi quieres salir del programa deverias de poner \"exit()\"\n", "yellow")

        elif self.comando == self.comandos[4]:
            os.system("pip install -r requirements.txt")
            cprint(f"\n\n1. AHORA VE HA '{directorio}\.example.env' \n2. RELLENA TODO LO NECESARIO Y YA DE PASO CAMBIA EL '{directorio}\.example.env' A '{directorio}\.env' \n\n", "green")
        
        elif self.comando == self.comandos[5]:
            self.python()
        
        elif self.comando == self.comandos[3][2]:
            exit(0)

        elif self.comando == self.comandos[7]:
            self.instrucciones(directorio)

        elif self.comando == self.comandos[6][1] or self.comando == self.comandos[6][0]:
            cprint("\nAyuda:\n-> exit() - Se sale del programa\n-> pip <modulo> - Instalar un modulo con pip\n-> cls (clear) - Limpiar la consola\n-> run (empezar) - Correr maubot\n-> instalar - Instalar lo necesario para maubot (RECOMENDABLE SI ES LA PRIMERA VEZ QUE USAS MAUBOT)\n-> help (ayuda) - Enseña este mensage\n-> instrucciones - Te esñara como utilizar maubot\n", "green")
        
        else:
            cprint(f"\n{self.comando} no existe:\n-> Prueva a poner \"ayuda\" o \"help\"\n", "red")

if __name__ == "__main__":
    from pathlib import Path
    cprint("\nPon \"instrucciones\" Si es la primera vesz que usas maubot <- o -> \"help\" para ver la lista de ayudas\n", "yellow")
    while True:
        comando = input(f"{Path(__file__).parent} -> ")
        Consola(comando).procesar_comandos(directorio=Path(__file__).parent)