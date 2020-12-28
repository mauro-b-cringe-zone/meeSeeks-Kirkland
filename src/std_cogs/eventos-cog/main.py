import discord
from discord.ext import commands
import json
import time
from os import environ as env
from App import eliminar_prefix
import re
from termcolor import cprint
import aiohttp

async def cerrar(iniciador=None, destinatario:int=None):
    with open(env["JSON_DIR"] + "chats.json", "r") as f:
        chats = json.load(f)

    if str(iniciador.id) in chats["chats"]:
        del chats["chats"][f"{iniciador.id}"]
        del chats["chats"][f"{destinatario}"]

        with open(env["JSON_DIR"] + "chats.json", "w") as f:
            json.dump(chats, f)

def EncontrarUrl(string: str = None):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

color = int(env["COLOR"])

class Servidor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Cambia los si quieres recivir notificaciones de niveles")
    @commands.has_permissions(manage_channels=True)
    async def levels(self, ctx):
        with open(env["JSON_DIR"] + "userslvl.json", "r") as f:
            guilds = json.load(f)

        if not str(ctx.guild.id) in guilds["active"]:
            guilds["active"][str(ctx.guild.id)] = True
        else:
            guilds["active"][str(ctx.guild.id)] = not guilds["active"][str(ctx.guild.id)]

        await ctx.send(embed=discord.Embed(title=f"Se ha cambiado el sistema de los niveles a | {guilds['active'][str(ctx.guild.id)]}", color=color))

        with open(env["JSON_DIR"] + "userslvl.json", "w") as f:
            json.dump(guilds, f)

    @commands.command(description="Mira tu nivel de mensajes", usage="[usuario]")
    async def rank(self, ctx, user: discord.Member = None):
        with open(env["JSON_DIR"] + "userslvl.json", "r") as f:
            users = json.load(f)

        if not str(ctx.guild.id) in users["active"]:
            users["active"][str(ctx.guild.id)] = False
        if users["active"][str(ctx.guild.id)] is False:
            return await ctx.send(embed=discord.Embed(title="No se permiten los niveles", description=f"{ctx.author.mention} En este servidor no se admiten los niveles", color=color).set_footer(text="puedes poner m.levels para activarlo".capitalize()))

        if user is None:
            user = ctx.author

        experience = users[str(user.id)]["experience"]
        lvl_start = users[str(user.id)]["level"]
        lvl_end = int(experience ** (1/4))
        print(int(experience / lvl_end))
        
        # url = f'https://vacefron.nl/api/rankcard?username={user.name}&avatar={user.avatar_url}&level={users[str(user.id)]["level"]}&currentxp={experience - lvl_end}&rank=1&nextlevelxp={experience}&previouslevelxp={lvl_end}&custombg=https://cdn.discordapp.com/attachments/740416020761804821/741310178330148894/1596811604088.png&xpcolor=FFFFFF&isboosting=true'.replace(" ", "%20")

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
            webhook = discord.Webhook.from_url(env["WEBHOOK_URL_SALIDA"], adapter = discord.AsyncWebhookAdapter(session))
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
                return await guild.leave()

        bots = [member for member in guild.members if member.bot]

        try:
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(env["WEBHOOK_URL_ENTRADA"], adapter = discord.AsyncWebhookAdapter(session))
                await webhook.send(content = ':inbox_tray: **Añadido a un servidor** `' + guild.name.strip('`') + '` (`' + str(guild.id) + '`)\n  Total: **' + str(guild.member_count) + '** | Usuarios: **' + str(guild.member_count - len(bots)) + '** | Bots: **' + str(len(bots)) + '**' + '<:maubot:774967705831997501>')
        except:
            pass

        try:
            def check(event):
                return event.target.id == self.bot.user.id
            bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).find(check)
            msg_ent = await bot_entry.user.send(embed=discord.Embed(title="Holaaaaaa ", description=f"""<:maubot:774967705831997501> ¡Hola! Mi nombre es **{self.bot.user.name}**, Mi dever es hacer que tu servidor como tu se diviertan los mas posible
                Estoy seguro de que tu y yo seremos los mejores socios de la historia asique, gracias por invitarme a\n-> **{guild.name}**.

                **Los prefijos de los comandos son: `&`, `m.`, `m-`, `@mencion`** - `&` Es custom\n
                Esos son mis prefijos, siempre puedes hacerme menciones con **{self.bot.user.mention}**. 
                Si otro bot esta usando el mismo prefijo. `deves anikilarlo` es broma
                para cambiar de prefijo tienes que poner **m.prefix <nuevo prefijo>** (NO USES LOS BRACKETS).
                Para una lista de commando solo tienes que poner **m.help** y te saldran tooodos los comandos. 
                
                ¡Y se enviara un mensaje a mi desarroyador si pones `m.rate_bot <descripcion>`, `m.report <error>`, `m.request <cosa nueva>`! Cada uno de los comandos seran respectivos a los nombres
                {self.bot.user.name} ¿¡A que esperas!? (https://dsc.gg/maubot_servidor)
                
                Puedes verme en:
                -> **[top.gg](https://top.gg/bot/730124969132163093)**
                -> **[blist.xyz](https://blist.xyz/bot/730124969132163093/)**
                -> **[Discord.Bots.gg](https://discord.bots.gg/bots/730124969132163093)**
                -> **[discord.boats](https://discord.boats/bot/730124969132163093)**
                -> **[botlist.space](https://botlist.space/bot/730124969132163093)**
                -> **[botsdatabase](https://botsdatabase.com/bot/730124969132163093)**    
                -> **[arcane](https://arcane-center.xyz/bot/730124969132163093)**    
                -> **[Delly](https://discordextremelist.xyz/bots/730124969132163093)**    
                -> **[botsfordiscord](https://botsfordiscord.com/bot/730124969132163093)**
                -> **[infinitybots](https://infinitybots.xyz/730124969132163093)**


                -> **[Web de Maubot](https://maubot.maucode.com)**
                """, colour=color))
            await msg_ent.add_reaction("<:maubot:774967705831997501>")
        except: pass
    
        with open(env["JSON_DIR"] + 'prefix.json', 'r') as f:
            prefixes = json.load(f)
        
        prefixes[str(guild.id)] = '&'

        with open(env["JSON_DIR"] + 'prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        # Niveles
        with open(env["JSON_DIR"] + "userslvl.json", "r") as f:
            users = json.load(f)

        if not str(guild.id) in users["active"]:
            users["active"][str(guild.id)] = False

        with open(env["JSON_DIR"] + "userslvl.json", "w") as f:
            json.dump(users, f)

        channel = discord.utils.get(guild.text_channels)

        embed1 = discord.Embed(title="Maubot - el mejor bot de la historia", description="<:maubot:774967705831997501> Maubot es un bot para que tu puedas hacer cosas diversas en tu servidor.\n\nMaubot tiene muchas funciones como: divertirte, puedes cambiar el prefijo del bot (por si quieres) y **mas** cosas, muchas cosas mas. Si quieres saber mas tu solo pon `m.help` o con el prefijo que tu le ayas puesto.\n\n", colour=color)
        embed1.set_author(name='Maubot', icon_url="https://img.icons8.com/nolan/64/launched-rocket.png")
        embed1.add_field(name="¿Necesitas ayuda?", value=f"Puedes poner **m.help** para conseguir una lista de los comandos mas guays del mundo desde diversion hasta musica y economia. La lista de comandos estan separadas por secciones asi que podrias poner `m.help [seccion]` para descubrir mas comandos super chulos. o si no puedes poner **<@730124969132163093>** .", inline=True)
        embed1.add_field(name="Diversion atope", value=f"Maubot tiene muchos comando para divertirse con manipulacion de imagenes a juegos como el `conecta4`, `rps` y mucho mas. Maubot tambien tiene un sistema de economia muy avanzado para ser millonarios y dominar el mundo 🤤...", inline=True)
        embed1.add_field(name="Legal", value=f"Escribe `&copyright` para ver el copyright de Maubot.", inline=False)
        embed1.add_field(name="¿Aun no te has enterado?", value=f"Puedes ver un tutorial de como usar Maubot poniendo <@730124969132163093>", inline=False)
        embed1.set_footer(text="Maubot - Puedes escribir @Maubot para mas info")

        msg_h1 = await channel.send(content="Hola, gracias por meterme en este servidor. \nlos mensajes de abajo os explicaran algunas características sobre mi.\nSi alguien quiere apoyar mi servidor por favor dale a este link **(https://dsc.gg/maubot_servidor)**", embed=embed1)

def setup(bot):
    bot.add_cog(Servidor(bot))