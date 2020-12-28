import discord
import asyncio
import random
import time
import datetime
import json
import aiohttp
import requests
from termcolor import cprint
import wikipediaapi
from discord.ext import commands
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group
from discord.utils import escape_markdown
import colorsys
import logging
from PIL import Image, ImageFont, ImageDraw, GifImagePlugin, ImageOps, ImageFilter
from requests import get
import pprint
import textwrap
import itertools
from collections import Counter, defaultdict
from string import Template
from typing import Any, Mapping, Optional, Union
import io
from io import BytesIO
from datetime import date, datetime
import logging
from random import choice
from bs4 import BeautifulSoup
import urllib
from collections import Counter
from googletrans import Translator, LANGUAGES

from os import environ as env
import re

color = int(env["COLOR"])
gtr = Translator()

def getSecrets():
    arr = [
        ' está durmiendo.',
        ' está respirando.',
        ' está a punto de || hacer algo. ||',
        ' le gustas.',
        ' te odia.',
        ' quería confesar algo.',
        ' es el tipo detrás de HowToBasic.',
        ' es la persona que dirige secretamente el gobierno de EE. UU.',
        ' es jeff el asesino.',
        ' es el responsable del desarrollo de Username601.',
        ' está pirateando el servidor.',
        ' está pirateando discord.',
        ' es genial.',
        ' es astuto',
        ' es el chico detrás de ti.',
        ' es un nerd.',
        ' le gustan las escuelas.',
        ' es el tipo que está espiando detrás de ti',
        ' tiene un canal secreto de youtube.',
        ' es un programador genial.',
        ' es un buen tipo, ¡aunque no vale la pena contar secretos!',
        ' es un usuario de discordia: v',
        ' está respirando.',
        ' umm ... tal vez no debería contar sus secretos.',
        ' es secretamente un bot. sí, selfbot. ',
        ' is ... umm .. :flushed:',
        ' es el hacker que gobernará el mundo']
    return arr

