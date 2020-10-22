from dataclasses import dataclass

from discord.ext.commands import MissingRequiredArgument, BadArgument
import aiohttp
from discord import Embed
from discord.ext import commands
from os import environ as env
color = int(env["COLOR"])

@dataclass
class Meaning:
    Author: int
    Definition: int
    Ref: str

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def search_meaning_of(term: str, sense: int) -> Meaning:
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"http://api.urbandictionary.com/v0/define?term={term}")
        await session.close()
        return Meaning(response["list"][sense]["author"], response["list"][sense]["definition"], response["list"][sense]["permalink"]) if len(response["list"]) > 0 else False


# More knowledge
class Urban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='urban', description="Busca algo en el diccionario de 'urban'")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def urban(self, ctx, term: str):
        terms_mean = await search_meaning_of(term, 0)
        if terms_mean:
            await ctx.send(embed=Embed(description=f"（︶^︶）**{ctx.author.name}** Esto es lo que significa *{term}*",
                                       colour=color)
                           .add_field(name=f"Definido por: __**{terms_mean.Author}**__",
                                      value=f"{terms_mean.Definition}\n[Miralo en Urban dictionary]({terms_mean.Ref})")
                           .set_author(name="Urban Dictionary", icon_url="https://img.icons8.com/color/48/000000/dictionary.png")
                           .set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png"))     
    
        else: await ctx.send("Es tan vergonzoso... no puedo encontrar esta palabra...", delete_after=5.0)



def setup(bot):
    bot.add_cog(Urban(bot))