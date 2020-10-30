import sys

import colorama

from consola.main import Consola
from pathlib import Path
directorio = str(Path.home().parent)

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

    app = App(cogs, command_prefix=prefix.get_prefix, description="Maubot | El mejor bot para divertirse")
    app.remove_command('help')


    app.run(token)
    app.add_cog(Main(app))

if __name__ == "__main__":
    while True:
        comando = input("Maubot> ")
        c = Consola(comando).procesar_comandos(directorio)

        if c == "preparacion":
            preparar()
        else:
            continue

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# 
#   CLASE MAIN
# 
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

import discord, asyncio, json
from discord.ext import commands

class Main(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await self.app.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"|  $help  |  {len(self.app.users)} Usuarios en  {len(self.app.guilds)} servidores | con 186 commandos"))
            await asyncio.sleep(10) 
            await self.app.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"https://top.gg/bot/730124969132163093"))
            await asyncio.sleep(10)
            await self.app.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"| Enviando memes a los  {len(self.app.users)} usuarios | "))
            await asyncio.sleep(10)
            await self.app.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"| Mejorandome para dominar el mundo | "))
            await asyncio.sleep(10)
            await self.app.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"| Hackeando sistemas del pais | "))
            await asyncio.sleep(10)
            await self.app.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"| Haciendo una tarta | "))
            await asyncio.sleep(10)

    @commands.command(description="Cambia el prefijo")
    @commands.cooldown(1, 25, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def prefix(self, ctx, prefix):

        with open('./src/json/prefix.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('./src/json/prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        e = discord.Embed(title="**__Se a cambiado el prefijo correctamente__**", description=f'Se a cambiado el prefijo a:     `{prefix}`', colour=color)
        e.add_field(name="¡Tenemos un servidor!", value="**Unete a nuestro server  ->  (https://discord.gg/4gfUZtB)**")
        await ctx.send(embed=e)
