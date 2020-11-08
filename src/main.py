# Activar el enviroment
# # py -m venv env
# ".\env\Scripts\activate"
# "deactivate"

import sys, os
from pathlib import Path

from consola.main import Consola

__autor__ = "Maubg"
__github__ = "https://github.com/maubg-debug/"
__repo__ = "https://github.com/maubg-debug/maubot/"
__version__ = "1.0.0"
__web__ = "http://maubot.mooo.com"

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

    # ----------------------------------------------------------------------------------------------------------------------
    #       INIT COLORAMA
    # ----------------------------------------------------------------------------------------------------------------------
    colorama.init(autoreset=True)

    # ----------------------------------------------------------------------------------------------------------------------
    #       COMPRUEBE LA VERSION 3.X DE PYTHON
    # ----------------------------------------------------------------------------------------------------------------------
    if not is_min_python_3_6:
        Logger.error('Maubot fue desarrollado para Python 3. Utilice la version 3.6 o superior.')
        sys.exit(1)

    # ----------------------------------------------------------------------------------------------------------------------
    #       LIBERACION DEL BOT
    # ----------------------------------------------------------------------------------------------------------------------
    env.set('VERSION_MAUBOT', "0.1")

    # ----------------------------------------------------------------------------------------------------------------------
    #       Base de datos INIT
    # ----------------------------------------------------------------------------------------------------------------------
    data_store.init_database(StdModels())

    # ----------------------------------------------------------------------------------------------------------------------
    #       EMPEZAR BOT
    # ----------------------------------------------------------------------------------------------------------------------

    cogs = StdCogs()
    ENVFILE = Path(__file__).parent / "secret.env"
    if ENVFILE.exists():
        try:
            token = env.get('TOKEN')
        except EnvironmentError:
            Logger.error('No se encontro ninguna ficha. Ejecute el bot con el parametro --token (-t) <token> o inserte TOKEN = <token> en el archivo .env.')
            sys.exit(1)

        extrasenv = ["WEATHER_KEY", "COMP_KEY", "COLOR"]
        for i in extrasenv:
            try:
                ex = env.get(f'{i}')
                if ex == "" or ex == " ":
                    Logger.warning(f"Te falta rellenar el {i} en el .env, es posible que algunos comandos no funcionen")
            except:
                Logger.warning(f"Te falta rellenar el {i} en el .env, es posible que algunos comandos no funcionen")
    else:
        Logger.warning("Es posible que no ayas cambiado el .example.env a .env. Si no es asi porfavor pon [y] para crearte un .env")
        conf = input("Parece que no existe el archivo .env ¿Quieres crear uno? [y/n]: ")
        if conf == "y":
            token = input("Introduce el token: ")
            with Path.open(ENVFILE, 'w', encoding='utf-8') as file:
                file.write(f"TOKEN={token}")
                file.write("WEATHER_KEY = https://openweathermap.org/api")
                file.write("COMP_KEY = ")
                file.write("COLOR = https://github.com/maubg-debug/maubot#instrucciones-para-el-color-del-env")
                file.write("USER_STATISTICS_THROTTLE_DURATION =5")
                file.write("USER_STATISTICS_INCREMENT = 10")
                file.write("DEBUG = True|False")
                file.write("WEBHOOK_URL = https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks")
                file.write("JSON_DIR = Tu direccion para los json")
                file.write("DB_DIR = Tu direccion para la DB")
            print(f"Entra en el .env y sigue los pasos")
            hecho = input("Cuando ayas terminado pon [Y] para empezar de nuevo, o pon [n] para terminar el programa: ")
            if hecho == "y":
                os.system("python ./src/main.py --cmd run")
            else:
                sys.exit(0)
        else:
            sys.exit(0)
        
    if env.is_debug():
        Logger.warning('Modo de depuracion habilitado. Ejecute el bot sin el parametro --debug (-d) o inserte DEBUG=False en el archivo .env.')

    Logger.success('Las opciones del robot estan cargadas.')

    app = App(cogs, command_prefix=prefix.get_prefix, description="Maubot | El mejor bot para divertirse", help_command=None)

    app.run(token)

if __name__ == "__main__":
    try:
        if sys.argv[1]:
            if sys.argv[1] == "--help" or sys.argv[1] == "-h":
                Consola("help").procesar_comandos(directorio=Path(__file__).parent.parent)
                sys.exit(0)
            if sys.argv[2]:
                c = Consola(sys.argv[2]).procesar_comandos(directorio=Path(__file__).parent.parent)
                if c == "preparacion":
                    preparar()
    except:
        while True:
            comando = input("Maubot> ")
            c = Consola(comando).procesar_comandos(directorio=Path(__file__).parent.parent)
            if c == "preparacion":
                preparar()
            else:
                continue
