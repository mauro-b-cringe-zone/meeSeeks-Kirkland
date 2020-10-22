from discord import Embed
from discord.ext import commands

import random

import aiohttp
from os import environ as env
color = int(env["COLOR"])

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_random_gif_by_theme(theme: str):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"https://api.tenor.com/v1/random?q={theme.replace(' ', '+')}&contentfilter=medium")
        await session.close()
        return response["results"][random.randint(0, len(response["results"]) - 1)]["media"][0]["gif"]["url"]




class Dormir(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='sleep', description="Duermete niño... duermete ya...")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sleep(self, ctx):
        await ctx.send(embed=Embed(description=f"[(－－)]..zzZ **{ctx.author.name}** esta durmiendo...",
                                   colour=color)
                       .set_image(url=f"{await get_random_gif_by_theme('anime sleeping')}"))


def setup(bot):
    bot.add_cog(Dormir(bot))