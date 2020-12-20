import sys, json, asyncio

import discord

from discord import Activity
from discord.ext import commands

from utils.Environment import Environment, env
from utils.Logger.Logger import Logger
from cogs.Cogs import Cogs
from middleware import run_middleware_stack

from googletrans import Translator

import random
import datetime


from discord_logger import DiscordLogger

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
        self.__web__ = "https://maubot.maucode.com"

        self.__estado = "███████╗███████╗ ██╔════╝╚════██║ █████╗░░░░███╔═╝ ██╔══╝░░██╔══╝░░ ███████╗███████╗ ╚══════╝╚══════╝"

        self.__cogs = cogs
        self.color = int(env.get("COLOR"))

        self.help_url = "https://github.com/maubg-debug/maubot/issues/new?assignees=&labels=bug&template=reporte-de-bugs.md&title=BUG"

        try:
            self.__load_cogs()
        except (commands.ExtensionNotLoaded,
                commands.ExtensionNotFound,
                commands.NoEntryPointError,
                commands.ExtensionFailed) as e:
            Logger.error(f'Error cargando cogs: {e}')
            sys.exit(1)

        self.add_command(App.__reload_cogs)
        
        
        
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name=self.__estado), status=discord.Status.do_not_disturb)
        Logger.success(f"--------------------------------------------------------------------------------------------------\nInfo: \n1. Autor              | {self.__autor__}\n2. Github del creador | {self.__github__}\n3. Repo de maubot     | {self.__repo__}\n4. Version            | {self.__version__}\n5. Web                | {self.__web__}", separador=False)
        Logger.success(f'Maubot esta online como "{self.user}".', separador=True)

    async def on_message(self, message):
        await run_middleware_stack(message)
        await self.process_commands(message)


    async def reaction(self, context, msg_error, debug: bool = False):
        if not debug: msg_error.set_footer(text='\n-- ERROR')
        msg_error = await context.send(embed=msg_error)
        emojiR = ""
        if debug: emojiR = "🇽"
        else: emojiR = "❌"
        await msg_error.add_reaction(str(emojiR))
        def _check(reaction, user):
            return (
                reaction.emoji in str(emojiR)
                and user == context.author
                and reaction.message.id == msg_error.id
            )

        reaction, user = await self.wait_for("reaction_add", check=_check)
        await msg_error.delete()

    async def on_command_error(self, context, exception):
        env = Environment()

        exception_type = exception.__class__
        if exception_type:

            if isinstance(exception, commands.CommandOnCooldown):
                embed = discord.Embed(title="Tranquilo...", description=f"{context.author.mention} Este comando esta en reposo\n Ahora tienes que esperar **{exception.retry_after:,.2f}** segundos", color=self.color)
                return await context.send(embed=embed)

            elif isinstance(exception, commands.DisabledCommand):
                embed = discord.Embed(title="404", description=f"{context.author.mention} Este comando esta **desactivado** intentalo mas tarde", color=self.color)
                return await context.send(embed=embed)

            elif isinstance(exception, commands.NotOwner):
                embed = discord.Embed(title="....", description=f"{context.author.mention} Este comando es para mi creador\n\nVete y consigue una vida.", color=self.color)
                return await context.send(embed=embed)

            elif isinstance(exception, commands.TooManyArguments):
                embed = discord.Embed(description=f"{context.author.mention} Escribe menos argumentos por favor.", colour=0xf15069)
                embed.set_author(name="Demasiado", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                return await self.reaction(context, embed)

            elif isinstance(exception, commands.BadArgument):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** {context.prefix}help ** para mas informacion', colour=0xf15069)
                embed.set_author(name="Escribe un argumento valido", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                return await self.reaction(context, embed)

            elif isinstance(exception, commands.MissingRequiredArgument):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** "{context.prefix}help" ** para mas informacion', colour=0xf15069)
                embed.set_author(name="Escribe todos los argumentos requeridos", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                return await self.reaction(context, embed)


            elif isinstance(exception, commands.MissingPermissions):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** "{context.prefix}help" ** para mas informacion', colour=0xf15069)
                embed.set_author(name=f"Necesitas permisos para hacer esto", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                perms = Translator().translate(str([perm.replace('_', ' ').replace('guild', 'server').title() for perm in exception.missing_perms]), src='en', dest='es').text
                perms = perms.replace("'", '').replace('[', '').replace(']', '')
                embed.add_field(name="\uFEFF", value=f"Permisos necesarios: `{perms}`")
                return await self.reaction(context, embed)

            elif isinstance(exception, commands.MissingRole):
                embed = discord.Embed(description=f'> {context.author.mention} Puedes escribir ** {context.prefix}help ** para mas informacion', colour=0xf15069)
                embed.set_author(name="Tienes que tener los roles correctos", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
                return await self.reaction(context, embed)


        excepciones = ["'reaction' referenced before assignment", "Command raised an exception: TimeoutError:", "Unknown Message", "You do not own this bot", 'command is disabled', 'Command "cancelar" is not found', 'You are on cooldown.', "KeyError: 'run'", "Unknown Emoji", "AttributeError: 'NoneType' object has no attribute 'id'", "AttributeError: 'ClientUser' object has no attribute 'send'", "is not found"]

        if env.get('DEBUG'):
            if str(exception) == "": return 
            for i in excepciones: 
                if i in str(exception): return
            embed=discord.Embed(
                                title="Como sabes, los robots no son perfectos", 
                                description=f"Se ha producido un error, Visita: **[Nuestro github]({self.help_url})** p `m.report <error/bug>` \npara mencionarnos el error y enviarnos una captura de pantalla con el comando\n\n**Error:** \n```{str(exception)}```",
                                color=self.color).set_footer(
                                    text="Maubot help | Solo envia bugs a github si son importantes, Si es un error de argumentos pon m.help [seccion]"
                                )
            Logger.error(f'ERROR: {str(exception)}')
            embed2 = discord.Embed(title=f'<:lightno:774581319367655424>  Un error', color=14362664)
            embed2.add_field(name="Comando:", value="` " + str(context.invoked_with) + " `")
            embed2.add_field(name="Servidor:", value="` " + str(context.guild.name) + " `")
            embed2.add_field(name="Hora:", value="` " + str(datetime.datetime.utcnow()) + " `")
            embed2.add_field(name="Error:", value=f"```\n{exception}\n```", inline=False)

            webhook_url = env.get("WEBHOOK_URL_ERRORES")
            options = {
                "application_name": "Maubot | Errores",
                "service_name": "Error de comando",
                "service_environment": "Produccion",
                "default_level": "info",
            }

            logger = DiscordLogger(webhook_url=webhook_url, **options)
            logger.construct(
                title="Un error con Maubot",
                description=f"¡Un error en el comando `{context.invoked_with}`!",
                error=exception,
                metadata={"host": "maubot.maucode.com:5000"},
            )

            response = logger.send()
            await self.reaction(context, embed, True)
 

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
    @commands.has_permissions(manage_channels=True)
    async def prefix(self, ctx, prefix):
                                
        for i in "!,-,.,+,?,$,>,/,;,*,s!,=,m!,!!".split(","):
            if str(prefix) == str(i):
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention}, \nLos prefijos: `!, -, ., +, ?, $, >, /, ;, *, s!, =, m!, !!`\n no estan permitidos", color=color))

        with open(env.get("JSON_DIR") + 'prefix.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open(env.get("JSON_DIR") + 'prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        e = discord.Embed(title="Se a cambiado el prefijo correctamente", description=f'Se a cambiado el prefijo a:      `{prefix}`\nLos prefijos de este servidor son: `{prefix}`, `m.` `m-`', color=color)
        e.add_field(name="¡Tenemos un servidor!", value="**Unete a nuestro server  ->  (https://discord.gg/mwDBgubwdP)**")
        await ctx.send(embed=e)

    @commands.command(name="bot", usage="[info | config]", description="Mira la info del bot o la config (m._bot info | m._bot config)")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _bot(self, ctx, inf_con=None):
        inf_con = inf_con.lower()
        if inf_con == 'info':
            em = discord.Embed(timestamp=datetime.datetime.utcnow(), colour=color)
            em.title = 'Info de Maubot'
            em.set_author(name=ctx.author.name, icon_url="https://img.icons8.com/plasticine/100/000000/bot.png")
            try:
                em.description = self.bot.psa + '\n[Soporta nuestro server](https://discord.gg/mwDBgubwdP)'
            except AttributeError:
                em.description = 'Un bot echo por [Maubg](https://github.com/maubg-debug). [¡Ùnete a que esperas!](https://discord.gg/mwDBgubwdP)'
            em.add_field(name="Servidores", value=f"> {len(self.bot.guilds)}")
            em.add_field(name="Usuarios online", value=f"> {str(len({m.id for m in self.bot.get_all_members() if m.status is not discord.Status.offline}))}")
            em.add_field(name='Usuarios totales', value=f"> {len(self.bot.users)}")
            em.add_field(name="Librerías", value=f"> discord.py")
            em.add_field(name="Tardanza de respuesta", value=f"> {self.bot.ws.latency * 1000:.0f} ms")        
            em.add_field(name="Color de maubot", value=f"> {color}")       
            c = self.bot.get_user(700812754855919667)
            em.add_field(name="Creador de maubot", value=f"> {c.name}#{c.discriminator}")         
            em.add_field(name="id de maubot", value=f"> 730124969132163093")  
            em.add_field(name="discriminador", value=f"> #6247")    
            em.add_field(name="prefijo", value=f"> {ctx.prefix}") 
            em.add_field(name="descripcion", value=f"{self.bot.description}") 
            em.add_field(name="Invita al bot", value=f"> [Invita al bot](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)", inline=True)

            em.add_field(name="INFORMACÍON", value=f"```Maubot es un discord bot que puede ser utilizado para ajustar servidores, diversíon, imagenes, informacíon, y mucho mas. El creador es ({c.name}#{c.discriminator}) por si quereis contactarlo.```", inline=False)
            em.set_footer(text="Maubot | Echo por Maubg")
            await ctx.send(embed=em) 

        elif inf_con == 'config':
            em = discord.Embed(timestamp=datetime.datetime.utcnow(), colour=color)
            em.title = 'Configuracion de Maubot'
            em.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            try:
                em.description = self.bot.psa + '[Soporta nuestro server](https://discord.gg/mwDBgubwdP)'
            except AttributeError:
                em.description = '[¡Unete a que esperas!](https://discord.gg/mwDBgubwdP)'
            em.add_field(name="Prefijo", value=f"Escribe este commando y luego el prefijo que quieras **ej: {ctx.prefix}prefix <prefijo>**")
            em.add_field(name="Niveles", value=f"Se es para activar los niveles **ej: {ctx.prefix}levels**")
            em.add_field(name="Seguridad", value=f"Maubot eliminara links, spam, etc **ej: {ctx.prefix}seguridad**")


            em.set_footer(text="Maubot | Echo por Maubg")
            await ctx.send(embed=em) 
        else:
            await ctx.send(embed=discord.Embed(title="Escoje de estas opciones", description=f"- {ctx.prefix}bot info\n- {ctx.prefix}bot config", color=color))

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


    @commands.command(description="Hola 👏 Gente 👏 ¿Què 👏 Tal 👏 ?")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def palmadas(self, ctx, *, message):
        msg = message.replace(" ", " 👏 ")

        await ctx.send(embed=discord.Embed(color=color, description=msg))


    @commands.command(description="Mira el avatar de alguien")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member = None):
        member = ctx.author if member == None else member
        embed = discord.Embed(title=f"**Avatar de -- ({member})**", description=f"**[Link]({member.avatar_url_as(static_format='png')})**",colour=color)
        embed.set_image(url=f"{member.avatar_url_as(static_format='png')}")
        await ctx.send(embed=embed)

    @commands.command(description="Mira el token del bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def token(self, ctx):
        embed = discord.Embed(title="🔑 ¡Toma tu llave! <:bot:774580334259994625>", description="".join([random.choice(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')) for i in range(24)]) + "." + "".join([random.choice(list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')) for i in range(4)]) + "." + "".join([random.choice(list('-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')) for i in range(25)]), colour=color)
        await ctx.send(embed=embed)

    @commands.command(asliases=['link', 'links'], description="Los links del bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def links(self, ctx):

        embed = discord.Embed(description=f"**Link para el bot:** [Mi link](https://discord.com/oauth2/authorize?client_id=730124969132163093&permissions=8&scope=bot)\n**Server**: (https://discord.gg/mwDBgubwdP)\n**Web**: [Link](https://maubot.maucode.com/)\n**Github**: [linky](https://github.com/maubg-debug/maubot)\n**Github del creador**: [link Github](https://github.com/maubg-debug/)", colour=color)
        l = """
            -> **[top.gg](https://top.gg/bot/730124969132163093)**
            -> **[blist.xyz](https://blist.xyz/bot/730124969132163093/)**
            -> **[bots.ondiscord.xyz](https://bots.ondiscord.xyz/bots/730124969132163093/)**
            -> **[Discord.Bots.gg](https://discord.bots.gg/bots/730124969132163093)**
            -> **[discord.boats](https://discord.boats/bot/730124969132163093)**
            -> **[botlist.space](https://botlist.space/bot/730124969132163093)**
            -> **[botsdatabase](https://botsdatabase.com/bot/730124969132163093)**    
            -> **[arcane](https://arcane-center.xyz/bot/730124969132163093)**    
            -> **[Delly](https://discordextremelist.xyz/bots/730124969132163093)**    
            -> **[botsfordiscord](https://botsfordiscord.com/bot/730124969132163093)**
        """
        embed.add_field(name="Puedes verme en:", value=l)
        embed.set_author(name="INVITACIONES", icon_url="https://img.icons8.com/color/48/000000/share.png")
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
            embed_done.add_field(name="Gracias por tu calificacion", value=f"estrellas: **{reaction.emoji}**\n\n**Descripcion:**\n{texto}\n **Si quieres te puedes unir a [nuestro server](https://discord.gg/mwDBgubwdP) para decirnos que tal tu experencia**")


        except asyncio.TimeoutError:
            try:
                await msg.clear_reactions()
            except:
                pass    
            await msg.edit(embed=embed_time_out)

        else:
            try:
                await msg.clear_reactions()
            except:
                pass
            await msg.edit(embed=embed_done)    

            feedbackCh = self.bot.get_channel(777598645725167618)
            embed_feed_CH = discord.Embed(title=f"Nueva reseña", colour=color)
            s = ""
            for i in range(0, NUMBERS[reaction.emoji]):
                s += "⭐"
            s += "⭐"
            embed_feed_CH.add_field(name="Calificacion:", value=f"estrellas:  **{s} ({reaction.emoji})**\n\n**Descripcion:**\n{texto}")
            embed_feed_CH.set_footer(text="Puedes poner m.rp <id> <res> | para responder a la reseña")
            await feedbackCh.send('<@700812754855919667>, Usuario con ID: '+str(ctx.message.author.id)+f' Ha enviado una reseña', embed=embed_feed_CH)

    @commands.command()
    async def request(self, ctx: commands.Context, *, feature):
        creator = await self.bot.fetch_user(700812754855919667)
        authors_name = str(ctx.author)
        await creator.send(embed=discord.Embed(title="Nueva propuesta", description=f':pencil: {authors_name}: {feature}', color=color))
        await ctx.send(embed=discord.Embed(title="Gracias", description=f''':pencil: Gracias, Se ha solicitado tu idea!''', color=color))

    @commands.command()
    async def report(self, ctx: commands.Context, *, error_report):
        creator = await self.bot.fetch_user(700812754855919667)
        authors_name = str(ctx.author)
        await creator.send(embed=discord.Embed(title="Nuevo bug", description=f':triangular_flag_on_post: {authors_name}: {error_report}', color=color))
        await ctx.send(embed=discord.Embed(title="Gracias", description=f''':triangular_flag_on_post: Gracias por tu ayuda, ¡El error ha sido informado! Pero tambien lo puedes sugerir en [Github](https://github.com/maubg-debug/maubot/issues/new?assignees=&labels=bug&template=reporte-de-bugs.md&title=BUG)''', color=color))

def setup(app):
    app.add_cog(Maubot(app))
    app.add_cog(Feedback(app))
