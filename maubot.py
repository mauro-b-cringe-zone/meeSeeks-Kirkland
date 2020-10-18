# -*- Programando: utf8 -*-
"""


La licencia del MIT (MIT)

Copyright (c) 2020 Maubg

Por la presente se otorga permiso, sin cargo, a cualquier persona que obtenga una
copia de este software y los archivos de documentación asociados (el "Software"),
para negociar con el Software sin restricciones, incluidas, entre otras,
los derechos de uso, copia, modificación, fusión, publicación, distribución, sublicencia,
y / o vender copias del Software, y permitir a las personas a quienes el
El software se proporciona para ello, sujeto a las siguientes condiciones:

El aviso de copyright anterior y este aviso de permiso se incluirán en
todas las copias o partes sustanciales del Software.

EL SOFTWARE SE PROPORCIONA "TAL CUAL", SIN GARANTÍA DE NINGÚN TIPO, EXPRESA
O IMPLÍCITA, INCLUYENDO PERO NO LIMITADO A LAS GARANTÍAS DE COMERCIABILIDAD,
APTITUD PARA UN PROPÓSITO PARTICULAR Y NO INFRACCIÓN. EN NINGÚN CASO
LOS AUTORES O TITULARES DE LOS DERECHOS DE AUTOR SERÁN RESPONSABLES DE CUALQUIER RECLAMO, DAÑOS U OTROS
RESPONSABILIDAD, YA SEA EN UNA ACCIÓN DE CONTRATO, AGRAVIO O DE OTRO MODO, QUE SURJA
DESDE, FUERA DE O EN RELACIÓN CON EL SOFTWARE O EL USO U OTROS
NEGOCIACIONES EN EL SOFTWARE.


                                                                                
                                                                 bbbbbbbb                                                    
MMMMMMMM               MMMMMMMM                                  b::::::b                                      tttt          
M:::::::M             M:::::::M                                  b::::::b                                   ttt:::t          
M::::::::M           M::::::::M                                  b::::::b                                   t:::::t          
M:::::::::M         M:::::::::M                                   b:::::b                                   t:::::t          
M::::::::::M       M::::::::::M  aaaaaaaaaaaaa  uuuuuu    uuuuuu  b:::::bbbbbbbbb       ooooooooooo   ttttttt:::::ttttttt    
M:::::::::::M     M:::::::::::M  a::::::::::::a u::::u    u::::u  b::::::::::::::bb   oo:::::::::::oo t:::::::::::::::::t    
M:::::::M::::M   M::::M:::::::M  aaaaaaaaa:::::au::::u    u::::u  b::::::::::::::::b o:::::::::::::::ot:::::::::::::::::t    
M::::::M M::::M M::::M M::::::M           a::::au::::u    u::::u  b:::::bbbbb:::::::bo:::::ooooo:::::otttttt:::::::tttttt    
M::::::M  M::::M::::M  M::::::M    aaaaaaa:::::au::::u    u::::u  b:::::b    b::::::bo::::o     o::::o      t:::::t          
M::::::M   M:::::::M   M::::::M  aa::::::::::::au::::u    u::::u  b:::::b     b:::::bo::::o     o::::o      t:::::t          
M::::::M    M:::::M    M::::::M a::::aaaa::::::au::::u    u::::u  b:::::b     b:::::bo::::o     o::::o      t:::::t          
M::::::M     MMMMM     M::::::Ma::::a    a:::::au:::::uuuu:::::u  b:::::b     b:::::bo::::o     o::::o      t:::::t    tttttt
M::::::M               M::::::Ma::::a    a:::::au:::::::::::::::uub:::::bbbbbb::::::bo:::::ooooo:::::o      t::::::tttt:::::t
M::::::M               M::::::Ma:::::aaaa::::::a u:::::::::::::::ub::::::::::::::::b o:::::::::::::::o      tt::::::::::::::t
M::::::M               M::::::M a::::::::::aa:::a uu::::::::uu:::ub:::::::::::::::b   oo:::::::::::oo         tt:::::::::::tt
MMMMMMMM               MMMMMMMM  aaaaaaaaaa  aaaa   uuuuuuuu  uuuubbbbbbbbbbbbbbbb      ooooooooooo             ttttttttttt  
                                                                                                                             
                                                                                                                             
                                                                                                                             
"""

# ````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````

__author__ = "Maubg"
__copyright__ = "Copyright (C) 2020 Maubg"
__license__ = "Public Domain"
__version__ = "1.4.1"




from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from discord.ext import commands, tasks
from discord.ext.commands import bot
from typing import Optional
from discord import Member, activity, message
from urllib import parse, request
from dotenv import load_dotenv
from discord.utils import find
from discord.utils import get
from itertools import cycle
from mauutils.mauunicode import *
from mauutils.secrete import *
from mauutils.fun.lists import *
from mauutils.hack import *
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pyqrcode
import traceback
from os import system 
from googletrans import Translator
import string
import shutil
import sqlite3
import dbl
import youtube_dl
import datetime
import discord
import praw
import asyncio
import logging
import random
import aiohttp
from aiohttp import request
import asyncio
import hashlib
import shutil
import utils
import json
import time
from PIL import Image, ImageFilter 
import re
import sys
import os


def get_prefix(bot, message):
    with open('./json/prefix.json', 'r') as f:
        prefixes = json.load(f)
    base = [prefixes[str(message.guild.id)], '?', '!', 'm.']
    return base

