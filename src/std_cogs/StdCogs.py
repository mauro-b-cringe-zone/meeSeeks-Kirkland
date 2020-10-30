import os

from cogs.Cogs import Cogs
from utils.Environment import env


class StdCogs(Cogs):
    __STD_COG_PATH = 'std_cogs'
    __cogs: list
    __cog_path: str

    def __init__(self):
        self.__cog_path = f'{env.get("BOT_ROOT_PATH")}/{self.__STD_COG_PATH}'
        self.__cogs = []
        for archivo in os.listdir(self.__cog_path):
            if archivo != "__pycache__":
                if self.__es_cog(archivo):
                    for nombre_archivo in os.listdir(f"{self.__cog_path}/{archivo}"):
                        if not nombre_archivo.startswith("__py"):
                            if not nombre_archivo.endswith(".txt"):
                                if not nombre_archivo.endswith("_cmds"):
                                    self.__cogs.append(f'std_cogs.{archivo}.{nombre_archivo[:-3]}')
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue

    def __es_cog(self, archivo: str):
        return archivo.endswith('-cog')

    def get(self):
        return self.__cogs
