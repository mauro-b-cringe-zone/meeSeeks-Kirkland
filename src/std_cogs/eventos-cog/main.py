import discord
from discord.ext import commands
import json
import time
from os import environ as env
import aiohttp
from App import eliminar_prefix
import asyncio
from termcolor import cprint

async def cerrar(iniciador=None, destinatario:int=None):
    with open("./src/json/chats.json", "r") as f:
        chats = json.load(f)

    if str(iniciador.id) in chats:
        del chats[f"{iniciador.id}"]
        del chats[f"{destinatario}"]

    with open("./src/json/chats.json", "w") as f:
        json.dump(chats, f)

color = int(env["COLOR"])

class Servidor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):


        with open("./src/json/chats.json", "r") as f:
            chats = json.load(f)

        try:
            if not message.guild:
                if message.author.id == 755433402299056139 or message.author.id == 730124969132163093:
                    return
                else:
                    if str(message.author.id) in chats:
                        dest = chats[f"{message.author.id}"]["dest"]
                        # print(dest)
                        if str(dest) in chats:
                            destid, dest = int(dest), self.bot.get_user(int(dest))
                            if message.content == "cerrarchat":
                                await message.author.send(embed=discord.Embed(title="El chat esta cerrado", description=f"{message.author.mention} se ha cerrado la conexion con **{dest.mention}**", color=0xc01fe0))
                                await dest.send(embed=discord.Embed(title="El chat esta cerrado", description=f"{dest.mention}, **{message.author.mention}** Ha cerrado la conexion con el chat.", color=0xc01fe0))
                                return await cerrar(message.author, destid)
                            else: 
                                cprint(f"[Log] Mensage de ({message.author.name}) | ({dest.name}): {message.content}", "cyan")
                                return await dest.send(f"**{message.author.name}:** {message.content}")
                    else:
                        return await message.author.send(embed=discord.Embed(title="No...", description=f"{message.author.mention} not puedes usar comandos dentro de los mensages de MD o hablar por aqui **(Solo puedes si estas en un chat con alguien $help ChatApp)**", color=0xf15069))
        except Exception as e:
            return cprint(f"[Log] Un error en on_message: {e}", "red")

        with open("./src/json/chats.json", "w") as f:
            json.dump(chats, f)

        with open("./src/json/mute.json", 'r') as f:
            user = json.load(f)

        # print(message.author.id)
        if str(message.author.id) in user:
            await message.delete()

        if message.content == "<@!730124969132163093>":
            # file = discord.File("assets/Maubot_tutorial.gif", filename="Maubot_tutorial.gif")
            await message.channel.send(embed=discord.Embed(title="Deja que me presente", 
                                                           description="Hola, mi nombre es Maubot. Si quieres conocer todos mis comandos, usa la ayuda de comandos, es bastante fácil usar todos mis comandos y dominarlos. Si quieres usar todos mis comandos, mis prefijos son (**<@!730124969132163093> prefijos**) Y para ver mis commandos solo pon **$help**", 
                                                           colour=color).set_image(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help.png").add_field(name="Mis comandos", value="¿No saves que hacer? Puedes poner `$help [Seccion]` y veras todos mis comandos disponibles. Si tienes cosas que decir siempre puedes poner `$rate_bot <Reseña>` y te responderemos **lo mas rapido** posible").add_field(name="¿Para que sirvo?", value="Mi dever en tu servidor es hacer que la gente se divierta con mis memes, que la gente le guste la musica y mi sistema de dinero, que el servidor sea bonito y **¡Mucho mas!**"))
                        
        if message.content == "<@!730124969132163093> prefijos":
                    # file = discord.File("assets/Maubot_tutorial.gif", filename="Maubot_tutorial.gif")
                    await message.channel.send(embed=discord.Embed(title="Mis prefijos", 
                                                description="Mis prefijos son `$ (O custom $prefix [prefijo])`, `!`, `?`, `m.` - O tambien puedes poner <@!730124969132163093> ", 
                                                colour=color).set_image(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-prefix.png"))


        with open("./src/json/userslvl.json", "r") as f:
            users = json.load(f)

        await self.update_data(users, message.author)
        await self.add_experience(users, message.author, 5)
        await self.level_up(self.bot, users, message.author, message.channel)

        with open("./src/json/userslvl.json", "w") as f:
            json.dump(users, f)
        # await self.bot.process_commands(message)

    async def update_data(self, users, user):
        if not str(user.id) in users:
            users[str(user.id)] = {}
            users[str(user.id)]["experience"] = 0
            users[str(user.id)]["level"] = 1
            users[str(user.id)]["last_message"] = 0

    async def add_experience(self, users, user, exp):
        users[str(user.id)]["experience"] += exp
        users[str(user.id)]["last_message"] = time.time()

    async def level_up(self, bot, users, user, channel):
        experience = users[str(user.id)]["experience"]
        lvl_start = users[str(user.id)]["level"]
        lvl_end = int(experience ** (1/4))

        if lvl_start < lvl_end and not user.id == 730124969132163093 and not user.id == 755433402299056139:
            await channel.send(embed=discord.Embed(title=f':tada: ¡felicidades!', description=f'{user.mention}, has subido al nivel {lvl_end}! :champagne_glass: ', colour=color))
            users[str(user.id)]['level'] = lvl_end

    @commands.command(description="Mira tu nivel de mensajes", usage="[usuario]")
    async def rank(self, ctx, user: discord.Member = None):
        with open("./src/json/userslvl.json", "r") as f:
            users = json.load(f)

        if user is None:
            user = ctx.author

        experience = users[str(user.id)]["experience"]
        lvl_end = int(experience ** (1/4))
        
        if not str(user.id) in users:
            await ctx.send(f"El usuario {user} aun no tiene un rango.")
        else:
            embed = discord.Embed(colour=color)
            embed.set_author(name=f"nivel - {user.name}", icon_url=user.avatar_url)
            embed.add_field(name="nivel", value=users[str(user.id)]["level"], inline=True)
            embed.add_field(name="exp", value=users[str(user.id)]["experience"], inline=True)
            await ctx.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        eliminar_prefix(guild)
        bots = [member for member in guild.members if member.bot]
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(env["WEBHOOK_URL"], adapter = discord.AsyncWebhookAdapter(session))
            await webhook.send(content = ':outbox_tray: **Quitado de un servidor** `' + guild.name.strip('`') + '` (`' + str(guild.id) + '`)\n  Total: **' + str(guild.member_count) + '** | Usuarios: **' + str(guild.member_count - len(bots)) + '** | Bots: **' + str(len(bots)) + '**')

    @commands.Cog.listener()
    async def on_ready(self):
    	for guild in self.bot.guilds:
    		if guild.member_count > 20:
    			bots = [member for member in guild.members if member.bot]
    			result = (len(bots) / guild.member_count) * 100
    			if result > 70.0:
    				await guild.leave()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.member_count > 20:
            bots = [member for member in member.guild.members if member.bot]
            result = (len(bots) / member.guild.member_count) * 100
            if result > 70.0:
                await member.guild.leave()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
    	if member.guild.member_count > 20:
    		bots = [member for member in member.guild.members if member.bot]
    		result = (len(bots) / member.guild.member_count) * 100
    		if result > 70.0:
    			await member.guild.leave()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        if guild.member_count > 20:
            bots = [member for member in guild.members if member.bot]
            result = (len(bots) / guild.member_count) * 100
            if result > 70.0:
                await guild.leave()

        bots = [member for member in guild.members if member.bot]
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(env["WEBHOOK_URL"], adapter = discord.AsyncWebhookAdapter(session))
            await webhook.send(content = ':inbox_tray: **Añadido a un servidor** `' + guild.name.strip('`') + '` (`' + str(guild.id) + '`)\n  Total: **' + str(guild.member_count) + '** | Usuarios: **' + str(guild.member_count - len(bots)) + '** | Bots: **' + str(len(bots)) + '**')


        def check(event):
            return event.target.id == self.bot.user.id
        bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).find(check)
        msg_ent = await bot_entry.user.send(embed=discord.Embed(title="Holaaaaaa", description=f""":tada: ¡¡¡Hola!!!Mi nombre e **{self.bot.user.name}**, Y soy el responsable que te ayudara 
            a ganar partidas en el destini `hacer tu server mejor` porque tu eres 
            uno de los mejores socios que voy a tener, asique, gracias por invitarme a **{guild.name}**.\n\n
            **El prefijo del comando es: `$`, `!`, `?`, `m.`**\n\n
            Ese es mi prefijo, siempre puedes hacerme menciones con **@{self.bot.user.name}**. 
            Si otro bot esta usando el mismo prefijo. `deves anikilarlo` es broma
            para cambiar de prefijo tienes que poner **$server** y luego **$prefix <nuevo prefijo>** (NO USES LOS BRACKETS).\n\n
            Para una lista de commando solo tienes que poner $help y te saldran tooodos los comandos. 
            \n\n
            y se enviara un mensaje a mi desarroyador! por si quieres poner una nueva cosa nueva en el bot, o poner un bug, 
            mantente actualizado con las nuevas funciones, o si solo quieres mas ayuda, mira el server oficial de 
            {self.bot.user.name} ¿¡A que esperas!? ( https://discord.gg/4gfUZtB )""", colour=color))

    
        with open('./src/json/prefix.json', 'r') as f:
            prefixes = json.load(f)
        
        prefixes[str(guild.id)] = '$'

        with open('./src/json/prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        channel = discord.utils.get(guild.text_channels)

        embed1 = discord.Embed(title="Maubot - el mejor bot de la historia", description="Maubot es un bot para que tu puedas hacer cosas diversas en tu servidor.\n\nMaubot tiene muchas funciones como: divertirte, puedes cambiar el prefijo del bot (por si quieres) y al igual ponerle un **__nickname__** , muchas cosas mas. Si quieres saber mas tu solo pon `$help` o con el prefijo que tu le ayas puesto.\n\n **ESCRIVE $verify PARA VERIFICAR QUE ERES HUMANO**", colour=color)
        embed1.set_author(name='Maubot', icon_url="https://img.icons8.com/nolan/64/launched-rocket.png")
        embed1.add_field(name="¿Necesitas ayuda?", value=f"Puedes poner **$help** para conseguir una lista de los comandos mas guays del mundo desde diversion hasta musica y economia. La lista de comandos estan separadas por secciones asi que podrias poner `$help [seccion]` para descubrir mas comandos super chulos. o si no puedes poner **<@730124969132163093>** .", inline=True)
        embed1.add_field(name="Diversion atope", value=f"Maubot tiene muchos comando para divertirse con manipulacion de imagenes a juegos como el `conecta4`, `rps` y mucho mas. Maubot tambien tiene un sistema de economia muy avanzado para ser millonarios y dominar el mundo 🤤...", inline=True)
        embed1.add_field(name="Legal", value=f"Escribe `$copyright` para ver el copyright de Maubot y tambien escribe `$verify` para erificar que eres humano", inline=False)
        embed1.add_field(name="¿Aun no te has enterado?", value=f"Puedes ver un tutorial de como usar Maubot poniendo <@730124969132163093>", inline=False)
        embed1.set_footer(text="Maubot - Puedes escribir @Maubot para mas info")


        msg_h1 = await channel.send(content="Hola, gracias por meterme en este servidor. \nlos mensajes de abajo os explicaran algunas características sobre mi.\nSi alguien quiere apoyar mi servidor por favor dale a este link **(https://discord.gg/4gfUZtB)**", embed=embed1)


    @commands.command(description="Verifica que eres humano")
    async def verify(self, ctx):
        embed5 = discord.Embed(title="Verifica que eres humano", description="En estos tiempos Discord cadavez tiene mas atackes de bots por lo que para mas seguridad verificar que no soy robots. \n\n porfavor dale al ✅ para comfirmar que no eres un robot", colour=0x1cce52)
        embed5.set_footer(text='Maubot | Verifica que eres humano')
        
        embed = discord.Embed(title="Bien eres humano", description="Ya puedes comenzar a usar el bot... pero cuidado. ajajaja solo bromeaba disfruta", colour=color)
        embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")


        msg = await ctx.send(embed=embed5)
        await msg.add_reaction('✅')
        guild = self.bot.get_guild(ctx.guild.id)
        def _check(reaction, user):
            return (
                reaction.emoji in '✅'
                and user == ctx.author
                and reaction.message.id == msg.id
            )
        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=600, check=_check)
        except asyncio.TimeoutError:
            await self.bot.leave_guild(guild)
        else:
            await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Servidor(bot))
