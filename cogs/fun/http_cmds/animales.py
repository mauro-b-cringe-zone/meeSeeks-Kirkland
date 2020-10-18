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
color = 0x75aef5
class Animales(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def randomimageapi(self, ctx, url, endpoint):
        try:
            r = await http.get(url, res_method="json", no_cache=True)
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")
            
        embed = discord.Embed(colour=color)
        embed.set_image(url=r[endpoint])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx):
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/cats', 'file')

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def dog(self, ctx):
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/dogs', 'file')

    @commands.command(aliases=["bird"])
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def birb(self, ctx):
        await self.randomimageapi(ctx, 'https://api.alexflipnote.dev/birb', 'file')

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx):
        await self.randomimageapi(ctx, 'https://random-d.uk/api/v1/random', 'url')

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def coffee(self, ctx):
        await self.randomimageapi(ctx, 'https://coffee.alexflipnote.dev/random.json', 'file')




def setup(bot):
    bot.add_cog(Animales(bot))