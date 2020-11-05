import discord
from discord.ext import commands
import asyncio

from os import environ as env
import json

color = int(env["COLOR"])

class Eventos():
    def __init__(self, bot):
        self.bot = bot
        self.color_c = 0x00fbff

    async def _checkear_usuario_baneado(self, ctx, iniciador, dest):
        with open("./src/json/chats.json", "r") as f:
            chats = json.load(f)

        if str(iniciador.id) in chats["baneos"]:
            if str(dest.id) in chats["baneos"][str(iniciador.id)]:
                return "a"
        if str(dest.id) in chats["baneos"]:
            if dest.id in chats["baneos"][str(dest.id)]:
                return "b"
        else:
            return "c"

        with open("./src/json/chats.json", "w") as f:
            json.dump(chats, f)

    async def cerrar(self, iniciador=None):
        with open("./src/json/chats.json", "r") as f:
            chats = json.load(f)

        if str(iniciador.id) in chats:
            destinatario, us = int(chats["chats"][str(iniciador.id)]["dest"]), self.bot.get_user(int(chats["chats"][str(iniciador.id)]["dest"]))
            await iniciador.send(embed=discord.Embed(title="El chat esta cerrado", description=f"{iniciador.mention} se ha cerrado la conexion con **{us.mention}**", color=self.color_c))
            await us.send(embed=discord.Embed(title="El chat esta cerrado", description=f"{us.mention}, **{iniciador.mention}** Ha cerrado la conexion con el chat.", color=self.color_c))
            del chats["chats"][f"{iniciador.id}"]
            del chats["chats"][f"{destinatario}"]

        with open("./src/json/chats.json", "w") as f:
            json.dump(chats, f)

    async def abrir(self, iniciador, destinatario):
        with open("./src/json/chats.json", "r") as f:
            chats = json.load(f)

        if not str(iniciador.id) in chats:
            chats["chats"][f"{iniciador.id}"] = {}
            chats["chats"][f"{iniciador.id}"]["dest"] = destinatario.id
            chats["chats"][f"{destinatario.id}"] = {}
            chats["chats"][f"{destinatario.id}"]["dest"] = iniciador.id
        else:
            if chats["chats"][f"{iniciador.id}"] == {}:
                return "Usuario ya en chat"

        with open("./src/json/chats.json", "w") as f:
            json.dump(chats, f)

    async def inicio(self, ctx, iniciador=None, dest=None):
        if dest is not None:
            b = await self._checkear_usuario_baneado(ctx, iniciador, dest)
            if b == "a":
                return await ctx.send(embed=discord.Embed(title="Lo has baneado", description=f"{iniciador.mention} ya tienes ha ese usuario baneado. **No** puedes hablar con el", color=self.color_c).set_footer(text="Puedes poner $unbanchat <@usuario> para quitarlo de la lista"))
            elif b == "b":
                return await ctx.send(embed=discord.Embed(title="Te ha baneado", description=f"{iniciador.mention}, **No** puedes hablar con el porque {dest.mention} te tiene baneado", color=self.color_c).set_footer(text="Puedes poner $unbanchat <@usuario> para quitarlo de la lista"))
            elif b == "c":
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
        Ev = Eventos(self.bot)
        await Ev.inicio(ctx, iniciador, destinatario)

    @commands.command(aliases="finish_chat,chatfinish".split(","), description="Finaliza un chat con una persona", name="finishchat")
    async def __finish_chat(self, ctx):
        """
        Cerramos el chat con el usuario con el que este conectado y le enviamos que el chat se ha terminado
        """
        Ev = Eventos(self.bot)
        await Ev.cerrar(ctx.author)

    @commands.command(aliases="banchat,chatban".split(","), description="banea a una persona", name="banfromchat")
    async def __banear_usuario(self, ctx):
        """
        Cerramos el chat con el usuario con el que este conectado y le enviamos que el chat se ha terminado
        """
        destinatario = ctx.message.mentions[0]
        with open("./src/json/chats.json", "r") as f:
            chats = json.load(f)

        if str(ctx.author.id) in chats["baneos"]:
            if str(destinatario.id) in chats["baneos"][str(ctx.author.id)]:
                return await ctx.send(embed=discord.Embed(title="Banear x 2", description=f"{ctx.author.mention}, {destinatario.mention} ya esta baneado en tu lista de baneos.", color=color).set_footer(text="Puedes poner $unbanchat <@usuario> para quitarlo de la lista"))
            chats["baneos"][str(ctx.author.id)][str(destinatario.id)] = destinatario.id
            await ctx.send(embed=discord.Embed(title="Baneado", description=f"Se ha baneadp a {destinatario.mention} de tus chats", color=color))
        else:
            chats["baneos"][str(ctx.author.id)] = {}
            chats["baneos"][str(ctx.author.id)][str(destinatario.id)] = destinatario.id
            await ctx.send(embed=discord.Embed(title="Baneado", description=f"Se ha baneadp a {destinatario.mention} de tus chats", color=color))

        with open("./src/json/chats.json", "w") as f:
            json.dump(chats, f)

    @commands.command(aliases="unbanchat,chatunban".split(","), description="banea a una persona", name="unbanfromchat")
    async def __desbanear_usuario(self, ctx):
        """
        Cerramos el chat con el usuario con el que este conectado y le enviamos que el chat se ha terminado
        """
        Ev = Eventos(self.bot)
        destinatario = ctx.message.mentions[0]
        with open("./src/json/chats.json", "r") as f:
            chats = json.load(f)

        if str(ctx.author.id) in chats["baneos"]:
            if str(destinatario.id) in chats["baneos"][str(ctx.author.id)]: 
                del chats["baneos"][str(ctx.author.id)][str(destinatario.id)]
                if chats["baneos"][str(ctx.author.id)] == {}:
                    del chats["baneos"][str(ctx.author.id)]
                await ctx.send(embed=discord.Embed(title="Desbaneado del chat", description=f"{ctx.author.mention}, se ha desbaneado en tu lista de baneos.", color=color).set_footer(text="Puedes poner $banchat <@usuario> para quitarlo de la lista"))
            else:
                await ctx.send(embed=discord.Embed(title="No lo tienes como baneado", description=f"{ctx.author.mention}, no tienes a este usuario baneado.", color=color).set_footer(text="Puedes poner $banchat <@usuario> para quitarlo de la lista"))
        else:
            return await ctx.send(embed=discord.Embed(title="Not tienes una lista de baneos", description=f"{ctx.author.mention}, No tienes una lista de baneos.", color=color).set_footer(text="Puedes poner $banchat <@usuario> para quitarlo de la lista"))

        with open("./src/json/chats.json", "w") as f:
            json.dump(chats, f)

def setup(bot):
    bot.add_cog(ChatApp(bot))
