import re

import discord
from discord.ext import commands
from . import http
import aiohttp
from os import environ as env
color = int(env["COLOR"])

async def GetUuid(name):
    u = await http.get(f'https://api.minetools.eu/uuid/{name}', res_method="json", no_cache=True)
    return u["id"]

class Mc(commands.Cog):
    @commands.command(description="Informacion de un usuario en minecraft")
    async def mc(self, ctx: commands.Context, *, user: str):

        async with ctx.channel.typing():

            try:
                u = await GetUuid(user)
                r = await http.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{u}", res_method="json", no_cache=True)
                s = f"https://crafatar.com/renders/body/{u}" + ".png"
            except aiohttp.ClientConnectorError:
                return await ctx.send("La API parece estar inactiva...")
            except aiohttp.ContentTypeError:
                return await ctx.send("La API devolvió un error o no devolvió JSON...")

        embed = discord.Embed(colour=color)
        embed.set_author(icon_url="https://idescargar.com/wp-content/uploads/2017/07/descargar-minecraft-pocket-edition.png", name=ctx.author.name)
        embed.add_field(name="Nombre en el juego:", value=f'[{r["name"]}](https://es.namemc.com/profile/{r["name"]})', inline=True)
        embed.add_field(name="Skin:", value=f"[Link para la skin]({s})", inline=True)
        embed.add_field(name="ID:", value=r["id"], inline=False)
        embed.set_thumbnail(url=s)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Mc(bot))
