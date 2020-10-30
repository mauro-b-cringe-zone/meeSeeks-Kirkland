import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re

from io import BytesIO
from discord.ext import commands
from . import http
from os import environ as env
color = int(env["COLOR"])



class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['color'], description="Busca un color con Nombre|Hex|rgb")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def colour(self, ctx, colour: str): 
        async with ctx.channel.typing():

            if colour == "random":
                colour = "%06x" % random.randint(0, 0xFFFFFF)

            if colour[:1] == "#":
                colour = colour[1:]

            if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', colour):
                return await ctx.send("Solo se le permite ingresar a HEX (0-9 & A-F)")

            try:
                r = await http.get(f"https://api.alexflipnote.dev/colour/{colour}", res_method="json", no_cache=True)
            except aiohttp.ClientConnectorError:
                return await ctx.send("La API parece estar inactiva...")
            except aiohttp.ContentTypeError:
                return await ctx.send("La API devolvió un error o no devolvió JSON...")

            embed = discord.Embed(colour=r["int"])
            embed.set_thumbnail(url=r["image"])
            embed.set_image(url=r["image_gradient"])

            embed.add_field(name="HEX", value=r['hex'], inline=True)
            embed.add_field(name="RGB", value=r['rgb'], inline=True)
            embed.add_field(name="Int", value=r['int'], inline=True)
            embed.add_field(name="Brillo", value=r['brightness'], inline=True)

            await ctx.send(embed=embed, content=f"Nombre del color: **{r['name']}**")

def setup(bot):
    bot.add_cog(General(bot))