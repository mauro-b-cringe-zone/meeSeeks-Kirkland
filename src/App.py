import sys

import discord
from discord import Activity, ActivityType
from discord.ext import commands

from utils.Environment import Environment
from utils.Logger.Logger import Logger
from cogs.Cogs import Cogs
from middleware import run_middleware_stack
from discord.ext.commands.errors import BotMissingPermissions, \
    MissingPermissions, \
    NotOwner, \
    MissingRequiredArgument, \
    CommandNotFound


class App(commands.Bot):
    __activity: Activity
    __cogs: Cogs

    def __init__(self, cogs: Cogs, **options):
        super().__init__(**options)

        self.__cogs = cogs

        # Try to load cogs
        try:
            self.__load_cogs()
        except (commands.ExtensionNotLoaded,
                commands.ExtensionNotFound,
                commands.NoEntryPointError,
                commands.ExtensionFailed) as e:
            Logger.error(f'Error cargando cogs. {e}')
            sys.exit(1)

        self.add_command(App.__reload_cogs)

    async def on_ready(self):
        Logger.success(f'Maubot esta online como "{self.user}".', separador=True)
        # await self.change_presence(activity=self.__activity)
        

    async def on_message(self, message):
        await run_middleware_stack(message)
        await self.process_commands(message)

    async def on_command_error(self, context, exception):
        env = Environment()

        

        message = {
            BotMissingPermissions: lambda err: f'Te faltan los permisos del robot: {", ".join(err.missing_perms)}.',
            MissingPermissions: lambda err: f'No tienes permisos para esta accion: {", ".join(err.missing_perms)}',
            NotOwner: lambda err: 'Necesitas permisos: Tu no eres el creador.',
            MissingRequiredArgument: lambda err: f'Falta un argumento: Pon **"{context.prefix}help"**.',
        }

        exception_type = exception.__class__
        if exception_type in message:
            await context.send(message[exception_type](exception))
        elif env.get('DEBUG'):
            await context.send(
                'Se ha producido un error, Visita:'
                ' **https://github.com/maubg-debug/maubot/issues**'
                ' para mencionarnos el error'
            )
            Logger.error(f'ERROR: {str(exception)}')

    def __load_cogs(self):
        """
        Load all cogs into bot.
        :return:
        """
        for cog in self.__cogs.get():
            self.load_extension(cog)

    @staticmethod
    @commands.command(name="recargar-cogs")
    @commands.is_owner()
    async def __reload_cogs(ctx: commands.Context):
        """
        Command to reload all cogs.
        :param ctx: Command context.
        :return:
        """
        # Inform user that reload began
        Logger.info(f'{ctx.author} triggered a reload of cogs.')
        await ctx.send(f'{ctx.message.author.mention} triggered a reload.')

        try:
            for cog in ctx.bot.__cogs.get():
                ctx.bot.reload_extension(cog)
        except (commands.ExtensionNotLoaded,
                commands.ExtensionNotFound,
                commands.NoEntryPointError,
                commands.ExtensionFailed):
            # Inform User that reload was not successful
            message_error = 'Error on reloading cogs.'
            Logger.error(message_error)
            await ctx.send(message_error)

            return

        # Inform User that reload was successful
        message_success = 'Cogs reloaded.'
        Logger.success(message_success)
        await ctx.send(message_success)

