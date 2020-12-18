
# ? Activar el enviroment
# ? py -m venv env
# ? ".\env\Scripts\activate"
# ? "deactivate"

import sys, os
from pathlib import Path

from consola.main import Consola

from tqdm import tqdm 
from time import sleep 
import threading, discord
from termcolor import cprint

__autor__ = "Maubg"
__github__ = "https://github.com/maubg-debug/"
__repo__ = "https://github.com/maubg-debug/maubot/"
__version__ = "1.0.0"
__web__ = "https://maubot.maucode.com"

def cargar(texto, t):
    for i in tqdm(range(1, 100), desc=texto, leave=False): 
        sleep(t)

# class Env():
#     def coger_prefijo_compat(self):
#         return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

#     def es_virtualenv(self):
#         return self.coger_prefijo_compat() != sys.prefix

def preparar():

    from App import App

    from models.StdModels import StdModels

    from utils.DataStore import data_store
    from utils.Environment import env

    from std_cogs.StdCogs import StdCogs

    from utils.Logger.Logger import Logger
    from utils.prefix import prefix
    from utils.Version import is_min_python_3_6

    import colorama

    # ---------------------------------------------------------------------------------------------------------------------- #
    #       INIT COLORAMA
    # ---------------------------------------------------------------------------------------------------------------------- #
    colorama.init(autoreset=True)

    # ---------------------------------------------------------------------------------------------------------------------- #
    #       COMPRUEBE LA VERSION 3.X DE PYTHON
    # ---------------------------------------------------------------------------------------------------------------------- #
    print("Discord: " + str(discord.__version__))
    if not is_min_python_3_6:
        Logger.error('Maubot fue desarrollado para Python 3. Utilice la version 3.6 o superior.')
        sys.exit(1)

    # ---------------------------------------------------------------------------------------------------------------------- #
    #       LIBERACION DEL BOT
    # ---------------------------------------------------------------------------------------------------------------------- #
    env.set('VERSION_MAUBOT', "0.1")

    # ---------------------------------------------------------------------------------------------------------------------- #
    #       Base de datos INIT
    # ---------------------------------------------------------------------------------------------------------------------- #
    data_store.init_database(StdModels())

    # ---------------------------------------------------------------------------------------------------------------------- #
    #       EMPEZAR BOT
    # ---------------------------------------------------------------------------------------------------------------------- #

    cogs = StdCogs()

    # Chequeamos si es prueva
    prueva = "TOKEN"
    try:
        pruevas = env.get("PRUEVA")
        if pruevas == "True":
            prueva = "TOKEN_BOT_PRUEVAS"
        else:
            pruevas = "TOKEN"
    except EnvironmentError:
        prueva = "TOKEN"

    try:
        token = env.get(prueva)
    except EnvironmentError:
        Logger.error('No se encontro ninguna ficha. Ejecute el bot con el parametro --token (-t) <token> o inserte TOKEN = <token> en el archivo .env.')
        sys.exit(1)

    extrasenv = [
        "WEATHER_KEY", 
        "COMP_KEY", 
        "COLOR",
        "WEBHOOK_URL_ENTRADA",
        "WEBHOOK_URL_SALIDA",
        "WEBHOOK_URL_ERRORES",
        "DEBUG",
        "JSON_DIR",
        "DB_DIR",
        "USER_STATISTICS_THROTTLE_DURATION",
        "USER_STATISTICS_INCREMENT"
    ]

    for i in extrasenv:
        try:
            ex = env.get(str(i))
            if ex == "" or ex == " ":
                Logger.warning("Te falta rellenar el " + i + " en el .env, es posible que algunos comandos no funcionen")
        except: 
            Logger.warning("Te falta rellenar el " + i + " en el .env, es posible que algunos comandos no funcionen")
        
        
    if env.is_debug():
        Logger.warning('Modo de depuracion habilitado. Ejecute el bot sin el parametro --debug (-d) o inserte DEBUG=False en el archivo .env.')

    x = threading.Thread(target=cargar, args=("Cargando cogs", .01,))
    x.start()
    app = App(cogs, command_prefix=prefix.get_prefix, description="Maubot | El mejor bot para divertirse", help_command=None, activity=discord.Game(name="███████╗███████╗ ██╔════╝╚════██║ █████╗░░░░███╔═╝ ██╔══╝░░██╔══╝░░ ███████╗███████╗ ╚══════╝╚══════╝", afk=True))
    x.join()
    Logger.success("Las opciones del robot estan cargadas")

    y = threading.Thread(target=cargar, args=("Haciendo login", .01,))
    y.start()
    try:
        app.run(token)
        y.join()
    except Exception as e:
        y.join()
        cprint(f"Un error con el login: {e}", "red")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            if sys.argv[1] == "--help" or sys.argv[1] == "-h":
                Consola("help").procesar_comandos(directorio=Path(__file__).parent.parent)
                sys.exit(0)
            if sys.argv[2]:
                c = Consola(sys.argv[2]).procesar_comandos(directorio=Path(__file__).parent.parent)
                if c == "preparacion":
                    preparar()
        except Exception as e:
            print(e)
    else:
        cprint("\nPuedes poner help para ver la lista de comando\n", "green")
        while True:
            try:
                comando = input("Maubot -> ")
            except KeyboardInterrupt:
                cprint("\n\nSi quieres salir del programa deverias de poner \"exit()\"\n", "yellow")
                continue
            c = Consola(comando).procesar_comandos(directorio=Path(__file__).parent.parent)
            if c == "preparacion":
                preparar()