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


class Facepalm(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='facepalm', description="Inutil...")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def facepalm(self, ctx):
        await ctx.send(embed=Embed(description=f"(－‸ლ) {ctx.message.author.name}",
                                   color=0x2F3136)
                       .set_image(url=await get_random_gif_by_theme("anime facepalm")))


def setup(bot):
    bot.add_cog(Facepalm(bot))