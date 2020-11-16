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

import random
import datetime
import aiohttp

color = int(env.get("COLOR"))

class App(commands.Bot):
    __activity: Activity
    __cogs: Cogs

    def __init__(self, cogs: Cogs, **options):
        super().__init__(**options)

        self.__autor__ = "Maubg"
        self.__github__ = "https://github.com/maubg-debug/"
        self.__repo__ = "https://github.com/maubg-debug/maubot"
        self.__version__ = "1.0.0"      
        self.__web__ = "http://maubot.mooo.com"

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

        self.add_command(App.__reload_cogs)
    
    async def barra_de_actividad(self, texto, status, ver=None, li=None):
        if li:
            await self.change_presence(status=status, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{texto} - Maubot"))
        if ver:
            await self.change_presence(status=status, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{texto} - Maubot"))
        await self.change_presence(status=status, activity=discord.Game(name=f"{texto} - Maubot"))
        await asyncio.sleep(4)

    async def on_ready(self):
        Logger.success(f"--------------------------------------------------------------------------------------------------\nInfo: \n1. Autor              | {self.__autor__}\n2. Github del creador | {self.__github__}\n3. Repo de maubot     | {self.__repo__}\n4. Version            | {self.__version__}\n5. Web                | {self.__web__}", separador=False)
        Logger.success(f'Maubot esta online como "{self.user}".', separador=True)
        # await self.change_presence(activity=self.__activity)
        while True:
            # await self.barra_de_actividad(f"|  $help  |  {len(self.users)} Usuarios en  {len(self.guilds)} servidores | con 186 commandos", discord.Status.do_not_disturb)
            await self.barra_de_actividad(f"|-> Processando $help y @mencion ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> ¡Mirame en top.gg y bots.ondiscord.xyz! ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> Preparandome para matar ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> Hackeando el systema de la nasa ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> Cambiando el codigo fuente de google ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> Troleando a mis espias ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> Enviando mensages a los de la policia ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> Cambiando contraseña en discord ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> Sirviendo té a mi amo ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> Mejorando mi web ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> Haciendo una tarta con chocolate ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> Haciendo PVPs contra niños de 9 años en mc ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> Mirando por la dark web ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> Tutoriales de como abrir puertas ", discord.Status.dnd, ver=True)
            await self.barra_de_actividad(f"|-> a un dios ", discord.Status.idle, li=True)
            await self.barra_de_actividad(f"|-> haqueando la webcam de el presidente de UUEE ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> FORTNITE ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> MINECRAFT ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> Haciendo deveres ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> PUBG ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHH ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> A mimir ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> Conseguir gemas en dungeons and drugons ", discord.Status.dnd)
            await self.barra_de_actividad(f"|-> Defendiendo a los robots ", discord.Status.idle)
            await self.barra_de_actividad(f"|-> Viendo el lenguage universal (Python ;v) ", discord.Status.idle)


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
                embed = discord.Embed(description=f"{context.author.mention} Escribe menos argumentos por favor.", colour=0xf15069)
                embed.set_author(name="Demasiado", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)

            elif isinstance(exception, commands.BadArgument):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** {context.prefix}help" ** para mas informacion', colour=0xf15069)
                embed.set_author(name="Escribe un argumento valido", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)

            elif isinstance(exception, commands.MissingRequiredArgument):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** "{context.prefix}help" ** para mas informacion', colour=0xf15069)
                embed.set_author(name="Escribe todos los argumentos requeridos", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)


            elif isinstance(exception, commands.MissingPermissions):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** "{context.prefix}help" ** para mas informacion', colour=0xf15069)
                embed.set_author(name=f"Necesitas permisos para hacer esto", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.add_field(name="\uFEFF", value=f"Permisos necesarios: `{Translator().translate(str([perm.replace('_', ' ').replace('guild', 'server').title() for perm in exception.missing_perms]), src='en', dest='es').text}`")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)

            elif isinstance(exception, commands.MissingRole):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** {context.prefix}help" ** para mas informacion', colour=0xf15069)
                embed.set_author(name="Tienes que tener los roles correctos", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                embed.set_footer(text='\n-- ERROR')
                msg_error = await context.send(embed=embed)
                await msg_error.add_reaction('❌')
                await self.reaction(context, msg_error)

        excepciones = ['command is disabled', 'Command "cancelar" is not found', 'You are on cooldown.', "KeyError: 'run'", "Unknown Emoji", "AttributeError: 'NoneType' object has no attribute 'id'", "AttributeError: 'ClientUser' object has no attribute 'send'", "is not found"]

        if env.get('DEBUG'):
            for i in excepciones:
                if i in str(exception):
                    return
            await context.send(embed=discord.Embed(
                              title="Como sabes, los robots no son perfectos", 
                              description=f"Se ha producido un error, Visita: **[Nuestro github]({self.help_url})** \npara mencionarnos el error y enviarnos una captura de pantalla con el comando\n\nError: \n```{str(exception)}```",
                              color=self.color).set_footer(
                                  text="Maubot help | Solo envia bugs a github si son importantes, Si es un error de argumentos pon $help [seccion]"
                              ))
            Logger.error(f'ERROR: {str(exception)}')
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(env.get("WEBHOOK_URL_ERRORES"), adapter = discord.AsyncWebhookAdapter(session))
                await webhook.send(content = f'<:lightno:774581319367655424> **Un error** ` {exception}')



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
                commands.ExtensionFailed) as e:
            message_error = 'Error al recargar cogs. {e}'
            Logger.error(message_error)
            await ctx.send(message_error)

            return

        message_success = 'Cogs recargados.'
        Logger.success(message_success)
        await ctx.send(message_success)





def eliminar_prefix(guild):
    with open(env.get("JSON_DIR") + 'prefix.json', 'r') as f:
        prefixes = json.load(f)
    
    del prefixes[str(guild.id)]

    with open(env.get("JSON_DIR") + 'prefix.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

class Maubot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Cambia el prefijo")
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def prefix(self, ctx, prefix):

        with open(env.get("JSON_DIR") + 'prefix.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open(env.get("JSON_DIR") + 'prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        e = discord.Embed(title="Se a cambiado el prefijo correctamente", description=f'Se a cambiado el prefijo a:      `{prefix}`', color=color)
        e.add_field(name="¡Tenemos un servidor!", value="**Unete a nuestro server  ->  (https://discord.gg/mwDBgubwdP)**")
        await ctx.send(embed=e)

    @commands.command(description="Mira la info del bot o la config ($_bot info | $_bot config)")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _bot(self, ctx, inf_con):
        if inf_con == 'info':
            em = discord.Embed(timestamp=datetime.datetime.utcnow(), colour=color)
            em.title = 'Info de Maubot'
            em.set_author(name=ctx.author.name, icon_url="https://img.icons8.com/plasticine/100/000000/bot.png")
            try:
                em.description = self.bot.psa + '\n[Soporta nuestro server](https://discord.gg/mwDBgubwdP)'
            except AttributeError:
                em.description = 'Un bot echo por [Maubg](https://www.youtube.com/channel/UCnNQ8-WPlcMqKpTdvAL8_HA). [¡Ùnete a que esperas!](https://discord.gg/mwDBgubwdP)'
            em.add_field(name="Servidores", value=f"> {len(self.bot.guilds)}")
            em.add_field(name="Usuarios online", value=f"> {str(len({m.id for m in self.bot.get_all_members() if m.status is not discord.Status.offline}))}")
            em.add_field(name='Usuarios totales', value=f"> {len(self.bot.users)}")
            em.add_field(name="Librerías", value=f"> discord.py")
            em.add_field(name="Tardanza de respuesta", value=f"> {self.bot.ws.latency * 1000:.0f} ms")        
            em.add_field(name="Color de maubot", value=f"> {color}")                 
            em.add_field(name="Creador de maubot", value=f"> Maubg ︻芫═───#2688")         
            em.add_field(name="id de maubot", value=f"> 730124969132163093")  
            em.add_field(name="discriminador", value=f"> #6247")    
            em.add_field(name="prefijo", value=f"> {ctx.prefix}") 
            em.add_field(name="descripcion", value=f"{self.bot.description}") 
            em.add_field(name="Invita al bot", value=f"> [Invita al bot](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)", inline=True)

            em.add_field(name="INFORMACÍON", value="```Maubot es un discord bot que puede ser utilizado para ajustar servidores, roles, diversíon, imagenes, informacíon, y mucho mas. El creador es (Maubg ︻芫═───#2688) por si quereis contactarlo.```", inline=False)
            em.set_footer(text="Maubot | Echo por Maubg")
            await ctx.send(embed=em) 

        if inf_con == 'config':
            em = discord.Embed(timestamp=self.datetime.datetime.utcnow(), colour=color)
            em.title = 'Configuracion de Maubot'
            em.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            try:
                em.description = self.bot.psa + '[Soporta nuestro server](https://discord.gg/mwDBgubwdP)'
                # CAMBIAR LINK AL TENER UN SERVER DE VERDAD
            except AttributeError:
                em.description = '[¡Unete a que esperas!](https://discord.gg/mwDBgubwdP)'
                # CAMBIAR LINK AL TENER UN SERVER DE VERDAD
            em.add_field(name="Prefix", value=f"Escribe este commando y luego el prefijo que quieras **ej: {ctx.prefix}prefix !**")
            em.add_field(name='rename_bot', value=f'Puedes usar este comando para ponerle in __nickname__ a Maubot.', inline=False)
            em.add_field(name='rate_bot <commentario>', value=f'Puedes darle un rating de 5 estrellas.', inline=False)


            em.set_footer(text="Maubot | Echo por Maubg")
            await ctx.send(embed=em) 


    @commands.command(aliases=['permisos_visu'], description="Mira los permisos de alguien")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def permisos(self, ctx, *, member: discord.Member=None):

        if not member:
            member = ctx.author



        perms = ',\n'.join(perm for perm, value in member.guild_permissions if value)
        trans = Translator()
        embed = discord.Embed(title=f'Los permisos de {member} son:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        translated_perms = trans.translate(perms, src="en", dest="es")
        embed.add_field(name='\uFEFF', value=translated_perms.text)

        await ctx.send(content=None, embed=embed)


    @commands.command(description="Mira la info de un usuario")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, ctx, member:discord.Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]

        embed = discord.Embed(colour=member.color, timestap=ctx.message.created_at)

        embed.set_author(name=f"informacion de  -  {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Propuesto por -- {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Nombre en el servidor", value=member.display_name, inline=False)

        embed.add_field(name="Creado en", value=member.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC"), inline=True)
        embed.add_field(name="Se a unido en", value=member.joined_at.strftime("%a %#d %B %Y, %I:%M %p UTC"), inline=True)

        if member.bot:
            embed.add_field(name="Bot?", value="Si", inline=True)
        else:
            embed.add_field(name="Bot?", value="No", inline=True)


        embed.add_field(name="Mejor rol", value=member.top_role.mention, inline=False)
        embed.add_field(name=f"Roles: ({len(roles)})", value=" ".join([role.mention for role in roles]), inline=False)


        await ctx.send(embed=embed)







    #fin de ayuda


    @commands.command(description="Hola 👏 Gente 👏 ¿Què 👏 Tal 👏 ?")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def palmadas(self, ctx, *, message):
        msg = message.replace(" ", " 👏 ")

        await ctx.send(msg)


    @commands.command(description="Mira el avatar de alguien")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        member = ctx.author if member == None else member
        embed = discord.Embed(title=f"**Avatar de -- ({member})**", description=f"[Link]({member.avatar_url})",colour=color)
        embed.set_image(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command(description="Mira el token del bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def token(self, ctx):
        embed = discord.Embed(title="".join([random.choice(list('abcdefghijklmnopqrstuvwxyz._=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.')) for i in range(59)]), colour=color)
        await ctx.send(embed=embed)

    @commands.command(asliases=['link', 'links'], description="Los links del bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def links(self, ctx):

        embed = discord.Embed(description=f"**Link para el bot:** [Mi link](https://discord.com/oauth2/authorize?client_id=730124969132163093&permissions=8&scope=bot)\n**Server**: (https://discord.gg/mwDBgubwdP)\n**Web**: [Link](http://maubot.mooo.com/)\n**Github**: [linky](https://github.com/maubg-debug/maubot)\n**Github del creador**: [link Github](https://github.com/maubg-debug/)", colour=color)
        embed.set_author(name="INVITACIONES", icon_url="https://img.icons8.com/color/48/000000/share.png")
        embed.set_image(url="https://top.gg/api/widget/730124969132163093svg?usernamecolor=FFFFFF&topcolor=000000")
        embed.set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-share-icon.png")
        # embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")
        await ctx.send(embed=embed)

    @commands.command(description="Invitacion")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):

        embed = discord.Embed(description=f"**https://discord.com/oauth2/authorize?client_id=730124969132163093&permissions=8&scope=bot**", colour=color)
        await ctx.send(embed=embed)

    @commands.command(description="¿Quien es el jefe del servidor?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def owner(self, ctx):

        embed = discord.Embed(title="👑 Owner del servidor", colour=color)
        embed.add_field(name=f"El owner de __{ctx.guild.name}__ es:", value=f"\n👑 **{ctx.guild.owner}**", inline=False)
        embed.set_thumbnail(url=f"{ctx.guild.owner.avatar_url}")
        embed.set_footer(text=f"Puesto por | {ctx.author}")
        embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['head'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def magicb(self, ctx, filetype):
        file = open('./src/utils/magic/magic.json').read()
        alldata = json.loads(file)
        try:
            messy_signs = str(alldata[filetype]['signs'])
            signs = messy_signs.split('[')[1].split(',')[0].split(']')[0].replace("'", '')
            filetype = alldata[filetype]['mime']
            await ctx.send(f'''{filetype}: {signs}''')
        except:
            await ctx.send(f"{filetype} no encontrado :( Si cree que este tipo de archivo debe incluirse, haga `> request \"magicb {filetype}\"`")


class Feedback(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Haz una reseña a el robot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rate_bot(self, ctx, *, texto):
        NUMBERS = {
            "1⃣": 0,
            "2⃣": 1,
            "3⃣": 2,
            "4⃣": 3,
            "5⃣": 4,
        }

        embed = discord.Embed(title="Califica al bot", colour=color)
        embed.add_field(name="Descripcion", value=f"`{texto}`")
        embed.set_footer(text=f"Propuesto por: {ctx.author.name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)

        def _check(reaction, user):
            return reaction.emoji in NUMBERS.keys() and reaction.message.id == msg.id and user == ctx.author

        embed_time_out = discord.Embed(title="SE ACABO EL TIEMPO", description="Intentalo otra vez pero esta vez no tardes 20 minutos", colour=color)

        embed_done = discord.Embed(title="Confirmando...", colour=color)
        embed_done.set_footer(text=f"Propuesto por: {ctx.author.name}", icon_url=ctx.author.avatar_url)


        for emoji in list(NUMBERS.keys()):
            await msg.add_reaction(emoji)

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=20, check=_check)
            embed_done.add_field(name="Gracias por tu calificacion, Puedes poner tu calificacion [aqui](https://bots.ondiscord.xyz/bots/730124969132163093/review)", value=f"estrellas: **{reaction.emoji}**\n\n**Descripcion:**\n{texto}\n **Si quieres te puedes unir a [nuestro server](https://discord.gg/mwDBgubwdP) para decirnos que tal tu experencia**")


        except asyncio.TimeoutError:
            await msg.clear_reactions()
            await msg.edit(embed=embed_time_out)

        else:
            await msg.clear_reactions()
            await msg.edit(embed=embed_done)    

            feedbackCh = self.bot.get_channel(777598645725167618)
            embed_feed_CH = discord.Embed(title=f"Nueva reseña", colour=color)
            embed_feed_CH.add_field(name="Calificacion:", value=f"estrellas: **{reaction.emoji}**\n\n**Descripcion:**\n{texto}")
            await feedbackCh.send('<@700812754855919667>, Usuario con ID: '+str(ctx.message.author.id)+f' Ha enviado una reseña', embed=embed_feed_CH)

    @commands.command()
    async def request(self, ctx: commands.Context, *, feature):
        creator = await self.bot.fetch_user(700812754855919667)
        authors_name = str(ctx.author)
        await creator.send(discord.Embed(title="Nueva propuesta", description=f':pencil: {authors_name}: {feature}', color=color))
        await ctx.send(discord.Embed(title="Gracias", description=f''':pencil: Gracias, Se ha solicitado tu idea!''', color=color))

    @commands.command()
    async def report(self, ctx: commands.Context, *, error_report):
        creator = await self.bot.fetch_user(700812754855919667)
        authors_name = str(ctx.author)
        await creator.send(embed=discord.Embed(title="Nuevo bug", description=f':triangular_flag_on_post: {authors_name}: {error_report}', color=color))
        await ctx.send(embed=discord.Embed(title="Gracias", description=f''':triangular_flag_on_post: Gracias por tu ayuda, ¡El error ha sido informado! Pero tambien lo puedes sugerir en [Github](https://github.com/maubg-debug/maubot/issues/new?assignees=&labels=bug&template=reporte-de-bugs.md&title=BUG)''', color=color))

def setup(app):
    app.add_cog(Maubot(app))
    app.add_cog(Feedback(app))
