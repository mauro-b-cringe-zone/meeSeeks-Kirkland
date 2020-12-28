from discord.ext.commands import MissingRequiredArgument, BadArgument
from discord.ext import commands
import discord
import random
import base64
from os import getenv
from subprocess import run, PIPE
from json import dumps
from urllib.request import urlopen as getapi
from urllib.parse import quote_plus as urlencode
from json import loads as jsonify
from requests import request
from googlesearch import search
from concurrent.futures import ThreadPoolExecutor

from os import environ as env
color = int(env["COLOR"])

class Google(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Busca algo en google", usage="<Busqueda>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, ctx, *, query):

        def gsync(query=query):
            lista = ""
            for i, j in enumerate(search(query)):
                lista += str(j) + "\n"
                if i == 4:
                    break
            return lista

        async with ctx.typing():
            # gasync = await self.bot.loop.run_in_executor(ThreadPoolExecutor(), gsync)
            await ctx.send(embed=discord.Embed(description=gsync(), color=color).set_author(name="Busquedas de google", icon_url="https://www.shareicon.net/data/512x512/2015/10/04/111650_google-icon_512x512.png"))


    @commands.command(description="Busca algo en lmgtfy con una animacion", usage="<Busqueda>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lmgtfy(self, ctx, *, term: str):
        embed= discord.Embed(description=f"[Aqui](https://lmgtfy.com/?q={term.replace(' ', '+')}) tienes tu busqueda de google", colour=color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Google(bot))
