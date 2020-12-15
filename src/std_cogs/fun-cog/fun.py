from dataclasses import dataclass

from discord.ext.commands import MissingRequiredArgument, BadArgument
import aiohttp
from discord import Embed
from discord.ext import commands
from os import environ as env
from _io import BytesIO
from gtts import gTTS
import discord
from googletrans import Translator
import requests
color = int(env["COLOR"])

@dataclass
class Meaning:
    Author: int
    Definition: int
    Ref: str

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_link_from_API(api):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, api)
        await session.close()
        return response["link"]

async def search_meaning_of(term: str, sense: int) -> Meaning:
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"http://api.urbandictionary.com/v0/define?term={term}")
        await session.close()
        return Meaning(response["list"][sense]["author"], response["list"][sense]["definition"], response["list"][sense]["permalink"]) if len(response["list"]) > 0 else False

async def get_answer(question: str):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"https://8ball.delegator.com/magic/JSON/{question}")
        await session.close()
        return response["magic"]["answer"]

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['talk','gtts','texttospeech','text-to-speech'], description="Convierte texto ha audio")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tts(self, ctx, *args):
        if len(list(args))==0: 
            return await ctx.send("Introduce algun argumento por ejemplo **123**")
        if len(list(args))>5:
            return await ctx.send("El maximo de el tts es **5**")
        res = BytesIO()
        tts = gTTS(text=' '.join(list(args)), slow=False)
        tts.write_to_fp(res)
        res.seek(0)
        await ctx.send(content="Dale al archivo que pone **tts.mp3** para descargartelo", file=discord.File(fp=res, filename='tts.mp3'))

    @commands.command(description="Pon un comentario en youtube", usage="<Video>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        resp = requests.get(f'https://some-random-api.ml/meme').json()
        embed = discord.Embed(color=0xea9e1a, title=resp["caption"], url=resp["image"])
        embed.set_image(url=resp["image"])
        embed.set_footer(text="ID: " + str(resp["id"]) + ", categoria: " + str(resp["category"]))
        await ctx.send(embed=embed)

    @commands.command(name='urban', description="Busca algo en el diccionario de 'urban'", usage="<palabra>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def urban(self, ctx, term: str):
        terms_mean = await search_meaning_of(term, 0)
        if terms_mean:
            await ctx.send(embed=Embed(description=f"（︶^︶）**{ctx.author.name}** Esto es lo que significa *{term}*",
                                       colour=color)
                           .add_field(name=f"Definido por: __**{terms_mean.Author}**__",
                                      value=f"{terms_mean.Definition}\n[Miralo en Urban dictionary]({terms_mean.Ref})")
                           .set_author(name="Urban Dictionary", icon_url="https://img.icons8.com/color/48/000000/dictionary.png"))     
    
        else: await ctx.send("Es tan vergonzoso... no puedo encontrar esta palabra...", delete_after=5.0)


    @commands.command(name='pikachu', aliases=['pika'], description="Gif'f de pikachu")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pikachu(self, ctx):
        embed = discord.Embed(title="Pika Pika.. CHUUUUU", colour=color)
        embed.set_image(url=await get_link_from_API('https://some-random-api.ml/img/pikachu'))
        await ctx.send(embed=embed)

    @commands.command(description="¿Qué tocaraa...?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ball(self, ctx: commands.Context, *, question: str):
        trans = Translator()
        translated_response = trans.translate(await get_answer(question), src='en', dest='es')
        await ctx.send(f"{ctx.message.author.mention}, ¡{translated_response.text}!")


def setup(bot):
    bot.add_cog(Fun(bot))
