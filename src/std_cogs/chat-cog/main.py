import discord
from discord.ext import commands
import asyncio

from os import environ as env
import json

color = int(env["COLOR"])

class Eventos():
    def __init__(self, bot):
        self.bot = bot
        self.color_c = 0xc01fe0

    async def cerrar(self, iniciador=None):
        with open("./src/json/chats.json", "r") as f:
            chats = json.load(f)

        if str(iniciador.id) in chats:
            destinatario, us = int(chats[str(iniciador.id)]["dest"]), self.bot.get_user(int(chats[str(iniciador.id)]["dest"]))
            await iniciador.send(embed=discord.Embed(title="El chat esta cerrado", description=f"{iniciador.mention} se ha cerrado la conexion con **{us.mention}**", color=self.color_c))
            await us.send(embed=discord.Embed(title="El chat esta cerrado", description=f"{us.mention}, **{iniciador.mention}** Ha cerrado la conexion con el chat.", color=self.color_c))
            del chats[f"{iniciador.id}"]
            del chats[f"{destinatario}"]

        with open("./src/json/chats.json", "w") as f:
            json.dump(chats, f)

    async def abrir(self, iniciador, destinatario):
        with open("./src/json/chats.json", "r") as f:
            chats = json.load(f)

        if not str(iniciador.id) in chats:
            chats[f"{iniciador.id}"] = {}
            chats[f"{iniciador.id}"]["dest"] = destinatario.id
            chats[f"{destinatario.id}"] = {}
            chats[f"{destinatario.id}"]["dest"] = iniciador.id
        else:
            if chats[f"{iniciador.id}"] == {}:
                return "Usuario ya en chat"

        with open("./src/json/chats.json", "w") as f:
            json.dump(chats, f)

    async def inicio(self, ctx, iniciador=None, dest=None):
        if dest is not None:
            j = await self.abrir(iniciador, dest)
            if j == "Usuario ya en chat":
                return await ctx.send("Ese usuario ya esta en un chat...")
            await iniciador.send(embed=discord.Embed(title="Se ha iniciado un chat", description=f"Hola, {iniciador.mention} se ha creado un chat con **{dest.mention}**",color=color).set_footer(text="Pon 'cerrarchat' para terminar la conversacion"))
            await dest.send(embed=discord.Embed(title="Se ha iniciado un chat", description=f"Hola, {dest.mention} **{iniciador.mention}** ha creado un chat para hablar",color=color).set_footer(text="Pon 'cerrarchat' para terminar la conversacion"))
        else: return await ctx.send("Ese usuario no existe. Creo...")

class ChatApp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases="startchat,start_chat,chat_start,chatstart".split(","), description="Inicia un chat con una persona", usage="<Mencion del usuario>", name="chat")
    async def __start_chat(self, ctx):
        """
        Inicia un chat
        Mas codigo de esto esta en  ./src/eventos-cog/main.py 

        Justo donde pone 'if not message.guild:'

        Tambien la funcion asyncrona de cerrar() 'async def cerrar(iniciador=None, destinatario:int=None):'

            :return  if not str(message.author.id) in chats: No se pueden hacer comandos en los DMs
            :return if not message.content == "cerrarchat": Se cierrran los chats de DM y la funcion de la linea de arriba se ejecuta

        El json esta en ./src/json/chats.json
        """        
        destinatario = ctx.message.mentions[0]

        iniciador = ctx.author
        
        chat = True

        Ev = Eventos(self.bot)

        await Ev.inicio(ctx, iniciador, destinatario)

    @commands.command(aliases="finish_chat,chatfinish".split(","), description="Finaliza un chat con una persona", name="finishchat")
    async def __finish_chat(self, ctx):
        """
        Cerramos el chat con el usuario con el que este conectado y le enviamos que el chat se ha terminado
        """
        Ev = Eventos(self.bot)
        await Ev.cerrar(ctx.author)

def setup(bot):
    bot.add_cog(ChatApp(bot))
