from peewee import SqliteDatabase, Database, InterfaceError, OperationalError

from models.Models import Models
from utils.Environment import env
from utils.Logger.Logger import Logger


class DataStore:
    """
    Contenedor de singleton para __DataStore.
    """

    class __DataStore:
        __db = Database

        def __init__(self):
            self.__db = SqliteDatabase(env.get("DB_DIR") + 'data.db')

        def __open_connection(self):
            """
            Conexión de base de datos abierta.
            :return: indica si la conexión está abierta.
            """
            Logger.info('- Conexión de base de datos abierta... ', newline=False)
            try:
                self.__db.close()
                self.__db.connect()
                Logger.success('Hecho.')
            except (InterfaceError, OperationalError):
                Logger.error('No se pudo establecer la conexión con la base de datos.')
                return False

            return True

        def __create_tables(self, models: Models):
            """
            Crea tablas de base de datos.
            :param modelos: modelos para crear tablas.
            :return:
            """
            Logger.info('- Inicializar tablas de base de datos... ', newline=False)
            try:
                self.__db.create_tables(models.get())
                Logger.success('Hecho.')
            except ValueError:
                Logger.error('No se pudieron crear tablas de base de datos.')

        def init_database(self, models: Models):
            """
            Abra la conexión y cree tablas.
            :param modelos: modelos para crear tablas.
            :return:
            """
            Logger.separador()
            Logger.info('Inicializar base de datos')

            is_connection_open = self.__open_connection()

            if is_connection_open:
                self.__create_tables(models)
                Logger.info('Base de datos inicializada')
            else:
                Logger.error('Base de datos no inicializada')

            Logger.separador()

        def get_database(self):
            """
            Obtener base de datos.
            :return: Devuelve la base de datos.
            """
            return self.__db

    __instance = None

    def __new__(cls):
        if DataStore.__instance is None:
            DataStore.__instance = DataStore.__DataStore()

        return DataStore.__instance

    def __getattr__(self, item):
        return getattr(self.__instance, item)

    def __setattr__(self, key, value):
        return setattr(self.__instance, key, value)
