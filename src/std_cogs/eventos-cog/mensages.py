import discord
from discord.ext import commands
import json
import time
from os import environ as env
import re
from termcolor import cprint

from utils.security.message import Seguridad

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


class Mensages(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot  

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        EsUnaInfraccion = await Seguridad(self.bot, message)

        if EsUnaInfraccion: return
        

        with open(env["JSON_DIR"] + "chats.json", "r") as f:
            chats = json.load(f)

        try:
            if not message.guild:
                if str(message.author.id) in chats["chats"]:
                    dest = chats["chats"][f"{message.author.id}"]["dest"]
                    # print(dest)
                    if str(dest) in chats["chats"]:
                        destid, dest = int(dest), self.bot.get_user(int(dest))
                        if len(message.attachments) > 0:
                            return await message.author.send(embed=discord.Embed(title="No se pueden los adjuntos", color=color, description=f"Las imagenes, tts, etc no estan permitidos en el chat de <@730124969132163093>"))
                        if EncontrarUrl(message.content):
                            await message.author.send(embed=discord.Embed(color=color, description="Se le ha enviado el link al usuario de forma como spoiler"))
                            msg = await dest.send(embed=discord.Embed(title="Un link", description=f"{message.author.mention} Se ha enviado un link, esta en modo spoiler por si acaso", color=color).add_field(name="Url:", value=f"||{EncontrarUrl(message.content)[0]}||"))
                            return
                        if message.content == "cerrarchat":
                            await cerrar(message.author, destid)
                            await message.author.send(embed=discord.Embed(title="El chat esta cerrado", description=f"{message.author.mention} se ha cerrado la conexion con **{dest.mention}**", color=color))
                            await dest.send(embed=discord.Embed(title="El chat esta cerrado", description=f"{dest.mention}, **{message.author.mention}** Ha cerrado la conexion con el chat.", color=color))
                            return
                        else: 
                            cprint(f"[Log] Mensage de ({message.author.name}) | ({dest.name}): {message.content}", "cyan")
                            return await dest.send(f"**{message.author.name}**`#{message.author.discriminator}`**:**  {message.content}")
                else:
                    return await message.author.send(embed=discord.Embed(title="No...", description=f"{message.author.mention} not puedes usar comandos dentro de los mensages de MD o hablar por aqui **(Solo puedes si estas en un chat con alguien m-help ChatApp)**", color=0xf15069))
        except Exception as e:
            return cprint(f"[Log] Un error en on_message: {e}", "red")

        with open(env["JSON_DIR"] + "chats.json", "w") as f:
            json.dump(chats, f)

        with open(env["JSON_DIR"] + "mute.json", 'r') as f:
            userm = json.load(f)

        # print(message.author.id)
        if str(message.author.id) in userm:
            try:
                return await message.delete()
            except discord.Forbidden:
                return

        if message.content == f"<@!{self.bot.user.id}>":
            await message.channel.send(embed=discord.Embed(title="Deja que me presente",
                                                           url="https://maubot.maucode.com", 
                                                           description="<:maubot:774967705831997501> Hola, mi nombre es Maubot. Si quieres conocer todos mis comandos, usa la ayuda de comandos, es bastante fácil usar todos mis comandos y dominarlos. Si quieres usar todos mis comandos, mis prefijos son (**<@!730124969132163093> prefijos**) Y para ver mis commandos solo pon **m.help**", 
                                                           colour=color).set_thumbnail(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-icon.png").add_field(name="Mis comandos", value="¿No saves que hacer? Puedes poner `m.help [Seccion]` y veras todos mis comandos disponibles. Si tienes cosas que decir siempre puedes poner `&rate_bot <Reseña>` y te responderemos **lo mas rapido** posible").add_field(name="¿Para que sirvo?", value="Mi dever en tu servidor es hacer que la gente se divierta con mis memes, que la gente le guste la musica y mi sistema de dinero, que el servidor sea bonito y **¡Mucho mas!**", inline=False))

        if message.content == f"<@!{self.bot.user.id}> prefijos":
                    await message.channel.send(embed=discord.Embed(title="Mis prefijos", 
                                                description="<:maubot:774967705831997501> Mis prefijos son `& (O custom m.prefix [prefijo])`, `m-`, `m.` - O tambien puedes poner <@!730124969132163093> ", 
                                                colour=color).set_image(url="https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/maubot-help-prefix.png"))


        with open(env["JSON_DIR"] + "userslvl.json", "r") as f:
            users = json.load(f)

        await self.update_data(users, message.author)
        await self.add_experience(users, message.author, 5)
        await self.level_up(self.bot, users, message.author, message.channel)

        with open(env["JSON_DIR"] + "userslvl.json", "w") as f:
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
        try:
            with open(env["JSON_DIR"] + "userslvl.json") as f:
                f = json.load(f)
            guilds = f["active"][str(channel.guild.id)]
        except:
            guilds = False

        if lvl_start < lvl_end:
            if guilds == True:
                await channel.send(embed=discord.Embed(title=f':tada: ¡felicidades!', description=f'{user.mention}, has subido al nivel {lvl_end}! :champagne_glass: ', colour=color).set_footer(text="Si quieres desactivarlo puedes poner m.levels para desactivarlo"))
                users[str(user.id)]['level'] = lvl_end

def setup(bot):
    bot.add_cog(Mensages(bot))