load_dotenv()
bot = commands.Bot(command_prefix = get_prefix, description="Maubot | El mejor bot para divertirse")
bot.remove_command('help')
bot.remove_command('warn')
bot.remove_command('next')
bot.remove_command('sum')

def main():


    @bot.event
    async def on_ready():

        print("""
             __    __     ______     __  __     ______     ______     ______  
            /\ "-./  \   /\  __ \   /\ \/\ \   /\  == \   /\  __ \   /\__  _\ 
            \ \ \-./\ \  \ \  __ \  \ \ \_\ \  \ \  __<   \ \ \/\ \  \/_/\ \/ 
             \ \_\ \ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_____\    \ \_\ 
              \/_/  \/_/   \/_/\/_/   \/_____/   \/_____/   \/_____/     \/_/                                                             
        """)

        # change_status.start()
        DEVMODE = True
        print("\n------------------------------------->\n"
            # f"Knecht Bot v.%s\n"
            f"Version de discord.py: {discord.__version__}\n"
            f"Prefijo: '$'\n"
            f"ModoDev: {'Activo' if DEVMODE else 'Inactivo'}\n"
            f"Estoy en: {len(bot.guilds)} Servidores\n"
            f"Estado: Actualizado\n"
            "------------------------------------->\n")

        print("\n------------------------------------->\n"
            f"COGS\n"
            f"Secrete.py a reyenado al token y los colores\n")

        # TODOS LOS ESTADOS: online, offline, idle, dnd, invisible

        while True:
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"|  $help  |  {len(bot.users)} Usuarios en  {len(bot.guilds)} servidores | con 186 commandos"))
            await asyncio.sleep(10) 
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"https://top.gg/bot/730124969132163093"))
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"| Enviando memes a los  {len(bot.users)} usuarios | "))
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"| Mejorandome para dominar el mundo | "))
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name=f"| Hackeando sistemas del pais | "))
            await asyncio.sleep(10)
            await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=f"| Haciendo una tarta | "))
            await asyncio.sleep(10)


    # Cuando el bot entra al servidor
    @bot.event
    async def on_guild_join(guild):
        # if not guild.id == 336642139381301249:
        def check(event):
            return event.target.id == bot.user.id
        bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).find(check)
        msg_ent = await bot_entry.user.send(embed=discord.Embed(title="Holaaaaaa", description=f""":tada: ¡¡¡Hola!!!Mi nombre e **{bot.user.name}**, Y soy el responsable que te ayudara 
            a ganar partidas en el destini `hacer tu server mejor` porque tu eres 
            uno de los mejores socios que voy a tener, asique, gracias por invitarme a **{guild.name}**.\n\n
            **El prefijo del comando es: `$`**\n\n
            Ese es mi prefijo, siempre puedes hacerme menciones con **@{bot.user.name}**. 
            Si otro bot esta usando el mismo prefijo. `deves anikilarlo` es broma
            para cambiar de prefijo tienes que poner **$server** y luego **$prefix <nuevo prefijo>** (NO USES LOS BRACKETS).\n\n
            Para una lista de commando solo tienes que poner $help y te saldran tooodos los comandos. 
            \n\n
            y se enviara un mensaje a mi desarroyador! por si quieres poner una nueva cosa nueva en el bot, o poner un bug, 
            mantente actualizado con las nuevas funciones, o si solo quieres mas ayuda, mira el server oficial de 
            {bot.user.name} ¿¡A que esperas!? ( https://discord.gg/4gfUZtB )""", colour=color))

    
        with open('./json/prefix.json', 'r') as f:
            prefixes = json.load(f)
        
        prefixes[str(guild.id)] = '$'

        with open('./json/prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        channel = discord.utils.get(guild.text_channels)
        # if not guild.id == 336642139381301249:

        embed1 = discord.Embed(title="Maubot - el mejor bot de la historia", description="Maubot es un bot para que tu puedas hacer cosas diversas en tu servidor.\n\nMaubot tiene muchas funciones como: divertirte, puedes cambiar el prefijo del bot (por si quieres) y al igual ponerle un **__nickname__** , muchas cosas mas. Si quieres saber mas tu solo pon `$help` o con el prefijo que tu le ayas puesto.\n\n **ESCRIVE $verify PARA VERIFICAR QUE ERES HUMANO**", colour=color)
        embed1.set_author(name='Maubot', icon_url="https://img.icons8.com/nolan/64/launched-rocket.png")
        embed1.add_field(name="¿Necesitas ayuda?", value=f"Puedes poner **$help** para conseguir una lista de los comandos mas guays del mundo desde diversion hasta musica y economia. La lista de comandos estan separadas por secciones asi que podrias poner `$help [seccion]` para descubrir mas comandos super chulos. o si no puedes poner **<@730124969132163093>** .", inline=True)
        embed1.add_field(name="Diversion atope", value=f"Maubot tiene muchos comando para divertirse con manipulacion de imagenes a juegos como el `ajedrez`, `conecta4`, `rps` y mucho mas. Maubot tambien tiene un sistema de economia muy avanzado para ser millonarios y dominar el mundo 🤤...", inline=True)
        embed1.add_field(name="Legal", value=f"Escribe `$copyright` para ver el copyright de Maubot y tambien escribe `$verify` para erificar que eres humano", inline=False)
        embed1.add_field(name="¿Aun no te has enterado?", value=f"Puedes ver un tutorial de como usar Maubot poniendo <@730124969132163093>", inline=False)
        embed1.set_footer(text="Maubot - Puedes escribir @Maubot para mas info")


        msg_h1 = await channel.send(content="Hola, gracias por meterme en este servidor. \nlos mensajes de abajo os explicaran algunas características sobre mi.\nSi alguien quiere apoyar mi servidor por favor dale a este link **(https://discord.gg/4gfUZtB)**", embed=embed1)


    @bot.command()
    async def verify(ctx):
        embed5 = discord.Embed(title="Verifica que eres humano", description="En estos tiempos Discord cadavez tiene mas atackes de bots por lo que para mas seguridad verificar que no soy robots. \n\n porfavor dale al ✅ para comfirmar que no eres un robot", colour=0x1cce52)
        embed5.set_footer(text='Maubot | Verifica que eres humano')
        
        embed = discord.Embed(title="Bien eres humano", description="Ya puedes comenzar a usar el bot... pero cuidado. ajajaja solo bromeaba disfruta", colour=color)
        embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")


        msg = await ctx.send(embed=embed5)
        await msg.add_reaction('✅')
        guild = bot.get_guild(ctx.guild.id)
        def _check(reaction, user):
            return (
                reaction.emoji in '✅'
                and user == ctx.author
                and reaction.message.id == msg.id
            )
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=600, check=_check)
        except asyncio.TimeoutError:
            await bot.leave_guild(guild)
        else:
            await msg.edit(embed=embed)



    @bot.event
    async def on_guild_remove(guild):

        # channel = discord.utils.get(guild.channels, name='general')

        # await channel.send("Veo que me has eliminado de tu servidor. Puedes unirte al mio y contarme porque lo hicistes -- (https://discord.gg/kKsxbJ)")

        with open('./json/prefix.json', 'r') as f:
            prefixes = json.load(f)
        
        del prefixes[str(guild.id)]

        with open('./json/prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @bot.command()
    @commands.cooldown(1, 25, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def reglas(ctx):

        await ctx.message.delete()
        
        # await ctx.send(f"Hola @everyone, aqui estan las reglas de este servidor si no se cumplen el usuario sera baneado depende de lo que haya echo. Dale al ✅ para saver si las has leido")

        embed = discord.Embed(title="Reglas", description="Teneis que seguir estas reglas o sereis baneados", colour=color)
        embed.add_field(name="#1 | No insultar/ser racista", value="Al no hacer caso ha este commando depende de como sea el tamaño de el insulto o comentario racista, el usuario sera **baneado durante 1 semana**", inline=False)
        embed.add_field(name="#2 | No tener nombres inapropiados", value="Si un usuario tiene un nombre inapropiado sera renombrado", inline=False)
        embed.add_field(name="#3 | No usar maubot de forma estupida", value="Si se trata a maubot de forma estupida el usuario que lo hizo sera baneado por 2 semanas", inline=False)
        embed.add_field(name="#4 | No contradecir las normas de los mas superiores", value="Si un administrador o alguien con autoridad os dice que no agais algo no lo agais sino sereis expulsados o baneados", inline=False)
        embed.add_field(name="#5 | No patrocinar", value="Si alguien patrocina en este servidor sera muteado por 3 semanas", inline=False)
        embed.add_field(name="#6 | Usar los canales apropiados", value="Si por ejemplo quereis jugar a economia teneis que ir a  <#739407816724316210>", inline=False)
        embed.add_field(name="#7 | No mencionar a los que tienen autoridad", value="Si se hace esta accion se muteara al qu lo hico durante 2 semanas", inline=False)
        embed.add_field(name="#8 | No discutas con los que tienen autoridad", value="Se ara 1 semana de muteo para esta persona", inline=False)
        embed.add_field(name="#9 | Nada ilegal", value=f"{ctx.prefix}se baneara a la persona durante 2 semanas", inline=False)
        embed.add_field(name="#10 | PASARLO BIEN", value="Disfrutar...", inline=False)



        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✅')



    @bot.command()
    @commands.cooldown(1, 25, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def prefix(ctx, prefix):

        with open('./json/prefix.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('./json/prefix.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        e = discord.Embed(title="**__Se a cambiado el prefijo correctamente__**", description=f'Se a cambiado el prefijo a:     `{prefix}`', colour=color)
        e.add_field(name="\uFEFF", value="\uFEFF", inline=False)
        e.add_field(name="¡Tenemos un servidor!", value="**Unete a nuestro server   -->   ( https://discord.gg/4gfUZtB )**")
        await ctx.send(embed=e)


    # Eventos para el robot

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, CommandOnCooldown):
            embed = discord.Embed(title="Tranquilo...", description=f"{ctx.author.mention} Este comando esta en reposo\n Ahora tienes que esperar **{error.retry_after:,.2f}** segundos", colour=color)
            await ctx.send(embed=embed)
            # await ctx.send('hola')

        if isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(title="404", description=f"{ctx.author.mention} Este comando esta **desactivado** intentalo mas tarde", colour=color)
            await ctx.send(embed=embed)

        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="....", description=f"{ctx.author.mention} Este comando es para mi creador\n\nVete y consigue una vida.", colour=color)
            await ctx.send(embed=embed)

        if isinstance(error, commands.NoPrivateMessage):
            embed = discord.Embed(title="NO", description=f"{ctx.author.mention} Este comando no es para canale de DM", colour=color)
            await ctx.send(embed=embed)

        if isinstance(error, commands.TooManyArguments):
            embed = discord.Embed(description=f"{ctx.author.mention} Escribe menos argumentos por favor.", colour=color_error)
            embed.set_author(name="Demasiado", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
            embed.set_footer(text='\n-- ERROR')
            msg_error = await ctx.send(embed=embed)
            await msg_error.add_reaction('❌')

        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(description=f'> {ctx.author.mention} Puedes escribir ** {ctx.prefix}help" ** para mas informacion', colour=color_error)
            embed.set_author(name="Escribe un argumento valido", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
            embed.set_footer(text='\n-- ERROR')
            msg_error = await ctx.send(embed=embed)
            await msg_error.add_reaction('❌')

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description=f'> {ctx.author.mention} Puedes escribir ** "{ctx.prefix}help" ** para mas informacion', colour=color_error)
            embed.set_author(name="Escribe todos los argumentos requeridos", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
            embed.set_footer(text='\n-- ERROR')
            msg_error = await ctx.send(embed=embed)
            await msg_error.add_reaction('❌')


        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(description=f'> {ctx.author.mention} Puedes escribir ** "{ctx.prefix}help" ** para mas informacion', colour=color_error)
            embed.set_author(name=f"Necesitas permisos para hacer esto", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
            embed.add_field(name="\uFEFF", value=f"Permisos necesarios: `{Translator().translate(str([perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]), src='en', dest='es').text}`")
            embed.set_footer(text='\n-- ERROR')
            msg_error = await ctx.send(embed=embed)
            await msg_error.add_reaction('❌')

        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(description=f'> {ctx.author.mention} Puedes escribir ** {ctx.prefix}help" ** para mas informacion', colour=color_error)
            embed.set_author(name="Tienes que tener los roles correctos", icon_url="https://img.icons8.com/color/48/000000/do-not-disturb.png")
            embed.set_footer(text='\n-- ERROR')
            msg_error = await ctx.send(embed=embed)
            await msg_error.add_reaction('❌')

        # if isinstance(error, commands.CommandNotFound): 
        #     embed = discord.Embed(title="❌ Escribe un commando que exista", description=f'> Puedes escribir ** "{ctx.prefix}help" ** para mas informacion', colour=color_error)
        #     embed.set_footer(text='\n-- ERROR')
        #     msg_error = await ctx.send(embed=embed)
        #     await msg_error.add_reaction('❌')

        def _check(reaction, user):
            return (
                reaction.emoji in '❌'
                and user == ctx.author
                and reaction.message.id == msg_error.id
            )
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000, check=_check)
        except asyncio.TimeoutError:
            await msg_error.delete()
        else:
            await msg_error.delete()



    # @bot.event
    # async def on_member_join(member):

    #     # if not guild.id == 336642139381301249:

    #         for channel in member.guild.text_channels:

        

    #             embed = discord.Embed(title="{}, info".format(member.name), description="Bienvenido a {}".format(member.guild.name), colour=color)
    #             embed.add_field(name="Nombre", value=member.name, inline=True)
    #             embed.add_field(name="ID", value=member.id, inline=True)
    #             embed.add_field(name="Estado", value=member.status, inline=True)
    #             embed.add_field(name="Roles", value=member.top_role)
    #             embed.add_field(name="Unido", value=member.joined_at)
    #             embed.add_field(name="Creado", value=member.created_at)
    #             embed.set_thumbnail(url=member.avatar_url)
                
    #             channel = discord.utils.get(member.guild.channels, name='bienvenido')

    #             if channel is None:
    #                 guild = member.guild
    #                 await guild.create_text_channel('bienvenido')

    #         await channel.send(embed=embed)

    #         await member.create_dm()
    #         await member.dm_channel.send(
    #             'Hola {}, ¡Bienvenido server ¡espero que te lo pases bien!'.format(member.mention)
    #         )

    #         role = discord.utils.get(member.guild.roles, name="miembros")
    #         await member.add_roles(role)

    # @bot.event
    # async def on_member_remove(member):

    #     # if not guild.id == 336642139381301249:

    #         for channel in member.guild.text_channels:

    #             channel_cr = discord.utils.get(member.guild.channels, name='bienvenido')

    #             if channel_cr is None:
    #                 guild = member.guild
    #                 await guild.create_text_channel('bienvenido')


    #         msg = "{} se ha ido del servidor".format(member.mention)
    #         await channel_cr.send(msg)

    ############
    # COMANDOS #
    ############

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _bot(ctx, inf_con):
        if inf_con == 'info':
            em = discord.Embed(timestamp=datetime.datetime.utcnow(), colour=color)
            em.title = 'Info de Maubot'
            em.set_author(name=ctx.author.name, icon_url="https://img.icons8.com/plasticine/100/000000/bot.png")
            try:
                em.description = bot.psa + '\n[Soporta nuestro server](https://discord.gg/4gfUZtB)'
            except AttributeError:
                em.description = 'Un bot echo por [Maubg](https://www.youtube.com/channel/UCnNQ8-WPlcMqKpTdvAL8_HA). [¡Ùnete a que esperas!](https://discord.gg/4gfUZtB)'
            em.add_field(name="Servidores", value=f"> {len(bot.guilds)}")
            em.add_field(name="Usuarios online", value=f"> {str(len({m.id for m in bot.get_all_members() if m.status is not discord.Status.offline}))}")
            em.add_field(name='Usuarios totales', value=f"> {len(bot.users)}")
            em.add_field(name="Librerías", value=f"> discord.py")
            em.add_field(name="Tardanza de respuesta", value=f"> {bot.ws.latency * 1000:.0f} ms")        
            em.add_field(name="Color de maubot", value=f"> {color}")                 
            em.add_field(name="Creador de maubot", value=f"> Maubg ︻芫═───#2688")         
            em.add_field(name="id de maubot", value=f"> 730124969132163093")  
            em.add_field(name="discriminador", value=f"> #6247")    
            em.add_field(name="prefijo", value=f"> {ctx.prefix}") 
            em.add_field(name="descripcion", value=f"{bot.description}") 
            em.add_field(name="Invita al bot", value=f"> [Invita al bot](https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot)", inline=True)

            em.add_field(name="INFORMACÍON", value="```Maubot es un discord bot que puede ser utilizado para ajustar servidores, roles, diversíon, imagenes, informacíon, y mucho mas. El creador es (Maubg ︻芫═───#2688) por si quereis contactarlo.```", inline=False)
            em.set_footer(text="Maubot | Echo por Maubg")
            await ctx.send(embed=em) 

        if inf_con == 'config':
            em = discord.Embed(timestamp=datetime.datetime.utcnow(), colour=color)
            em.title = 'Configuracion de Maubot'
            em.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            try:
                em.description = bot.psa + '[Soporta nuestro server](https://discord.gg/4gfUZtB)'
                # CAMBIAR LINK AL TENER UN SERVER DE VERDAD
            except AttributeError:
                em.description = '[¡Unete a que esperas!](https://discord.gg/4gfUZtB)'
                # CAMBIAR LINK AL TENER UN SERVER DE VERDAD
            em.add_field(name="Prefix", value=f"Escribe este commando y luego el prefijo que quieras **ej: {ctx.prefix}prefix !**")
            em.add_field(name='rename_bot', value=f'Puedes usar este comando para ponerle in __nickname__ a Maubot.', inline=False)
            em.add_field(name='rate_bot <commentario>', value=f'Puedes darle un rating de 5 estrellas.', inline=False)


            em.set_footer(text="Maubot | Echo por Maubg")
            await ctx.send(embed=em) 


    @bot.command(aliases=['permisos_visu'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def permisos(ctx, *, member: discord.Member=None):

        if not member:
            member = ctx.author



        perms = ',\n'.join(perm for perm, value in member.guild_permissions if value)
        from googletrans import Translator
        trans = Translator()
        embed = discord.Embed(title=f'Los permisos de {member} son:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        translated_perms = trans.translate(perms, src="en", dest="en")
        embed.add_field(name='\uFEFF', value=translated_perms.text)

        await ctx.send(content=None, embed=embed)

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rate_bot(ctx, *, texto):
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
            reaction, user = await bot.wait_for("reaction_add", timeout=20, check=_check)
            embed_done.add_field(name="Gracias por tu calificacion", value=f"estrellas: **{reaction.emoji}**\n\n**Descripcion:**\n{texto}\n **Si quieres te puedes unir a [nuestro server](https://discord.gg/4gfUZtB) para decirnos que tal tu experencia**")


        except asyncio.TimeoutError:
            await msg.clear_reactions()
            await msg.edit(embed=embed_time_out)

        else:
            await msg.clear_reactions()
            await msg.edit(embed=embed_done)    

            feedbackCh = bot.get_channel(748235336869478441)
            embed_feed_CH = discord.Embed(title=f"Nueva reseña", colour=color)
            embed_feed_CH.add_field(name="Calificacion:", value=f"estrellas: **{reaction.emoji}**\n\n**Descripcion:**\n{texto}")
            await feedbackCh.send('<@700812754855919667>, Usuario con ID: '+str(ctx.message.author.id)+f' Ha enviado una reseña', embed=embed_feed_CH)


    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(ctx, member:discord.Member = None):
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


    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def palmadas(ctx, *, message):
        msg = message.replace(" ", " 👏 ")

        await ctx.send(msg)


    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(ctx, member: discord.Member = None):
        member = ctx.author if member == None else member
        embed = discord.Embed(title=f"**Avatar de -- ({member})**", description=f"[Link]({member.avatar_url})",colour=color)
        embed.set_image(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def token(ctx):
        embed = discord.Embed(title="".join([random.choice(list('abcdefghijklmnopqrstuvwxyz._=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.')) for i in range(59)]), colour=color)
        await ctx.send(embed=embed)

    @bot.command(asliases=['link', 'links'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(ctx):

        embed = discord.Embed(description=f"**Link para el bot: [Mi link](https://discord.com/oauth2/authorize?client_id=730124969132163093&permissions=8&scope=bot)\n\nServer: (https://discord.gg/4gfUZtB)**\n\nWeb: **[Link](http://maubot.mooo.com/maubot/)**", colour=color)
        embed.set_author(name="INVITACIONES", icon_url="https://img.icons8.com/color/48/000000/share.png")
        embed.set_image(url="https://top.gg/api/widget/730124969132163093svg?usernamecolor=FFFFFF&topcolor=000000")
        # embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")
        await ctx.send(embed=embed)

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def owner(ctx):

        embed = discord.Embed(title="👑 Owner del servidor", colour=color)
        embed.add_field(name=f"El owner de __{ctx.guild.name}__ es:", value=f"\n👑 **{ctx.guild.owner}**", inline=False)
        embed.set_thumbnail(url=f"{ctx.guild.owner.avatar_url}")
        embed.set_footer(text=f"Puesto por | {ctx.author}")
        embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")
        await ctx.send(embed=embed)

    # MATES

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sum(ctx, numOne: int, numTwo: int):
        embed = discord.Embed(title=f"{numOne} + {numTwo} = {numOne + numTwo}", colour=color)
        await ctx.send(embed=embed)
        
    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def mul(ctx, numOne: int, numTwo: int):
        embed = discord.Embed(title=f"{numOne} x {numTwo} = {numOne * numTwo}", colour=color)
        await ctx.send(embed=embed)

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def div(ctx, numOne: int, numTwo: int):
        embed = discord.Embed(title=f"{numOne} / {numTwo} = {numOne / numTwo}", colour=color)
        await ctx.send(embed=embed)


    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def restar(ctx, numOne: int, numTwo: int):
        embed = discord.Embed(title=f"{numOne} - {numTwo} = {numOne - numTwo}", colour=color)
        await ctx.send(embed=embed)

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rz(ctx, numOne: int):
        embed = discord.Embed(title=f"La raiz cuadrda de {numOne} es:    {numOne ** (1/2)}", colour=color)
        await ctx.send(embed=embed)




    # FINAL DE MATES




    # BUSCADOR DE VIDEOS

    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def youtube(ctx, *search):
        import urllib.parse
        import urllib.request
        query_string = urllib.parse.urlencode({'search_query': search})
        html_content = urllib.request.urlopen('http://www.youtube.com/results?'+str(query_string))
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})', html_content.read().decode())
        print(search_results)
        await ctx.send('https://www.youtube.com/watch?v='+str(search_results[0]))

    # BUSCADOR DE IMAGENES

    ############################################
    # SYSTEMA DE NIVELES | no palabrotas |spam #
    ############################################

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def rename_bot(ctx, *, text='Maubot'):
        await ctx.message.guild.me.edit(nick=text)
        await ctx.send(f'Apodo establecido a {text}')



    # JUEGOS





    # RE = NECESITA REPARACION

    @bot.command(aliases=["honk"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def honkhonk(ctx):
        await ctx.send(random.choice(honkhonkfgt))

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def say(ctx, *, message:str):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(message)

    # @bot.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def cat(ctx):
    #     async with ctx.session.get('htts://api.thecatapi.com/v1/images/search') as resp:
    #         if resp.status != 200:
    #             return await ctx.send('No se encontro ningun gato :(')
    #         js = await resp.json()
    #         await ctx.send(embed=discord.Embed(title='Meowwww').set_image(url=js[0]['url']))

    # @bot.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def dog(ctx):
    #     async with ctx.channel.typing():
    #         async with aiohttp.ClientSession() as cs:
    #             async with cs.get("https://random.dog/woof.json") as r:
    #                 data = await r.json()

    #                 embed = discord.Embed(title="Woof Woof", colour=color)
    #                 embed.set_image(url=data['url'])
    #                 embed.set_footer(text="http://random.dog/")

    #                 await ctx.send(embed=embed)

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Floof", colour=color)
                    embed.set_image(url=data['image'])
                    embed.set_footer(text="https://randomfox.ca/")

                    await ctx.send(embed=embed)


    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def infinite(ctx):

        await ctx.send("https://media1.tenor.com/images/1c50bdbc44d5433fa3c67758dde775d2/tenor.gif")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dad(ctx):

        await ctx.send("https://cdn.discordapp.com/attachments/265156322012561408/744860278683992094/dad.jpg")

    # @bot.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def info_animal(ctx, animal: str):
    #     if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
    #         fact_url = f"https://some-random-api.ml/facts/{animal}"
    #         image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

    #         async with request("GET", image_url, headers={}) as response:
    #             if response.status == 200:
    #                 data = await response.json()
    #                 image_link = data["link"]

    #             else:
    #                 image_link = None

    #         async with request("GET", fact_url, headers={}) as response:
    #             if response.status == 200:
    #                 data = await response.json()

    #                 embed = Embed(title=f"Info de {animal.title()}",
    #                                 description=data["fact"],
    #                                 colour=colo)
    #                 if image_link is not None:
    #                     embed.set_image(url=image_link)
    #                 await ctx.send(embed=embed)
    #             else:
    #                 await ctx.send(f"El api a devuelto el estado '{response.status}'")

    #     else:
    #         embed_error = discord.Embed(title="No se a conseguido conseguir informacion", description="Aqui tienes una lista de animales validos\n> dog\n> panda\n> cat\n> koala\n> fox\n> bird", colour=color_error)
    #         await ctx.send(embed=embed_error)





    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def f(ctx):
        with open('./mauutils/languages/spanish.json', 'r') as f:
            Language = json.load(f)
        await ctx.send(Language.get("fun.respects", ctx).format(ctx.author, random.randint(1, 10000)))

    @bot.command()
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def nicememe(ctx):
        await ctx.send("http://niceme.me")

    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def spam(ctx):
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/spam.png"))

    # @bot.command()
    # async def random(ctx, subreddit: str=""):
    #     async with ctx.channel.typing():
    #         if ctx.reddit:

    #             chosen_subreddit = REDDIT_EANABLE_MEME_SUBREDDITS[0]
    #             if subreddit:

    #                 if subreddit in REDDIT_EANABLE_MEME_SUBREDDITS:
    #                     chosen_subreddit = subreddit

    #                 else:

    #                     ctx.send("Porfavor pon un subrredit valido")
    #             submissions = ctx.reddit.subreddit(chosen_subreddit).hot()

    #             post_to_pick = random.randqint(1,10)

    #             for i in range(0, post_to_pick):

    #                 submisions = next(x for x in submissions if not x.stickied) 
    #             await ctx.send(submissions.url)

    #         else:

    #             await ctx.send("Esto no funciona contacta al administrador o creador")


    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hack(ctx, *args):
        foundArgs, tohack = False, None
        try:
            tohack = ctx.guild.get_member(int(list(args)[0]))
            assert tohack!=None
            foundArgs = True
        except: 
            pass
        if len(ctx.message.mentions)<1 and not foundArgs:
            await ctx.send(f'Porfavor pon a alguien!\nejemplo: {ctx.prefix}hack <@'+str(ctx.message.author.id)+'>')
        if tohack==None: 
            tohack = ctx.message.mentions[0]
        console = 'nombredeusuario601@HACKERMAN:/$ '
        if len(ctx.message.mentions)>0 or foundArgs:
            main = await ctx.send('Abriendo consola...\n```bash\nCargando...```')
            flow = hackflow(tohack)
            for i in range(0, len(flow)):
                console = console + flow[i][1:]
                await main.edit(content=f"```bash\n{console}```")
                await asyncio.sleep(random.randint(5, 6))
        else:
            console += 'ERROR: TAG INVALIDP.\nACCESO DENEGADO.\n\nCódigo cifrado en base64 con codificación hash:\n'+bin(ctx.message.author.name)+ '\n' + console
            await ctx.send(f'```bash\n{console}```')


    @bot.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coin(ctx):
        n = random.randint(0, 1)
        if n == 0:
            msg = "Cara"
        elif n == 1:
            msg = "Cruz"
        await ctx.send(f"Ha tocado: **{msg}**")

    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def b1nzy(ctx):
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/b1nzy_with_banhammer.png"))

    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def cykablyat(ctx):
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/cykablyat.jpg"))

    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def sombra(ctx):
        await ctx.send("```\n                       :PB@Bk:                         \n                   ,jB@@B@B@B@BBL.                     \n                7G@B@B@BMMMMMB@B@B@Nr                  \n            :kB@B@@@MMOMOMOMOMMMM@B@B@B1,              \n        :5@B@B@B@BBMMOMOMOMOMOMOMM@@@B@B@BBu.          \n     70@@@B@B@B@BXBBOMOMOMOMOMOMMBMPB@B@B@B@B@Nr       \n   G@@@BJ iB@B@@  OBMOMOMOMOMOMOM@2  B@B@B. EB@B@S     \n   @@BM@GJBU.  iSuB@OMOMOMOMOMOMM@OU1:  .kBLM@M@B@     \n   B@MMB@B       7@BBMMOMOMOMOMOBB@:       B@BMM@B     \n   @@@B@B         7@@@MMOMOMOMM@B@:         @@B@B@     \n   @@OLB.          BNB@MMOMOMM@BEB          rBjM@B     \n   @@  @           M  OBOMOMM@q  M          .@  @@     \n   @@OvB           B:u@MMOMOMMBJiB          .BvM@B     \n   @B@B@J         0@B@MMOMOMOMB@B@u         q@@@B@     \n   B@MBB@v       G@@BMMMMMMMMMMMBB@5       F@BMM@B     \n   @BBM@BPNi   LMEB@OMMMM@B@MMOMM@BZM7   rEqB@MBB@     \n   B@@@BM  B@B@B  qBMOMB@B@B@BMOMBL  B@B@B  @B@B@M     \n    J@@@@PB@B@B@B7G@OMBB.   ,@MMM@qLB@B@@@BqB@BBv      \n       iGB@,i0@M@B@MMO@E  :  M@OMM@@@B@Pii@@N:         \n          .   B@M@B@MMM@B@B@B@MMM@@@M@B                \n              @B@B.i@MBB@B@B@@BM@::B@B@                \n              B@@@ .B@B.:@B@ :B@B  @B@O                \n                :0 r@B@  B@@ .@B@: P:                  \n                    vMB :@B@ :BO7                      \n                        ,B@B                           ```")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lenny(ctx):
        await ctx.send("( ͡° ͜ʖ ͡° )")
        
    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tableflip(ctx):
        await ctx.send("(╯°□°）╯︵ ┻━┻")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def doubleflip(ctx):
        await ctx.send("┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def misc_weeb_face(ctx):
        await ctx.send("(・`ω´・)")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gun(ctx):
        await ctx.send("︻芫═───")

    @bot.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def psat(ctx):
        await ctx.send(random.choice(psat_memes))

    # @bot.command()
    # @commands.cooldown(1, 25, commands.BucketType.user)
    # async def ball(ctx, *, question:str):
    #     await ctx.send("{}: {}".format(ctx.author.name, random.choice(magic_conch_shell)))

    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def insult(ctx, *, user:str):
        await ctx.send("{} {}".format(user, random.choice(insults)))

    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def actdrunk(ctx):
        await ctx.send(random.choice(drunkaf))

    @bot.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def rate(ctx, user:discord.User=None):
        with open('mauutils/languages/spanish.json', 'r') as f:
            Language = json.load(f)
        if user is None or user.id == ctx.author.id:
            await ctx.send(Language.get("fun.rate_author", ctx).format(random.randint(10)))
        elif user == ctx.bot.user:
            await ctx.send(Language.get("fun.rate_self", ctx))
        else:
            await ctx.send(Language.get("fun.rate_user", ctx).format(user.name, random.randint(0, 10)))

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def plzmsgme(ctx, *, message:str):

        with open('./mauutils/languages/spanish.json', 'r') as f:
            Language = json.load(f)

        await ctx.author.send(message)
        await ctx.send(Language.get("fun.plzmsgme", ctx))

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def twentyoneify(ctx, *, input:str):
        await ctx.send(input.replace("O", "Ø").replace("o", "ø"))

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spellout(ctx, *, msg:str):

        await ctx.send(" ".join(list(msg.upper())))


    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reverse(ctx, *, msg:str):
        await ctx.send("🔁 " + msg[::-1])

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def intellect(ctx, *, msg:str):
        await ctx.channel.trigger_typing()
        intellectify = ""
        for char in msg:
            intellectify += random.choice([char.upper(), char.lower()])
        await ctx.send(intellectify)

    encode_morse ={
        "1":".----",
        "2":"..---",
        "3":"...--",
        "4":"....-",
        "5":".....",
        "6":"-....",
        "7":"--...",
        "8":"---..",
        "9":"----.",
        "0":"-----",
        "A":".-",
        "B":"-...",
        "C":"-.-.",
        "D":"-..",
        "E":".",
        "F":"..-.",
        "G":"--.",
        "H":"....",
        "I":"..",
        "J":".---",
        "K":"-.-",
        "L":".-..",
        "M":"--",
        "N":"-.",
        "O":"---",
        "P":".--.",
        "Q":"--.-",
        "R":".-.",
        "S":"...",
        "T":"-",
        "U":"..-",
        "V":"...-",
        "W":".--",
        "X":"-..-",
        "Y":"-.--",
        "Z":"--..",
        ".":".-.-.-",
        ",":"--..--",
        ":":"---...",
        "?":"..--..",
        "'":".----.",
        "-":"-....-",
        "/":"-..-.",
        "@":".--.-.",
        "=":"-...-",
        " ":"/"
    }

    decode_morse = dict((morse_char, char) for (char, morse_char) in encode_morse.items())


    # @bot.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def encodemorse(ctx, *, msg:str):

    #     # RE

    #     encoded_message = ""
    #     for char in list(msg.upper()):
    #         encoded_message += encode_morse + " "
    #     await ctx.send(encoded_message)

    # @bot.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def decodemorse(ctx, *, msg:str):
    #     # RE
    #     decoded_message = ""
    #     for char in msg.split():
    #         if char == " ":
    #             continue
    #         decoded_message += decode_morse[char]
    #     await ctx.send(decoded_message)

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def randomnumber(ctx, *, digits:int=1):

        number = ""
        for i in range(digits):
            number += str(random.randint(0, 9))
        embed = discord.Embed(title="Numero random", description=number, colour=color)
        embed.set_footer(text=f"Numero random | {ctx.prefix}help para mas informacion")
        await ctx.send(embed=embed)

    @bot.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roll(ctx, dice_amount: int, sides: int):

        if dice_amount > 999:
            await ctx.send(f"{ctx.message.author.mention}, superaste el límite de la cantidad de dados de 999")
            return
        if sides > 999:
            await ctx.send(f"{ctx.message.author.mention}, superaste el límite del lado de los dados de 999")
            return
        if sides == 1: 
            await ctx.send(f"{ctx.message.author.mention}, No apunta a tirar un dado de 1 cara")



        run_l1 = True
        dice_a1 = dice_amount
        total = 0
        dice_track = []  

        while run_l1:  
            if dice_a1 != 0:
                dice_roll = random.randint(1, sides)  # roll
                print(dice_a1)
                dice_track.append(dice_roll) 
                dice_a1 -= 1
            else:
                run_l1 = False

        for roll_num in dice_track:
            total += roll_num


        try:
            await ctx.send(f"{ctx.message.author.mention} a girado el dado {dice_amount} veces y {sides} caras. "
                        f"Total: {total}")
        except:
            await ctx.send("Soy una computadora que conozco, ¡pero eso es mucho incluso para mí!")

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def md5(ctx, *, msg:str):
        await ctx.send("`{}`".format(hashlib.md5(bytes(msg.encode("utf-8"))).hexdigest()))\


    @bot.command()
    async def pegar(ctx, member: Member, *, reason: str = "ninguna razon"):
        await ctx.send(f"{ctx.author.display_name} a pegado a {member.mention} por {reason}!")


    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sha256(ctx, *, msg:str):
        await ctx.send("`{}`".format(hashlib.sha256(bytes(msg.encode("utf-8"))).hexdigest()))

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sha512(ctx, *, msg:str):
        await ctx.send("`{}`".format(hashlib.sha512(bytes(msg.encode("utf-8"))).hexdigest()))

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uppercase(ctx, *, msg:str):
        await ctx.send(msg.upper())

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lowercase(ctx, *, msg:str):
        await ctx.send(msg.lower())

    @bot.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def fight(ctx, user:str=None, *, weapon:str=None):

        if user is None or user.lower() == ctx.author.mention or user == ctx.author.name.lower() or ctx.guild is not None and ctx.author.nick is not None and user == ctx.author.nick.lower():
            await ctx.send("{} ¡Acabo en un hospital para locos!".format(ctx.author.mention))
            return
        if weapon is None:
            await ctx.send("{0} a intentado combatir contra {1} sin nada asique... {1} lo consigue matar!".format(ctx.author.mention, user))
            return
        await ctx.send("{} a usado un(a) **{}** a **{}** {}".format(ctx.author.mention, weapon, user, random.choice(fight_results).replace("%user%", user).replace("%attacker%", ctx.author.mention)))

    @bot.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def notu(ctx):
        await ctx.message.delete()
        await ctx.send("no tu")

    # @bot.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def fortune(ctx):
    #     await ctx.send("```{}```".format(random.choice(fortunes)))

    # @bot.command()
    # async def owo(ctx, *, text:str):
    #     # RE
    #     print(owofy(text))
    #     await ctx.send(owoify(text))




    @bot.command()
    async def praise(ctx):
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')

    @bot.command()
    async def css(ctx):
        await ctx.send('http://i.imgur.com/TgPKFTz.gif')