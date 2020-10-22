from dataclasses import dataclass

import aiohttp
from discord.ext.commands import MissingRequiredArgument, BadArgument, CommandOnCooldown
from discord.ext import commands
from discord import Embed

from os import environ as env
color = int(env["COLOR"])

@dataclass
class AnimeInfo:
    Title: str
    Type: str
    Episodes: str
    Airing: bool
    Score: float
    Synopsis: str
    Image_URL: str
    URL: str

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()
 
async def get_anime_info_by_name(name: str) -> AnimeInfo:
    async with aiohttp.ClientSession() as session:
        response = await fetch(session,
                               f"https://api.jikan.moe/v3/search/anime?q={name}")
        await session.close()
        return AnimeInfo(response["results"][0]["title"],
                         response["results"][0]["type"],
                         response["results"][0]["episodes"],
                         response["results"][0]["airing"],
                         response["results"][0]["score"],
                         response["results"][0]["synopsis"] if len(response["results"][0]["synopsis"]) < 516 else f"{response['results'][0]['synopsis'][:516]}..",
                         response["results"][0]["image_url"],
                         response["results"][0]["url"]
                         ) if len(response["results"]) > 0 else False


# Know more about anime
class Anime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime', aliases=['animeinfo', 'ai', 'mal', 'myanimelist'], description="Mira informacion sobre el anime")
    @commands.cooldown(1, 3)
    async def anime(self, ctx, *, term: str):
        query = await get_anime_info_by_name(term)
        if query:
            await ctx.send(embed=Embed(colour=color, title=f"Información de anime para - ( {query.Title} ) - {query.Type}", description=f"ᕙ(⇀‸↼‵‵)ᕗ  **{ctx.author.mention}**¡He descubierto tu anime!")
                           .set_thumbnail(url=query.Image_URL)
                           .add_field(name="**Informacion**", value=f"Puntiacion MAL: **{query.Score}**\nEpisodes: **{query.Episodes}**\nVentilación: **{'Si' if query.Airing else 'No'}**", inline=False)
                           .add_field(name=f"**Synopsis**", value=f"{query.Synopsis}\n[Miralo en MAL]({query.URL})"))
        else: await ctx.send("Es tan vergonzoso ... No puedo encontrar este anime ...", delete_after=5.0)



def setup(bot):
    bot.add_cog(Anime(bot))