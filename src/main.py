# Activar el enviroment
# # py -m venv env
# ".\env\Scripts\activate"
# "deactivate"

import sys
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

    try:
        token = env.get('TOKEN')
        color = int(env.get('COLOR'))
    except EnvironmentError:
        Logger.error('No se encontro ninguna ficha. Ejecute el bot con el parametro --token (-t) <token> o inserte TOKEN = <token> en el archivo .env.')
        sys.exit(1)

    if env.is_debug():
        Logger.warning('Modo de depuracion habilitado. Ejecute el bot sin el parametro --debug (-d) o inserte DEBUG=False en el archivo .env.')

    Logger.success('Las opciones del robot estan cargadas.')

    app = App(cogs, command_prefix=prefix.get_prefix, description="Maubot | El mejor bot para divertirse")
    app.remove_command("help")

    app.run(token)

if __name__ == "__main__":
    # print(sys.argv[2])
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
