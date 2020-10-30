import aiohttp
from discord import User, Message, File
from discord.ext.commands import BadArgument, MissingRequiredArgument

from discord.ext import commands
from numpy import format_parser
import typing
from distutils import util
import io
import json
import os
import functools
from discord.ext import commands
from random import randint
from io import BytesIO
import discord
import urllib
from os import environ as env
color = int(env["COLOR"])

async def fetch_media(session, url):
    async with session.get(url) as response:
        return io.BytesIO(await response.read())


async def trigger_pic(pic: str):
    async with aiohttp.ClientSession() as session:
        triggered = await fetch_media(session, f"https://some-random-api.ml/canvas/triggered?avatar={pic}")
        await session.close()
        return triggered


async def gray_scale_pic(pic: str):
    async with aiohttp.ClientSession() as session:
        gray_scale = await fetch_media(session, f"https://some-random-api.ml/canvas/greyscale?avatar={pic}")
        await session.close()
        return gray_scale


async def glass_pic(pic: str):
    async with aiohttp.ClientSession() as session:
        glass = await fetch_media(session, f"https://some-random-api.ml/canvas/glass?avatar={pic}")
        await session.close()
        return glass

async def sepia_pic(pic: str):
    async with aiohttp.ClientSession() as session:
        sepia = await fetch_media(session, f"https://some-random-api.ml/canvas/sepia?avatar={pic}")
        await session.close()
        return sepia

async def gay_pic(pic: str):
    async with aiohttp.ClientSession() as session:
        gay = await fetch_media(session, f"https://some-random-api.ml/canvas/gay?avatar={pic}")
        await session.close()
        return gay

async def invert_pic(pic: str):
    async with aiohttp.ClientSession() as session:
        invert = await fetch_media(session, f"https://some-random-api.ml/canvas/invert?avatar={pic}")
        await session.close()
        return invert

class Trigger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='trigger', description="TRIGERRRRR", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trigger(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(file=File(await trigger_pic(str(target.avatar_url_as(static_format='png'))),
                           f"trigger_{target}.gif"))
        else:
            await ctx.send(file=File(await trigger_pic(str(ctx.message.author.avatar_url_as(static_format='png'))),
                           f"trigger_{ctx.message.author}.gif"))

    @commands.command(description="Pon ha alguien gris", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gray(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(file=File(await gray_scale_pic(str(target.avatar_url_as(static_format='png'))),
                           f"gray_scale_{target}.gif"))
        else:
            await ctx.send(file=File(await gray_scale_pic(str(ctx.message.author.avatar_url_as(static_format='png'))),
                           f"gray_scale_{ctx.message.author}.gif"))

    @commands.command(description="Pinchas jaja lol", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glass(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(file=File(await glass_pic(str(target.avatar_url_as(static_format='png'))),
                           f"glass_{target}.gif"))
        else:
            await ctx.send(file=File(await glass_pic(str(ctx.message.author.avatar_url_as(static_format='png'))),
                           f"glass_{ctx.message.author}.gif"))

    @commands.command(description="Convierte un usuario en sepia", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sepia(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(file=File(await sepia_pic(str(target.avatar_url_as(static_format='png'))),
                           f"sepia_{target}.gif"))
        else:
            await ctx.send(file=File(await sepia_pic(str(ctx.message.author.avatar_url_as(static_format='png'))),
                           f"sepia_{ctx.message.author}.gif"))

    @commands.command(description=".....................", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(file=File(await gay_pic(str(target.avatar_url_as(static_format='png'))),
                           f"gay_{target}.gif"))
        else:
            await ctx.send(file=File(await gay_pic(str(ctx.message.author.avatar_url_as(static_format='png'))),
                           f"gay_{ctx.message.author}.gif"))

    @commands.command(description="Invierte los colores del usuario", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invert(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(file=File(await invert_pic(str(target.avatar_url_as(static_format='png'))),
                           f"invert_{target}.gif"))
        else:
            await ctx.send(file=File(await invert_pic(str(ctx.message.author.avatar_url_as(static_format='png'))),
            f"invert_{ctx.message.author}.gif"))


    @commands.command(aliases=['truthscroll', 'truth-scroll'], description="Una legenda dijo", usage="[texto]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def scroll(self, ctx, *, text):
        text = urllib.parse.quote(text)
        # await ctx.send(f'https://api.alexflipnote.dev/scroll?text={text}') 
        embed = discord.Embed(colour=color)
        embed.set_image(url=f'https://api.alexflipnote.dev/scroll?text={text}')
        await ctx.send(embed=embed)

    @commands.command(description="Interesante...", usage="[texto]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def facts(self, ctx, *, text):
        text = urllib.parse.quote(text)
        # await ctx.send(f'https://api.alexflipnote.dev/facts?text={text}')
        embed = discord.Embed(colour=color)
        embed.set_image(url=f'https://api.alexflipnote.dev/facts?text={text}')
        await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(Trigger(bot))