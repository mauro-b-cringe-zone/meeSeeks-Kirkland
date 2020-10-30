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
                r = await http.get(f"https://mcapi.ca/player/profile/{u}", res_method="json", no_cache=True)
                s = f"https://crafatar.com/renders/body/{u}"
                # print(s)
            except aiohttp.ClientConnectorError:
                return await ctx.send("La API parece estar inactiva...")
            except aiohttp.ContentTypeError:
                return await ctx.send("La API devolvió un error o no devolvió JSON...")

        embed = discord.Embed(colour=color)
        embed.add_field(name="ID:", value=r["id"], inline=False)
        embed.add_field(name="UUID:", value=r["uuid_formatted"], inline=False)
        embed.add_field(name="Nombre en el juego:", value=f'[{r["properties_decoded"]["profileName"]}](https://es.namemc.com/profile/{r["properties_decoded"]["profileName"]})', inline=False)
        embed.add_field(name="Skin:", value=f"[Link para la skin]({s})", inline=False)
        embed.set_thumbnail(url=r['properties_decoded']['textures']['SKIN']['url'])
        embed.set_image(url=s)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Mc(bot))