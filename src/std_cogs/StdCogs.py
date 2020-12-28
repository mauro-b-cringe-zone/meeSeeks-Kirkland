import os

from cogs.Cogs import Cogs
from utils.Environment import env

class StdCogs(Cogs):
    __STD_COG_PATH = 'std_cogs'
    __cogs: list
    __cog_path: str

    def __mas_cmds(self, archivo, nombre_archivo):
        if nombre_archivo == "http_cmds":
            for i in os.listdir(f"{self.__cog_path}/{archivo}/{nombre_archivo}"):
                if i.startswith("cmd_"):
                    self.__cogs.append(f"std_cogs.fun-cog.http_cmds.{i[:-3]}")
                return True
        return False

    def __init__(self):
        self.__cog_path = f'{env.get("BOT_ROOT_PATH")}/{self.__STD_COG_PATH}'
        self.__cogs = []
        for archivo in os.listdir(self.__cog_path):
            if archivo != "__pycache__":
                if self.__es_cog(archivo):
                    for nombre_archivo in os.listdir(f"{self.__cog_path}/{archivo}"):
                        _mas__cmd = self.__mas_cmds(archivo, nombre_archivo)
                        if _mas__cmd: continue
                        if nombre_archivo.endswith(".py"):
                            self.__cogs.append(f'std_cogs.{archivo}.{nombre_archivo[:-3]}')

        self.__cogs.append("utils.help.main")
        self.__cogs.append("App")

    def __es_cog(self, archivo: str):
        return archivo.endswith('-cog')

    def get(self):
        return self.__cogs
