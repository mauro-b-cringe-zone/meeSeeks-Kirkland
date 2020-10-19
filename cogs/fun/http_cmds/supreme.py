  
import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re

from io import BytesIO
from discord.ext import commands
from . import argparser, http


class Supreme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  

    async def api_img_creator(self, ctx, url, filename, content=None):
        async with ctx.channel.typing():
            req = await http.get(url, res_method="read")

            if req is None:
                return await ctx.send("No pude crear la imagen ;-;")

            bio = BytesIO(req)
            bio.seek(0)
            await ctx.send(content=content, file=discord.File(bio, filename=filename))    

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def supreme(self, ctx, *, text: commands.clean_content(fix_channel_mentions=True)):
        """ 
        argumentos:
            --dark | Hace el fondo de color negro
            --light | Hace el fondo de color blanco
        """
        parser = argparser.Arguments()
        parser.add_argument('input', nargs="+", default=None)
        parser.add_argument('-d', '--dark', action='store_true')
        parser.add_argument('-l', '--light', action='store_true')

        args, valid_check = parser.parse_args(text)
        if not valid_check:
            return print("[Log] un error: " + args)

        inputText = urllib.parse.quote(' '.join(args.input))
        if len(inputText) > 75:
            return await ctx.send(f"**{ctx.author.mention}**, la API suprema está limitada a 500 caracteres, lo siento.")

        darkorlight = ""
        if args.dark:
            darkorlight = "dark=true"
        if args.light:
            darkorlight = "light=true"
        if args.dark and args.light:
            return await ctx.send(f"**{ctx.author.name}**, no puede definir ambos --dark y --light, lo siento ..")

        await self.api_img_creator(ctx, f"https://api.alexflipnote.dev/supreme?text={inputText}&{darkorlight}", "supreme.png")

def setup(bot):
    bot.add_cog(Supreme(bot))