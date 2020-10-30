import aiohttp
from discord import User, Message, File
from discord.ext.commands import BadArgument, MissingRequiredArgument

from discord.ext import commands
from numpy import format_parser

from distutils import util
import io
import json
import os
from discord.ext import commands
import random

from os import environ as env
color = int(env["COLOR"])

async def fetch_media(session, url):
    async with session.get(url) as response:
        return io.BytesIO(await response.read())


async def wasted_pic(pic: str):
    async with aiohttp.ClientSession() as session:
        wasted = await fetch_media(session, f"https://some-random-api.ml/canvas/wasted?avatar={pic}")
        await session.close()
        return wasted

class Wasted(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wasted', description="Bruhh...")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wasted(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(file=File(await wasted_pic(str(target.avatar_url_as(static_format='png'))),
                           f"wasted_{target}.gif"))
        else:
            await ctx.send(file=File(await wasted_pic(str(ctx.message.author.avatar_url_as(static_format='png'))),
                           f"wasted_{ctx.message.author}.gif"))


def setup(bot):
    bot.add_cog(Wasted(bot))

