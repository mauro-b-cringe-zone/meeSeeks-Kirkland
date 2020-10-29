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
from discord import Member, activity, message
from discord.utils import find
from mauutils.mauunicode import *
from mauutils.secrete import *
from mauutils.fun.lists import *
from mauutils.hack import *
from googletrans import Translator
import sys
import datetime
import discord
import random
import aiohttp
import asyncio
import json
import time
import re
import os
from termcolor import cprint

def get_prefix(bot, message):
    with open('./json/prefix.json', 'r') as f:
        prefixes = json.load(f)
    base = [prefixes[str(message.guild.id)], '?', '!', 'm.']
    return base

bot = commands.Bot(command_prefix = get_prefix, description="Maubot | El mejor bot para divertirse")

bot.remove_command('help')


def main():
    

    @bot.event
    async def on_ready():

        cprint("""
             __    __     ______     __  __     ______     ______     ______  
            /\ "-./  \   /\  __ \   /\ \/\ \   /\  == \   /\  __ \   /\__  _\ 
            \ \ \-./\ \  \ \  __ \  \ \ \_\ \  \ \  __<   \ \ \/\ \  \/_/\ \/ 
             \ \_\ \ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_____\    \ \_\ 
              \/_/  \/_/   \/_/\/_/   \/_____/   \/_____/   \/_____/     \/_/                                                             
        """, 'blue')

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

        cprint(f"\nTOKEN:  {TOKEN}\n", 'blue')

        print("\n------------------------------------->\n"
            f"COGS\n"
            f"Secrete.py a reyenado al token y los colores\n")
        
        cprint("-----------------------> [LOG]\n", 'red')

        

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
            **El prefijo del comando es: `$`, `!`, `?`, `m.`**\n\n
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


    @bot.command(description="Verifica que eres humano")
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

    @bot.command(description="Mira las reglas del server")
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



    @bot.command(description="Cambia el prefijo")
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

    @bot.command(description="Mira la info del bot o la config ($_bot info | $_bot config)")
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


    @bot.command(aliases=['permisos_visu'], description="Mira los permisos de alguien")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def permisos(ctx, *, member: discord.Member=None):

        if not member:
            member = ctx.author



        perms = ',\n'.join(perm for perm, value in member.guild_permissions if value)
        trans = Translator()
        embed = discord.Embed(title=f'Los permisos de {member} son:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        translated_perms = trans.translate(perms, src="en", dest="es")
        embed.add_field(name='\uFEFF', value=translated_perms.text)

        await ctx.send(content=None, embed=embed)

    @bot.command(description="Haz una reseña a el robot")
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


    @bot.command(description="Mira la info de un usuario")
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


    @bot.command(description="Hola 👏 Gente 👏 ¿Què 👏 Tal 👏 ?")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def palmadas(ctx, *, message):
        msg = message.replace(" ", " 👏 ")

        await ctx.send(msg)


    @bot.command(description="Mira el avatar de alguien")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(ctx, member: discord.Member = None):
        member = ctx.author if member == None else member
        embed = discord.Embed(title=f"**Avatar de -- ({member})**", description=f"[Link]({member.avatar_url})",colour=color)
        embed.set_image(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)

    @bot.command(description="Mira el token del bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def token(ctx):
        embed = discord.Embed(title="".join([random.choice(list('abcdefghijklmnopqrstuvwxyz._=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.')) for i in range(59)]), colour=color)
        await ctx.send(embed=embed)

    @bot.command(asliases=['link', 'links'], description="Los links del bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def links(ctx):

        embed = discord.Embed(description=f"**Link para el bot:** [Mi link](https://discord.com/oauth2/authorize?client_id=730124969132163093&permissions=8&scope=bot)\n**Server**: (https://discord.gg/4gfUZtB)\n**Web**: [Link](http://maubot.mooo.com/maubot/)\n**Github**: [linky](https://github.com/maubg-debug/maubot)\n**Github del creador**: [link Github](https://github.com/maubg-debug/)", colour=color)
        embed.set_author(name="INVITACIONES", icon_url="https://img.icons8.com/color/48/000000/share.png")
        embed.set_image(url="https://top.gg/api/widget/730124969132163093svg?usernamecolor=FFFFFF&topcolor=000000")
        # embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")
        await ctx.send(embed=embed)

    @bot.command(description="Invitacion")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(ctx):

        embed = discord.Embed(description=f"**https://discord.com/oauth2/authorize?client_id=730124969132163093&permissions=8&scope=bot**", colour=color)
        await ctx.send(embed=embed)

    @bot.command(description="¿Quien es el jefe del servidor?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def owner(ctx):

        embed = discord.Embed(title="👑 Owner del servidor", colour=color)
        embed.add_field(name=f"El owner de __{ctx.guild.name}__ es:", value=f"\n👑 **{ctx.guild.owner}**", inline=False)
        embed.set_thumbnail(url=f"{ctx.guild.owner.avatar_url}")
        embed.set_footer(text=f"Puesto por | {ctx.author}")
        embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")
        await ctx.send(embed=embed)


if __name__ == "__main__":
    cprint("[ESTUPIDO] Ve a launcher.py", 'red')