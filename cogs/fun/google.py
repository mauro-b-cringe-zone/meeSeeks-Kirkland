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

    @commands.command(description="Busca algo en google")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gl(self, ctx, *, query):

        def gsync(query=query):
            name = str(ctx.message.author)
            for j in search(query, tld="com", num=1, stop=1):
                return j

        async with ctx.typing():
            gasync = await self.bot.loop.run_in_executor(ThreadPoolExecutor(), gsync)
            await ctx.send(gasync)


    @commands.command(description="Busca algo en google")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, ctx, *, term: str):
        embed= discord.Embed(title="Busqueda de google", url=f"https://lmgtfy.com/?q={term.replace(' ', '+')}", colour=color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Google(bot))