def EncontrarUrl(string: str = None):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Un url-shortener en maubot")
    @commands.cooldown(1, 5, commands.BucketType.user)       
    async def url(self, ctx: commands.Context, *, url: str):
        url = EncontrarUrl(url)[0]
        codigo = requests.get(f"https://maubot.maucode.com/api/redir/crear?url={url}").json()
        await ctx.send(embed=discord.Embed(color=color, title=f"Se te ha creado una url | {codigo['codigo']}", description=f"Puedes visitarlo dandole al link \n-> **https://maubot.maucode.com/api/redir?codigo={codigo['codigo']}**"))

    @commands.command(description="Mira la tardanza de respuesta")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        msg = await ctx.send("`Tardanza del bot...`")
        times = []
        counter = 0
        embed = discord.Embed(title="Mas informacion:", description="Se a hecho 4 pings y aqui estan los resultados:", colour=color)
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"provando ping... {counter}/3")
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            if speed < 160:
                embed.add_field(name=f"Ping {counter}:", value=f"🟢 | {speed}ms", inline=True)
                cprint(f"[Log] Ping: {speed}ms en el sevidor | {ctx.guild.name}", "green")
            elif speed > 170:
                embed.add_field(name=f"Ping {counter}:", value=f"🟡 | {speed}ms", inline=True)
                cprint(f"[Log] Ping: {speed}ms en el sevidor | {ctx.guild.name}", "yellow")
            else:
                embed.add_field(name=f"Ping {counter}:", value=f"🔴 | {speed}ms", inline=True)
                cprint(f"[Log] Ping: {speed}ms en el sevidor | {ctx.guild.name}", "red")


        embed.set_author(name="🏓    **PONG**    🏓", icon_url="https://img.icons8.com/ultraviolet/40/000000/table-tennis.png")
        embed.add_field(name="Tardanza del bot", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Velocidad normal", value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
        embed.set_footer(text=f"Tiempo total estimado transcurrido: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**", embed=embed)

    @commands.command(aliases='useless,uselesssites,uselessweb,uselesswebsites,uselesswebsite'.split(","), description="https://maubot.maucode.com/")
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def uselesswebs(self, ctx):
        try:
            url = requests.get('https://useless-api.vierofernando.repl.co/uselesssites').json()["url"]
            await ctx.send(embed=discord.Embed(title="Web inutil", description=f'**{url}**', color=color))
        except:
            await ctx.send(f'Ups. hay algún error, mientras tanto mira este sitio inútil: <https://top.gg/bot/730124969132163093/vote>')

    @staticmethod
    def get_channel_type_counts(guild: Guild):
        channel_counter = Counter(c.type for c in guild.channels)
        channel_type_list = []
        for channel, count in channel_counter.items():
            channel_type = str(channel).title()
            channel_type_list.append(f"{channel_type} channels: {count}")

        channel_type_list = sorted(channel_type_list)
        return "\n".join(channel_type_list)

    @commands.command(description="Mira la info del servidor")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def infoserver(self, ctx):

        created = ctx.guild.created_at
        features = ", ".join(ctx.guild.features)
        if features == "":
            features = "__NO__ hay caracteristicas en este servidor"
        region = ctx.guild.region
        if region == "europe":
            region = "europa"

        roles = len(ctx.guild.roles)
        member_count = ctx.guild.member_count
        channel_counts = self.get_channel_type_counts(ctx.guild)

        statuses = Counter(member.status for member in ctx.guild.members)

        embed = discord.Embed(title=f"Informacion del servidor __{ctx.guild.name}__", description=f"**ID:** {ctx.guild.id}\n**Creado:** {created}\n**Creador:** {ctx.guild.owner}\n**Region**: {region}\n**Caracteristicas:** {features}\n\n**Contador de miembros**\nMiembros: **{len(ctx.guild.members)}**\nHumanos: **{len(list(filter(lambda m: not m.bot, ctx.guild.members)))}**\nBots: **{len(list(filter(lambda m: m.bot, ctx.guild.members)))}**\n\n**Estados de los miembros**\n<:online:774982837354496021> {statuses[Status.online]:,}  <:idle:774983296533790730> {statuses[Status.idle]:,}  <:dnd:774983232541163541> {statuses[Status.dnd]:,}  <:offline:774982964592640030> {statuses[Status.offline]:,}\n\n**Canales:**\nCanales de texto: **{len(ctx.guild.text_channels)}**\nCanales de voz: **{len(ctx.guild.voice_channels)}**\nCategorias: **{len(ctx.guild.categories)}**\n\n**Mas info:**\nRoles: **{len(ctx.guild.roles)}**\nInvitaciones: **{len(await ctx.guild.invites())}**\n\nUnete al mio **( https://dsc.gg/maubot_servidor )**\nInvitame a otro servidor **( [Link para el bot](https://dsc.gg/maubot) )**", colour=color)

        embed.set_thumbnail(url=ctx.guild.icon_url)
        # embed.set_footer(text=f"Propuesto por {ctx.author.name}", icon_url=ctx.author.icon_url)
        await ctx.send(embed=embed)

    @commands.command(description="¿Ha cuantos has invitado?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invites(self, ctx):
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == ctx.author:
                totalInvites += i.uses
        embed = discord.Embed(title="Invitaciones", description=f"{ctx.author.mention} has invitado a **{totalInvites}** persona{'' if totalInvites == 1 else 's'}", colour=color)        
        await ctx.send(embed=embed)

    @commands.command(description="¿Una cerbeza?", usage="[usuario] [razon]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.mention}**: fieeeeestaaa!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*Veve una cerbeza con tigo* 🍻")
        if user.bot:
            return await ctx.send(f"Me encantaria dar una cerbeza al bot **{ctx.author.mention}**, pero no se si te respondera :/")

        beer_offer = f"**{user.mention}**, Tienes una 🍺 ofrecida de **{ctx.author.mention}**"
        beer_offer = beer_offer + f"\n\n**Razon:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=10.0, check=reaction_check)
            await msg.edit(content=f"**{user.mention}** y **{ctx.author.mention}** Estan veviendo una encantadora 🍻")
            try:
                await msg.clear_reactions()
            except: pass
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"bueno, parece que **{user.name}** no queria una cerbeza con **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            beer_offer = f"**{user.name}**, tienes una 🍺 de **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**razon:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=['guapocal', 'guapocl'], description="¿Eres guapo? Nah", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def guapo(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = ""
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"
        if hot < 25:
            emoji = "💔"

        await ctx.send(f"**{user.name}** es **{hot:.2f}%** guapo {emoji}")

    @commands.command(description="Desaparece del server (SE TE EXPULSA)")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vanish(self, ctx):
        await ctx.message.add_reaction('✅')
        time.sleep(0.5)
        await ctx.author.kick(reason='Su-propio-kick')

    @commands.command(name='djenerate', description="¿Puedes tocar esta pieza?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def generateDjent(self, ctx):
        import random

        oneString = ""
        for _ in range(0, 14):
            randomNum = random.randint(1, 100)

            if randomNum <= 65:
                oneString = oneString + "0\t—\t"
            if randomNum > 65 and randomNum <= 85:
                oneString = oneString + "1\t—\t"
            if randomNum > 85 and randomNum <= 95:
                oneString = oneString + "X\t—\t"

            if randomNum >= 95:
                randomFret = random.randint(2, 24)
                if oneString:
                    if oneString[-4] == "1":
                        oneString = oneString + "0\t—\t"
                        oneString = oneString + f"{randomFret}\t—\t"
                    else:
                        oneString = oneString + f"{randomFret}\t—\t"
                else:
                    oneString = oneString + f"{randomFret}\t—\t"

        oneString = oneString[:-3]

        emptyString = ("—\t" * 24) + "\n"
        output = ""
        randomString = random.randint(1, 100)

        if randomString <= 90:
            for _ in range(0, 5):
                output = output + emptyString
            output = output + oneString

        if randomString > 90:
            for _ in range(0, 4):
                output = output + emptyString
            output = output + oneString
            output = output + f"\n{emptyString}"

        bpm = random.randint(80, 200)
        randomTuning = random.choice(["Drop D","Drop C#","Drop B","Drop A#","Drop F","Drop F#","Drop G"])

        embed = discord.Embed(title=f"Tu tab aleatoria de Djent", color=color)
        embed.set_thumbnail(url="https://cdn.playlists.net/images/playlists/image/medium/82282.jpg")
        embed.add_field(name=f"{bpm}bpm, {randomTuning}", value=output, inline=True)
        await ctx.send(embed=embed)

    @commands.command(description="Traduze a el idioma que quieras (Ej: m.translate es helllo (m.translate --lista para ver los idiomas disponibles))", usage="<lang><texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def translate(self, ctx, *args):
        wait = await ctx.send(' | Porfavor espera...') ; args = list(args)
        if len(args)>0:
            if args[0]=='--lista':
                lang = ''
                for bahasa in LANGUAGES:
                    lang = lang+str(bahasa)+' ('+str(LANGUAGES[bahasa])+')\n'
                embed = discord.Embed(title='Lista de idiomas admitidos', description=str(lang), colour=color)
                await wait.edit(content='', embed=embed)
            elif len(args)>1:
                destination = args[0]
                toTrans = ' '.join(args[1:len(args)])
                try:
                    translation = gtr.translate(toTrans, dest=destination)
                except: return await ctx.send("Porfavor pon `m.translate --lista` para ver todos los idiomas")
                embed = discord.Embed(description=translation.text, colour=color)
                embed.set_footer(text=f'Traducido {LANGUAGES[translation.src]} al {LANGUAGES[translation.dest]}.')
                await wait.edit(content='', embed=embed)
            else:
                await wait.edit(content=f'¡Agregue un idioma! Para tener la lista y su identificación, escriba \n` {ctx.prefix}translate --lista`.')
        else:
            await wait.edit(content=f'Agregue traducciones o \nEscriba `{ctx.prefix}translate --lista` para los idiomas admitidos.')
    

	# @commands.command(aliases=['w', 'wa'])
	# @commands.cooldown(rate=3, per=10.0, type=commands.BucketType.user)
	# @commands.bot_has_permissions(embed_links=True)
	# async def wolfram(self, ctx, *, query):

	# 	if WOLFRAM_KEY is None:
	# 		raise commands.CommandError('The host has not set up an API key.')

	# 	params = {
	# 		'appid': WOLFRAM_KEY,
	# 		'i': query
	# 	}

	# 	async with ctx.channel.typing():
	# 		try:
	# 			async with ctx.http.get('https://api.wolframalpha.com/v1/result', params=params) as resp:
	# 				if resp.status != 200:
	# 					raise QUERY_ERROR

	# 				res = await resp.text()
	# 		except asyncio.TimeoutError:
	# 			raise QUERY_ERROR

	# 	query = query.replace('`', '\u200b`')

	# 	embed = discord.Embed()

	# 	embed.add_field(name='Query', value=f'```{query}```')
	# 	embed.add_field(name='Result', value=f'```{res}```', inline=False)

	# 	embed.set_author(name='Wolfram Alpha', icon_url='https://i.imgur.com/KFppH69.png')
	# 	embed.set_footer(text='wolframalpha.com')

	# 	if len(query) + len(res) > 1200:
	# 		raise commands.CommandError('Wolfram response too long.')

	# 	await ctx.send(embed=embed)

    @commands.command(description="Historias de mi dia a dia")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fml(self, ctx):
        async with ctx.channel.typing():
            response = requests.get('https://api.alexflipnote.dev/fml', headers={"Authorization": env["API_FLEX"]})
            json_data = json.loads(response.text)
            trans = Translator()
            translated_response = trans.translate(json_data['text'], src='en', dest='es')
            await ctx.send(translated_response.text)
 

    @commands.command(aliases=["cpr", "copy"], description="NO COPIES")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def copyright(self, ctx):
        embed = discord.Embed(colour=color)
        embed.set_author(name="Copyright", icon_url="https://img.icons8.com/color/48/000000/creative-commons--v1.png")
        embed.description = "> Maubot esta bajo la licencia de [GNU](https://github.com/maubg-debug/maubot/blob/main/LICENSE.md)"

        await ctx.send(embed=embed)


    @commands.command(aliases=["ltr", "letra", "repetida"], description="Mira haver si hay una letra repetida en tu texto", usage="<palabra>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def letra_repetida(self, ctx, palabra):
        embed = discord.Embed(title=f"Nada encontrado", description=f"Inserta una palabra con letras repetidas",colour=color)
        try:
            longituz_palabra = Counter(palabra)

            for m, v in longituz_palabra.items():
                if v > 1:
                    embed = discord.Embed(title=f"Encontrado", description=f"La **{m}** esta **{v}** veces en **{palabra}**",colour=color)
        except:
            pass
        await ctx.send(embed=embed)


    @commands.command(aliases=["edit", "editar"], description="Pon | Donde quieras que este la marca de (editado)", usage="<texto> <Pon una \"|\" donde quieras que este el \"editado\">")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def edited(self, ctx, *args):
        msg = await ctx.send('...')
        if len(list(args))==0 or '|' not in ' '.join(list(args)):
            return await msg.edit(content='Porfavor usa | Donde quieras que el \u202b valla.')
        if "@everyone" in ' '.join(list(args)) or '@here' in ' '.join(list(args)): 
            return await msg.edit("No puede mencionar a todos | Lol")
        await msg.edit(content=' '.join(list(args)).replace('|', '\u202b')+' \u202b')

    def urlify(self, word):
        from urllib.parse import quote_plus as urlencode
        return urlencode(word).replace('+', '%20')
    def api(self, url):
        return get(url).json()
    def dearray(self, arr):
        return str(', '.join(arr))+'.'

    @commands.command(description="Cuantas palabras riman con \"Palabra\"", usage="<Palabra>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rhyme(self, ctx, *args):
        if len(list(args))==0: await ctx.send('Por favor ingrese una palabra. E intentaremos encontrar la palabra que mejor rime con ella.')
        else:
            wait, words = await ctx.send(' | Espere... Buscando...'), []
            data = self.api('https://rhymebrain.com/talk?function=getRhymes&word='+str(self.urlify(' '.join(list(args)))))
            if len(data)<1: 
                await wait.edit(content='No encontramos ninguna palabra que rime correspondiente a esa letra.')
            else:
                for i in range(0, len(data)):
                    if data[i]['flags']=='bc': words.append(data[i]['word'])
                words = self.dearray(words)
                if len(words)>1950:
                    words = self.limitify(words)
                embed = discord.Embed(title='Palabras que riman con '+str(' '.join(list(args)))+':', description=words, colour=color)
                await wait.edit(content='', embed=embed)


    def jsonisp(self, url):
        from requests import get as decodeurl
        return decodeurl(url).json()

    @commands.command(description="Te dare la rezeta de lo que quieras", usage="<comida>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def receta(self, ctx, *args):

        trans = Translator()

        if len(list(args))==0:
            await ctx.send(embed=discord.Embed(title='Aquí tienes una receta para no cocinar nada:', description='1. No haga nada', color=color))
        else:
            data = self.jsonisp("http://www.recipepuppy.com/api/?q={}".format(self.urlify(' '.join(list(args)))))
            if len(data['results'])==0: 
                await ctx.send(" | No encontré nada.")
            elif len([i for i in data['results'] if i['thumbnail']!=''])==0:
                await ctx.send(" | No encontré nada con una imagen deliciosa..")
            else:
                

                total = random.choice([i for i in data['results'] if i['thumbnail']!=''])

                translated_title = gtr.translate(total['title'], src='en', dest='es')
                translated_ingredients = gtr.translate(total['ingredients'], src='en', dest='es')


                embed = discord.Embed(title=translated_title.text, url=total['href'], description='Ingredientes:\n{}'.format(translated_ingredients.text), colour=color)
                embed.set_image(url=total['thumbnail'])
                await ctx.send(embed=embed)

    @commands.command(description="Mira si una web esta abajo", usage="<website>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def isitdown(self, ctx, *args):
        from datetime import datetime as t
        from requests import post, get
        if len(list(args))==0: 
            return await ctx.send(' | Porfavor introduce un link de alguna web...')
        wait = await ctx.send(' | Pingingeando...')
        web = list(args)[0].replace('<', '').replace('>', '')
        if not web.startswith('http'): web = 'http://' + web
        try:
            a = t.now()
            ping = get(web, timeout=5)
            pingtime = round((t.now()-a).total_seconds()*1000)
            await wait.edit(content="", embed=discord.Embed(title=' | Ese sitio web está activo.', description='Ping: {} ms\nCódigo de estado: {}'.format(pingtime, ping.status_code), colour=color))
        except:
            await wait.edit(content=' | Si. ese sitio web está caído.')

    def imagefromURL(self, url): 
        return Image.open(BytesIO(get(url).content))

    def buffer(self, data):
        arr = BytesIO()
        data.save(arr, format='PNG')
        arr.seek(0)
        return arr

    def urltoimage(self, url):
        image = self.imagefromURL(url)
        return self.buffer(image)


class GeneralSecundario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def jsonisp(self, url):
        from requests import get as decodeurl
        return decodeurl(url).json()

    def urlify(self, word):
        from urllib.parse import quote_plus as urlencode
        return urlencode(word).replace('+', '%20')
    def api(self, url):
        return get(url).json()
    def dearray(self, arr):
        return str(', '.join(arr))+'.'

    def imagefromURL(self, url): 
        return Image.open(BytesIO(get(url).content))

    def buffer(self, data):
        arr = BytesIO()
        data.save(arr, format='PNG')
        arr.seek(0)
        return arr

    def urltoimage(self, url):
        image = self.imagefromURL(url)
        return self.buffer(image)


    @commands.command(aliases=["qr"], description="Crea un codigo QR o de barras poniendo m.barcode", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def barcode(self, ctx, *args):
        if len(list(args))==0:
            await ctx.send(' | Porfavor pon texto')
        elif len(' '.join(list(args))) > 50:
            await ctx.send(' | demasiado largooooooooooooooooooooooooo')
        else:
            async with ctx.message.channel.typing():
                if 'qr' in str(ctx.message.content).split(' ')[0][1:]: 
                    url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(self.urlify(str(' '.join(list(args)))))
                    await ctx.send(embed=discord.Embed(title="Codigo QR creado", url=f"{url}", colour=color).set_image(url=url))
                else: 
                    url= 'http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data='+str(self.urlify(str(' '.join(list(args)))))
                    await ctx.send(embed=discord.Embed(title="Codigo de barras creado", url=f"{url}", colour=color).set_image(url=url))


    @commands.command(description="Te dire un secreto increible")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def secret(self, ctx):
        secretlist = getSecrets()
        embed = discord.Embed(title='¿Savias que?', description="**"+random.choice(ctx.message.guild.members).name+"** |  "+str(random.choice(secretlist)), colour=color)
        embed.set_footer(text='No le digas esto a nadie más.')
        await ctx.message.author.send(embed=embed)
        await ctx.send('Compartí el secreto a través de DM. ¡No se lo muestres a nadie más! :wink::ok_hand:')

    @command(aliases=['fact-core', 'fact-sphere', 'factsphere'], description="Te dire una anecdota")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def factcore(self, ctx):
        data = self.jsonisp('https://raw.githubusercontent.com/dragonfire535/xiao/master/assets/json/fact-core.json')
        trans = Translator()
        traducted_data =  trans.translate(random.choice(data), src='en', dest='es')
        embed = discord.Embed(title='Centro de informacion', description=traducted_data.text, colour=color)
        embed.set_thumbnail(url='https://i1.theportalwiki.net/img/thumb/5/55/FactCore.png/300px-FactCore.png')
        await ctx.send(embed=embed)

    @commands.command(description="ME ABURROOOOOO")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bored(self, ctx):
        data = self.api("https://www.boredapi.com/api/activity?participants=1")
        trans = Translator()
        traducted_data =  trans.translate(data['activity'], src='en', dest='es')
        await ctx.send('**¿Aburrido?**\n'+str(traducted_data.text))

    @commands.command(description="Busca canciones en itunes", usage="<cancion>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def itunes(self, ctx, *args):
        if len(list(args))==0: return await ctx.send(' | ¡Porfavor pon un termino!')
        data = self.jsonisp('https://itunes.apple.com/search?term={}&media=music&entity=song&limit=1&explicit=no'.format(self.urlify(' '.join(list(args)))))
        if len(data['results'])==0: 
            return await ctx.send(' | No se encontro nada... oops...')
        data = data['results'][0]
        em = discord.Embed(title=data['trackName'], url=data['trackViewUrl'],description='**Artista: **{}\n**Album: **{}\n**Fecha de lancamiento:** {}\n**Genero: **{}'.format(
            data['artistName'], data['collectionName'], data['releaseDate'].replace('T', ' ').replace('Z', ''), data['primaryGenreName']
        ), color=color)
        em.set_thumbnail(url=data['artworkUrl100'])
        em.set_author(name='iTunes', icon_url='https://i.imgur.com/PR29ow0.jpg', url='https://www.apple.com/itunes/')
        await ctx.send(embed=em)

    @commands.command(description="JAJAJA DON COMEDIAS")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joke(self, ctx):
        data = self.api("https://official-joke-api.appspot.com/jokes/general/random")
        translated_setup = gtr.translate(data[0]["setup"], src='en', dest='es')
        translated_punch = gtr.translate(data[0]["punchline"], src='en', dest='es')
        embed = discord.Embed(
            title = str(translated_setup.text),
            description = '||'+str(translated_punch.text)+'||',
            colour = color
        )
        embed.set_thumbnail(url=random.choice(["https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/joypixels/257/rolling-on-the-floor-laughing_1f923.png", "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/google/263/face-with-tears-of-joy_1f602.png"]))
        await ctx.send(embed=embed)        

    def time_encode(self, sec):
        time_type = 'seconds'
        newsec = int(sec)
        if sec>60:
            newsec, time_type = round(sec/60), 'minuto/s'
            if sec>3600: 
                newsec, time_type = round(sec/3600), 'hora/s'
                if sec>86400:
                    newsec, time_type = round(sec/86400), 'dia/s'
                    if sec>2592000:
                        newsec, time_type = round(sec/2592000), 'mes/es'
                        if sec>31536000:
                            newsec, time_type = round(sec/31536000), 'año/s'
        return str(str(newsec)+' '+time_type)

    def getUser(self, ctx, args, user=None, allownoargs=False):
        if len(list(args))==0:
            return ctx.author
        if len(ctx.message.mentions)>0: 
            return ctx.message.mentions[0]
        name = str(' '.join(list(args))).lower().split('#')[0] 
        for i in ctx.guild.members:
            if name in str(i.name).lower():
                user = i; break
            elif name in str(i.nick).lower():
                user = i; break
        if user!=None: return user
        if list(args)[0].isnumeric():
            return ctx.guild.get_member(int(list(args)[0]))
        return ctx.author


    def limitto(self, text, limitcount):
        a = text
        if len(a) < limitcount: 
            return text
        while (len(a) > limitcount):
            temp = list(a)
            temp.pop()
            a = ''.join(temp)
        return a


    @commands.command(aliases=['pokedex','dex','bulbapedia','pokemoninfo','poke-info','poke-dex','pokepedia'], description="Info sobre un pockemon")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pokeinfo(self, ctx, *args):
        query = 'Missingno' if (len(list(args))==0) else self.urlify(' '.join(list(args)))
        try:
            trans = Translator()
            data = self.jsonisp('https://bulbapedia.bulbagarden.net/w/api.php?action=query&titles={}&format=json&formatversion=2&pithumbsize=150&prop=extracts|pageimages&explaintext&redirects&exintro'.format(query))
            translated_description = trans.translate(data['query']['pages'][0]['extract'], src='en', dest='es')
            embed = discord.Embed(
                url='https://bulbapedia.bulbagarden.net/wiki/{}'.format(query),
                color=color,
                title=data['query']['pages'][0]['title'], description=self.limitto(translated_description.text, 1000)
            )
            try:
                pokeimg = data['query']['pages'][0]['thumbnail']['source']
                embed.set_thumbnail(url=pokeimg)
            except:
                pass
            await ctx.send(embed=embed)
        except Exception as e:
            cprint("[Log] un error: " + e, 'red')
            return await ctx.send(" | ¡No se encontro un pockemon!")

    def html2discord(self, text):
        res = text.replace('<p>', '').replace('</p>', '').replace('<b>', '**').replace('</b>', '**').replace('<i>', '*').replace('</i>', '*').replace('<br />', '\n')
        return res

    @commands.command(description="Mira una serie de television", usage="[serie de tv]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tv(self, ctx, *args):
        if len(list(args))==0: 
            return await ctx.send(' | Porfavor dame argumentos')
        query = self.urlify(' '.join(list(args)))
        data = get(f'http://api.tvmaze.com/singlesearch/shows?q={query}')
        if data.status_code==404: 
            return await ctx.send(' | ¡Oops! No se encontro nada.')
        try:
            trans = Translator()
            data = data.json()
            star = str(':star:'*round(data['rating']['average'])) if data['rating']['average']!=None else 'No han dado ninguna reseña.'
            translated_des = trans.translate(self.html2discord(data['summary']), src='en', dest='es')
            translated_stats = trans.translate(data['status'], src='en', dest='es')
            translated_premired = trans.translate(data['premiered'], src='en', dest='es')
            translated_type = trans.translate(data['type'], src='en', dest='es')
            translated_languaje = trans.translate(data['language'], src='en', dest='es')
            translated_languaje = trans.translate(data['language'], src='en', dest='es')
            translated_schedule_time = trans.translate(data['schedule']['time'], src='en', dest='es')
            translated_schedule = trans.translate(self.dearray(data['schedule']['days']), src='en', dest='es')
            translated_gen = trans.translate(self.dearray(data['genres']), src='en', dest='es')
            em = discord.Embed(title=data['name'], url=data['url'], description=translated_des.text, color=color)
            em.add_field(name='Información general', value='**Estado: **'+translated_stats.text+'\n**Estrenada en: **'+translated_premired.text+'\n**Tipo: **'+translated_type.text+'\n**Lenguaje: **'+translated_languaje.text+'\n**Rating: **'+str(data['rating']['average'] if data['rating']['average']!=None else 'None')+'\n'+star)
            em.add_field(name='Red de televisión', value=data['network']['name']+' at '+data['network']['country']['name']+' ('+data['network']['country']['timezone']+')')
            em.add_field(name='Genero', value=translated_gen.text if len(data['genres'])>0 else 'Ningun genero avalibre')
            em.add_field(name='Calendario', value=translated_schedule.text+' en '+translated_schedule_time.text)
            em.set_image(url=data['image']['original'])
            await ctx.send(embed=em)
        except Exception as e:
            cprint(str("[Log] un error: " + e), 'red')
            await ctx.send(' | ¡Oops! Un error...')

    def insp(self, url):
        return requests.get(url).text

    @commands.command(description="Pon el texto en grande", usage="<texto>")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ascii(self, ctx, *args):
        text = '+'.join(list(args)) if len(list(args))>0 else 'ascii%20texto'
        try:
            await ctx.send('```{}```'.format(
                self.insp('http://artii.herokuapp.com/make?text={}'.format(text))
            ))
        except:
            await ctx.send('d | ¡Tu texto es muy largo!')

    @commands.command(description="Mira info de la nasa")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def nasa(self, ctx, *args):
        query = 'earth' if len(list(args))==0 else self.urlify(' '.join(list(args)))
        data = self.jsonisp(f'https://images-api.nasa.gov/search?q={query}&media_type=image')
        await ctx.channel.trigger_typing()
        if len(data['collection']['items'])==0: 
            return await ctx.send(' | No se encontro nada.')
        img = random.choice(data['collection']['items'])

        trans = Translator()
        translated_title, translated_info = trans.translate(img['data'][0]['title'], src='en', dest='es'), trans.translate(img['data'][0]["description"], src='en', dest='es')
       
        em = discord.Embed(title=translated_title.text, description=translated_info.text, color=color)
        em.set_image(url=img['links'][0]['href'])
        await ctx.send(embed=em)

    @commands.command(description="Una frase de alguien random")
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def quote(self, ctx):
        async with ctx.channel.typing():
            data = self.insp('https://quotes.herokuapp.com/libraries/math/random')
            text, quoter = data.split(' -- ')[0], data.split(' -- ')[1]
            translated_quote = Translator().translate(text, src='en', dest='es')
            await ctx.send(embed=discord.Embed(description=f'***{translated_quote.text}***\n\n-- {quoter} --', color=color))


    @commands.command(description="Letra de una cancion (PRIMERO SOLO PONES LA BANDA O AUTOR LUEGO EN OTRO MENSAJE SEPARADO PONES EL TITULO DE LA CANCION)")
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def lyrics(self, ctx: commands.Context, *, Comp: str):
        if len(Comp) == 0:
            return await ctx.send("¡Pon un artista!", delete_after=10.0)
        now = await ctx.send("Ahora pon la cancion")
        def check(m):
            return m.author == ctx.author
        try:    
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
        except TimeoutError:
            await now.delete()
            return await ctx.send("Tiempo agotado intenta ser mas rapido la siguiente vez", delete_after=10.0)
        else:
            Song = msg.content
            try:
                # print(f'https://api.lyrics.ovh/v1/{Comp}/{Song}')
                data = self.jsonisp(f'https://api.lyrics.ovh/v1/{Comp}/{Song}')
                # if data['error']:
                #     return await ctx.send("Upss. No se encontro nada")
                # print(data['lyrics'])
                await ctx.send(embed=discord.Embed(title=f"Letra de {Song}", description=f"**1... 2... 3... 4...**\n\n{data['lyrics']}", colour=color))
            except Exception as e:
                await ctx.send("Upss... un error. Intenta poner una cancion/artista valido")
                cprint(str("[Log] un error: " + e), 'red')

    @commands.command(description="Busca algo en wiki", usage="[pagina]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wikipedia(self, ctx, *args):
        wait = await ctx.send(' | Porfavor espera...')
        if len(list(args))==0:
            await wait.edit(content='¡Porfavor pon algun argumento!')
        else:
            wikipedia = wikipediaapi.Wikipedia('es')
            page = wikipedia.page(' '.join(list(args)))
            if page.exists()==False:
                await wait.edit(content='¡Esa pagina no existe!\n40404040404040404040404')
            else:
                if 'puede referirse a:' in page.text:
                    byCategory = page.text.split('\n\n')
                    del byCategory[0]
                    temp = ''
                    totalCount = 0
                    for b in byCategory:
                        if b.startswith('mira tambien') or len(temp)>950:
                            break
                        totalCount = int(totalCount)+1
                        temp = temp + str(totalCount)+'. ' + str(b) + '\n\n'
                    explain = temp
                    pageTitle = 'La página a la que puede hacer referencia puede ser;'
                else:
                    pageTitle = page.title
                    explain = ''
                    count = 0
                    limit = random.choice(list(range(2, 4)))
                    for i in range(0, len(page.summary)):
                        if count==limit or len(explain)>900:
                            break
                        explain = explain + str(list(page.summary)[i])
                        if list(page.summary)[i]=='.':
                            count = int(count) + 1
                embed = discord.Embed(title=pageTitle, url=str(page.fullurl), description=str(explain), colour=0xf7f7f7)
                await wait.edit(content='', embed=embed)

# import asyncio, time



# class Reminder(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot     
#         self.color = int(env["COLOR"])

#     def CalcularTiempo(self, t: float):
#         return t * 60

#     @commands.command(aliases=["remind"], description="Se te recordara una tarea que tu quieras", usage="<Tiempo: minutos> <Recordatorio: texto>")
#     @commands.cooldown(1, 20, commands.BucketType.user)
#     async def reminder(self, ctx: commands.Context, tiempo: float, *, texto):
#         autor = ctx.author
#         if tiempo is None and texto is None:
#             return await ctx.send(embed=discord.Embed(color=self.color, title="No has puesto el tiempo bien", description=f"{ctx.author.mention} no has puesto el tiempo correctamente\n**eg: m.reminder [minutos] <texto>**"))
#         t = self.CalcularTiempo(tiempo)
#         await ctx.send(embed=discord.Embed(color=self.color, title="Recordatorio añadido", description=f"{autor.mention} se te recordara en dentro de **{tiempo}** minuto/s"))
#         await asyncio.sleep(t)
#         start = time.perf_counter()
#         recormsg = await autor.send(embed=discord.Embed(color=self.color, title="RECORDATORIO", description=f"{ctx.author.mention} Has iniciado un recordatorio hace **{tiempo}** minutos. ").add_field(name="Recordatorio", value=texto))
#         end = time.perf_counter()
#         speed = round((end - start) * 1000)
#         await recormsg.edit(embed=discord.Embed(color=self.color, title="RECORDATORIO", description=f"{ctx.author.mention} Has iniciado un recordatorio hace **{tiempo}** minutos. ").add_field(name="Recordatorio", value=texto).add_field(name="tardanza", description=speed + "ms", inline=False))

def setup(bot):
    # bot.add_cog(Reminder(bot))
    bot.add_cog(General(bot))
    bot.add_cog(GeneralSecundario(bot))
