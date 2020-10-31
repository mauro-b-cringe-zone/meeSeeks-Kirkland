import sys, json, asyncio

import discord
from discord import Activity, ActivityType
from discord.ext import commands

from utils.Environment import Environment, env
from utils.Logger.Logger import Logger
from cogs.Cogs import Cogs
from middleware import run_middleware_stack
from discord.ext.commands.errors import BotMissingPermissions, CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, NotOwner
from googletrans import Translator


class App(commands.Bot):
    __activity: Activity
    __cogs: Cogs

    def __init__(self, cogs: Cogs, **options):
        super().__init__(**options)

        self.__cogs = cogs
        self.color = int(env.get("COLOR"))

        self.help_url = "https://github.com/maubg-debug/maubot/issues/new?assignees=&labels=bug&template=reporte-de-bugs.md&title=BUG"

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
        while True:
            await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"|  $help  |  {len(self.users)} Usuarios en  {len(self.guilds)} servidores | con 186 commandos"))
            await asyncio.sleep(10) 
            await self.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"https://top.gg/bot/730124969132163093"))
            await asyncio.sleep(10)
            await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"| Enviando memes a los  {len(self.users)} usuarios | "))
            await asyncio.sleep(10)
            await self.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"| Mejorandome para dominar el mundo | "))
            await asyncio.sleep(10)
            await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"| Hackeando sistemas del pais | "))
            await asyncio.sleep(10)
            await self.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"| Haciendo una tarta | "))
            await asyncio.sleep(10)

    async def on_message(self, message):
        await run_middleware_stack(message)
        await self.process_commands(message)

    async def reaction(self, context, msg_error):
        def _check(reaction, user):
            return (
                reaction.emoji in '❌'
                and user == context.author
                and reaction.message.id == msg_error.id
            )
        try:
            reaction, user = await self.wait_for("reaction_add", timeout=9999999, check=_check)
        except  asyncio.TimeoutError:
            await msg_error.delete()
        else:
            await msg_error.delete()

    async def on_command_error(self, context, exception):
        env = Environment()

        

        exception_type = exception.__class__
        if exception_type:

            if isinstance(exception, CommandOnCooldown):
                embed = discord.Embed(title="Tranquilo...", description=f"{context.author.mention} Este comando esta en reposo\n Ahora tienes que esperar **{exception.retry_after:,.2f}** segundos", color=self.color)
                await context.send(embed=embed)

            elif isinstance(exception, commands.DisabledCommand):
                embed = discord.Embed(title="404", description=f"{context.author.mention} Este comando esta **desactivado** intentalo mas tarde", color=self.color)
                await context.send(embed=embed)

            elif isinstance(exception, commands.NotOwner):
                embed = discord.Embed(title="....", description=f"{context.author.mention} Este comando es para mi creador\n\nVete y consigue una vida.", color=self.color)
                await context.send(embed=embed)

            elif isinstance(exception, commands.NoPrivateMessage):
                embed = discord.Embed(title="NO", description=f"{context.author.mention} Este comando no es para canale de DM", color=self.color)
                await context.send(embed=embed)

            elif isinstance(exception, commands.TooManyArguments):
                embed = discord.Embed(description=f"{context.author.mention} Escribe menos argumentos por favor.", colour=0xc42323)
                embed.set_author(name="Demasiado", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)

            elif isinstance(exception, commands.BadArgument):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** {context.prefix}help" ** para mas informacion', colour=0xc42323)
                embed.set_author(name="Escribe un argumento valido", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)

            elif isinstance(exception, commands.MissingRequiredArgument):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** "{context.prefix}help" ** para mas informacion', colour=0xc42323)
                embed.set_author(name="Escribe todos los argumentos requeridos", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)


            elif isinstance(exception, commands.MissingPermissions):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** "{context.prefix}help" ** para mas informacion', colour=0xc42323)
                embed.set_author(name=f"Necesitas permisos para hacer esto", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.add_field(name="\uFEFF", value=f"Permisos necesarios: `{Translator().translate(str([perm.replace('_', ' ').replace('guild', 'server').title() for perm in exception.missing_perms]), src='en', dest='es').text}`")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)

            elif isinstance(exception, commands.MissingRole):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** {context.prefix}help" ** para mas informacion', colour=0xc42323)
                embed.set_author(name="Tienes que tener los roles correctos", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)

        excepciones = ['Command "cancelar" is not found', 'You are on cooldown.']

        if env.get('DEBUG'):
            if str(exception) in excepciones or str(exception).startswith(excepciones[1]):
                return
            await context.send(embed=discord.Embed(
                              title="Como saves los robots no son perfectos", 
                              description=f"Se ha producido un error, Visita: **[Nuestro github]({self.help_url})** \npara mencionarnos el error y enviarnos una captura de pantalla con el comando\n\nError: \n```{str(exception)}```",
                              color=self.color).set_footer(
                                  text="Maubot help | Solo envia bugs a github si son importantes, Si es un error de argumentos pon $help [seccion]"
                              ))
            Logger.error(f'ERROR: {str(exception)}')


    def __load_cogs(self):
        """
        Carga todos los engranajes en bot.
        :return:
        """
        for cog in self.__cogs.get():
            self.load_extension(cog)

    @staticmethod
    @commands.command(name="recargar-cogs")
    @commands.is_owner()
    async def __reload_cogs(ctx: commands.Context):
        """
        Un comando para recargar todos los cogs
        :param ctx: Command context.
        :return:
        """
        Logger.info(f'{ctx.author} desencadenó una recarga de engranajes.')
        await ctx.send(f'{ctx.message.author.mention} desencadenó una recarga.')

        try:
            for cog in ctx.bot.__cogs.get():
                ctx.bot.reload_extension(cog)
        except (commands.ExtensionNotLoaded,
                commands.ExtensionNotFound,
                commands.NoEntryPointError,
                commands.ExtensionFailed):
            message_error = 'Error al recargar piñones.'
            Logger.error(message_error)
            await ctx.send(message_error)

            return

        message_success = 'Cogs recargados.'
        Logger.success(message_success)
        await ctx.send(message_success)



    @staticmethod
    @commands.command(description="Cambia el prefijo")
    @commands.cooldown(1, 25, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def prefix(self, ctx, prefix):

        with open('./src/json/prefix.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('./src/json/prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        e = discord.Embed(title="**__Se a cambiado el prefijo correctamente__**", description=f'Se a cambiado el prefijo a:      `{prefix}`', colour=self.color)
        e.add_field(name="¡Tenemos un servidor!", value="**Unete a nuestro server  ->  (https://discord.gg/4gfUZtB)**")
        await ctx.send(embed=e)