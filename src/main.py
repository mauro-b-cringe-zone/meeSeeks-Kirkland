# Activar el enviroment
# ".\env\Scripts\activate"
# "deactivate"

import sys

import colorama

from consola.main import Consola
from pathlib import Path

def preparar():
    from App import App
    from models.StdModels import StdModels
    from utils.DataStore import data_store
    from utils.Environment import env
    from std_cogs.StdCogs import StdCogs
    from utils.Logger.Logger import Logger
    from utils.prefix import prefix
    from utils.Version import is_min_python_3_6

    # ----------------------------------------------------------------------------------------------------------------------
    #       INIT COLORAMA
    # ----------------------------------------------------------------------------------------------------------------------
    colorama.init(autoreset=True)

    # ----------------------------------------------------------------------------------------------------------------------
    #      COMPRUEBE LA VERSIÓN 3.X DE PYTHON
    # ----------------------------------------------------------------------------------------------------------------------
    if not is_min_python_3_6:
        Logger.error('Maubot fue desarrollado para Python 3. Utilice la versión 3.6 o superior.')
        sys.exit(1)

    # ----------------------------------------------------------------------------------------------------------------------
    #       LIBERACIÓN DEL BOT
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
        Logger.error('No se encontró ninguna ficha. Ejecute el bot con el parámetro --token (-t) <token> o inserte TOKEN = <token> en el archivo .env.')
        sys.exit(1)

    if env.is_debug():
        Logger.warning('Modo de depuración habilitado. Ejecute el bot sin el parámetro --debug (-d) o inserte DEBUG=False en el archivo .env.')

    Logger.success('Las opciones del robot estan cargadas.')

    app = App(cogs, command_prefix=prefix.get_prefix, description="Maubot | El mejor bot para divertirse", help_command=None)

    app.run(token)




if __name__ == "__main__":
    while True:
        comando = input("Maubot> ")
        c = Consola(comando).procesar_comandos(directorio=Path(__file__).parent)
        if c == "preparacion":
            preparar()
        else:
            continue