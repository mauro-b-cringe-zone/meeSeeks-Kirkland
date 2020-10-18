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
from requests import get as decodeurl
from PIL import Image, ImageFont, ImageDraw, GifImagePlugin, ImageOps, ImageFilter
from io import BytesIO
from datetime import datetime as t
color = 0x75aef5

class Google(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def google(self, ctx, *, term: str):
        embed= discord.Embed(title="Busqueda de google", url=f"https://lmgtfy.com/?q={term.replace(' ', '+')}", colour=color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Google(bot))