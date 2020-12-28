
from urllib.parse import quote_plus as urlencode
import discord
import requests
from googletrans import Translator

from discord import Message

from decorators import Decoradores
from os import environ as env

color = int(env["COLOR"])
trans = Translator()

async def Chequeo(texto: str):
    texto = urlencode(texto).replace('+', '%20')
    profanidad = requests.get(f"https://profanity.totallyusefulapi.ml/{texto}").json()
    if profanidad["profanity"] == True:
        return profanidad
    return False

async def Seguridad(bot, msg: Message):
    ctx = await bot.get_context(msg)
    d = await Decoradores().EsEspam(ctx=ctx)
    if d:
        chequeo = await Chequeo(trans.translate(msg.content, dest='en').text)
        if chequeo:
            await msg.delete()
            embed = discord.Embed(title="Se ha detectado una palabrota", color=color)
            embed.set_footer(text="m.seguridad | Para desactivarlo")
            embed.add_field(name="Frase (En español)", value=trans.translate(chequeo["censored"], dest='es').text.replace("*", "\*"))
            await ctx.send(embed=embed)
            return True
        if "discord.gg/" in msg.content:
            await msg.delete()
            await ctx.send("No puedes poner invitaciones")
            return True
        if len(msg.raw_mentions) >= 5:
            await msg.channel.send(embed=discord.Embed(title=f"Demasiado...", description=f"{ctx.author.mention} Este servidor esta en modo antiespam asique no puedes poner **mas de 5** menciones", color=color).set_footer(text="m.seguridad | Para desactivarlo"), delete_after=30.0)
            await msg.delete()
            return True
        if len(msg.content) >= 1400:
            await msg.channel.send(embed=discord.Embed(title=f"Demasiado...", description=f"{ctx.author.mention} Este servidor esta en modo antiespam asique no puedes poner **mas de 1500** caracteres", color=color).set_footer(text="m.seguridad | Para desactivarlo"), delete_after=30.0)
            await msg.delete()
            return True
        return False
