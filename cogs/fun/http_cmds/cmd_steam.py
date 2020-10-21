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

    @commands.command(aliases=['steam_profile'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def steam(self, ctx, user: str): 
        async with ctx.channel.typing():

            try:
                r = await http.get(f"https://api.alexflipnote.dev/steam/user/{user}", res_method="json", no_cache=True)
            except aiohttp.ClientConnectorError:
                return await ctx.send("La API parece estar inactiva...")
            except aiohttp.ContentTypeError:
                return await ctx.send("La API devolvió un error o no devolvió JSON...")

            embed = discord.Embed(colour=color)
            embed.set_thumbnail(url=r["avatars"]["avatarmedium"])

            embed.add_field(name="Nombre de usuario", value=r["profile"]["username"], inline=True)
            embed.add_field(name="url", value=f'[URL]({r["profile"]["url"]})', inline=True)
            embed.add_field(name="ID", value=r["id"]["steamid64"], inline=False)
            embed.add_field(name="Nomre real", value=r["profile"]["realname"], inline=False)

            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))