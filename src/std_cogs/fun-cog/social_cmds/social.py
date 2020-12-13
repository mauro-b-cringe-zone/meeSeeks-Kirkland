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

import aiohttp, discord
from discord import User
from discord.ext.commands import MissingRequiredArgument, BadArgument

from discord import Embed
from discord.ext import commands
import asyncio

from utils.hack import hackflow

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_random_gif_by_theme(theme: str):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"https://api.tenor.com/v1/random?q={theme.replace(' ', '+')}&contentfilter=medium")
        await session.close()
        return response["results"][random.randint(0, len(response["results"]) - 1)]["media"][0]["gif"]["url"]


async def fetch_media(session, url):
    async with session.get(url) as response:
        return io.BytesIO(await response.read())


async def wasted_pic(pic: str):
    async with aiohttp.ClientSession() as session:
        wasted = await fetch_media(session, f"https://some-random-api.ml/canvas/wasted?avatar={pic}")
        await session.close()
        return wasted

class Social(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Hackea ha alguien", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hack(self, ctx, *args):
        foundArgs, tohack = False, None
        try:
            tohack = ctx.guild.get_member(int(list(args)[0]))
            assert tohack!=None
            foundArgs = True
        except: 
            pass
        if len(ctx.message.mentions)<1 and not foundArgs:
            await ctx.send(f'Porfavor pon a alguien!\nejemplo: {ctx.prefix}hack <@'+str(ctx.message.author.id)+'>')
        if tohack==None: 
            tohack = ctx.message.mentions[0]
        console = 'maubot@HACKERMAN:/$ '
        if len(ctx.message.mentions)>0 or foundArgs:
            main = await ctx.send('Abriendo consola...\n```bash\nCargando...```')
            flow = hackflow(tohack)
            for i in range(0, len(flow)):
                console = console + flow[i][1:]
                await main.edit(content=f"```bash\n{console}```")
                await asyncio.sleep(random.randint(5, 6))
        else:
            console += 'ERROR: TAG INVALIDP.\nACCESO DENEGADO.\n\nCódigo cifrado en base64 con codificación hash:\n'+bin(ctx.message.author.name)+ '\n' + console
            await ctx.send(f'```bash\n{console}```')


                               
    @commands.command(name='wasted', description="Bruhh...")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wasted(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(file=File(await wasted_pic(str(target.avatar_url_as(static_format='png'))),
                           f"wasted_{target}.gif"))
        else:
            await ctx.send(file=File(await wasted_pic(str(ctx.message.author.avatar_url_as(static_format='png'))),
                           f"wasted_{ctx.message.author}.gif"))

    @commands.command(name='wink', description=";v")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wink(self, ctx, target: User):
        await ctx.send(embed=Embed(description=f"(✿-◡•̀) **{ctx.author.name}** giña a **{target.name}**",
                                    colour=color)
                        .set_image(url=f"{await get_random_gif_by_theme('anime wink')}"))

    @commands.command(name='sleep', description="Duermete niño... duermete ya...")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sleep(self, ctx):
        await ctx.send(embed=Embed(description=f"[(－－)]..zzZ **{ctx.author.name}** esta durmiendo...",
                                   colour=color)
                       .set_image(url=f"{await get_random_gif_by_theme('anime sleeping')}"))

    @commands.command(name='shrug', description="¿Y yo que se?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shrug(self, ctx):
        await ctx.send(embed=Embed(description=f"¯\_( ツ )_/¯ **{ctx.author.name}** shrugs",
                                   color=color)
                       .set_image(url=f"{await get_random_gif_by_theme('anime shrug')}"))

    @commands.command(name='pout', description="Gritale ha alguien")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pout(self, ctx):
        await ctx.send(embed=Embed(description=f"(￣ε(#￣) **{ctx.author.name}** poutea !",
                                   color=color)
                       .set_image(url=f"{await get_random_gif_by_theme('anime pout')}"))

    @commands.command(name='pat', aliases=["patpat"], description="Dale una palmada a alguien")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(embed=Embed(description=f"(　´Д｀)ﾉ(´･ω･`) **{ctx.author.name}** patpats a **{target.name}**",
                                       colour=color)
                           .set_image(url=f"{await get_random_gif_by_theme('anime pat')}"))
        else: await ctx.send("¿De verdad quieres darte unas palmaditas…? No es un problema, pero ...", delete_after=5.0)

    @commands.command(description="TE ODIOO @usuario")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuke(self, ctx, target: discord.Member):
        await ctx.send(embed=discord.Embed(description=f"**{ctx.author.name}** a lanzado una bomba nuclear contra **{target.name}**  💔",
                                    colour=color)
                        .set_image(url="https://db.manx7.net/assets/m7/nukes/2.gif"))

    @commands.command(name='kiss', aliases=['smack'], description="Un besito...")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(embed=Embed(description=f"(✿˘ω˘)˘ε˘˶ ) **{ctx.author.name}** a besado a **{target.name}**",
                                       color=0x2F3136)
                           .set_image(url=f"{await get_random_gif_by_theme('anime kiss')}"))
        else: await ctx.send("Tu no quieres hacer esto solo ¿no?.. ?", delete_after=5.0)

    @commands.command(name='facepalm', description="Inutil...")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def facepalm(self, ctx):
        await ctx.send(embed=Embed(description=f"(－‸ლ) {ctx.message.author.name}",
                                   color=0x2F3136)
                       .set_image(url=await get_random_gif_by_theme("anime facepalm")))

    @commands.command(name='cry', description="LLora")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cry(self, ctx):
        await ctx.send(embed=Embed(description=f"｡:ﾟ(;´∩`;)ﾟ:｡ **{ctx.author.name}** llora...",
                                   color=color)
                       .set_image(url=f"{await get_random_gif_by_theme('anime cry')}"))
                         


def setup(bot):
    bot.add_cog(Social(bot))

