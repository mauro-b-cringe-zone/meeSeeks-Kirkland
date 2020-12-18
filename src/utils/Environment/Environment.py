import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from os import environ as env

from utils.Logger.Logger import Logger


class Environment:
    """
    Envoltorio singleton para __Environment.
    """

    class __Environment:
        __args: argparse.Namespace = None
        __env_file_exists: bool = False

        def __init__(self):
            """
            Vaciar chat en caso de que estemos reiniciando
            Para que el texto no se haga lioso
            Tambien miaremos si el usuario esta en 'linux' o 'windows'
            """

            if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):  
                os.system("cls")
            else:
                os.system("clear")

            # Init
            Logger.separador()
            Logger.info('Preparar el entorno.')

            # Establecer ruta raíz
            Logger.info('- Establecer ruta raíz... ', newline=False)
            root_path = Path(f'{__file__}/').parent.parent.parent.absolute()
            if not os.path.isfile(f'{root_path}/main.py'):
                Logger.error('No se pudo encontrar la carpeta raíz.')
                sys.exit(1)
            self.set('BOT_ROOT_PATH', str(root_path))
            Logger.success('Hecho.')

            # Analizar argumentos
            Logger.info('- Analizar argumentos... ', newline=False)
            self.__args = self.__cojer_arg_parser().parse_args()
            Logger.success('Hecho.')

            # Inicio directorio inicial
            Logger.info('- Directorio inicial de inicio... ', newline=False)
            home_dir = self.__get_home_dir()
            self.set('MAUBOT_DIRECCION_DE_CASA', home_dir)
            #self.set(f'{env["DB_DIR"]}data.db', f'{env["DB_DIR"]}data.db')
            Logger.success('Hecho.')

            # Cargar .env
            Logger.info('- Cargar .env... ', newline=False)
            self.__env_file_exists = self.__read_env(root_path)
            if self.__env_file_exists:
                Logger.success('Hecho.')
            if self.__env_file_exists:
                Logger.success('Hecho.')
            else:
                Logger.warning('.env No existe.')
                ENVFILE = Path(__file__).parent.parent.parent.parent / ".env"
                Logger.warning("Es posible que no ayas cambiado el .example.env a .env. Si no es asi porfavor pon [y] para crearte un .env")
                conf = input("Parece que no existe el archivo .env ¿Quieres crear uno? [y/n]: ")
                if conf == "y":
                    token = input("Introduce el token: ")
                    with Path.open(ENVFILE, 'w', encoding='utf-8') as file:
                        file.write(f"TOKEN={token}\n")
                        file.write("WEATHER_KEY = \n")
                        file.write("COMP_KEY = \n")
                        file.write("COLOR = 16777215\n")
                        file.write("USER_STATISTICS_THROTTLE_DURATION =5\n")
                        file.write("USER_STATISTICS_INCREMENT = 10\n")
                        file.write("DEBUG = True\n")
                        file.write("WEBHOOK_URL = \n")
                        file.write("JSON_DIR = \n")
                        file.write("DB_DIR = \n")
                    print(f"Entra en el .env y sigue los pasos")
                    hecho = input("Cuando ayas terminado pon [Y] para empezar de nuevo, o pon [n] para terminar el programa (https://github.com/maubg-debug/maubot/blob/main/.example.env): ")
                    if hecho == "y":
                        Logger.success("> python ./src/main.py --cmd run")
                        sys.exit(0)
                    else:
                        sys.exit(0)
                else:
                    sys.exit(0)

            # Init final
            Logger.success('Ambiente preparado.')
            Logger.separador()

        def __cojer_arg_parser(self):
            """
            Preparar argparser.
            :return: argparser.
            """
            parser = argparse.ArgumentParser(description='Ejecutar argumentos en maubot')
            parser.add_argument('--token', '-t', help='define tu secreto de discord', type=str)
            # parser.add_argument('--prefix', help='define el prefijo de maubot', type=str)
            parser.add_argument('--debug', '-d', help='activa el modo de depuración', type=bool)
            parser.add_argument('--cmd', '-c', help='activa el modo de depuración', type=str)
            return parser

        def __get_home_dir(self):
            """
            Prepara el directorio de inicio.
            :return: Ruta del directorio de inicio.
            """
            home = f'{Path.home()}/.maubot/'
            # print(home)

            if not Path.home().is_dir():
                Logger.error('No home directory found.')
                sys.exit(1)

            if not os.path.isdir(home):
                try:
                    os.mkdir(home)
                except Exception:
                    Logger.error('Falta el permiso de escritura en el directorio de inicio.')
                    sys.exit(1)

            return f'{Path.home()}/.maubot/'

        def __read_env(self, root_path: Path):
            """
            Leer archivo .env.
            :return: indica si env existe o no.
            """
            env_file = None
            env_file_root = f'{root_path}/../.env'
            if os.path.exists(env_file_root) and os.path.isfile(env_file_root):
                env_file = env_file_root
            elif os.path.isfile(f'{os.getenv("MAUBOT_DIRECCION_DE_CASA")}/.env'):
                env_file = f'{os.getenv("MAUBOT_DIRECCION_DE_CASA")}/.env'

            if env_file is not None:
                load_dotenv(env_file)

            return env_file is not None

        def get(self, name: str):
            """
            Obtenga la variable de entorno.
            Se transforma en inferior para argumento y superior para entorno.
            :genera EnvironmentError: aumenta si no se encuentra la variable.
            :nombre del parámetro: Nombre de la variable.
            :retorno: Valor de la variable.
            """
            name_lower = name.lower()
            name_upper = name.upper()
            if hasattr(self.__args, name_lower) and getattr(self.__args, name_lower) is not None:
                return getattr(self.__args, name_lower)
            elif self.__env_file_exists and os.getenv(name_upper) is not None:
                return os.getenv(name_upper)

            raise EnvironmentError(f'No se ha encontrado el atribbuto {name}.')

        def set(self, name: str, value):
            """
            Establece la variable de entorno.
            :nombre del parámetro: Nombre de la variable. Se transformará en mayúsculas.
            :param value: Valor de la variable.
            :return:
            """
            os.environ[name.upper()] = value

        def is_debug(self):
            try:
                debug = self.get('DEBUG') == 'True'
            except EnvironmentError:
                debug = False

            return debug


    __instance = None

    def __new__(cls):
        if Environment.__instance is None:
            Environment.__instance = Environment.__Environment()

        return Environment.__instance

    def __getattr__(self, item):
        return getattr(self.__instance, item)

    def __setattr__(self, key, value):
        return setattr(self.__instance, key, value)
