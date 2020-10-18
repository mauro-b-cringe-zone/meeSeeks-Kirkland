from discord import User
from discord.ext.commands import MissingRequiredArgument, BadArgument

from discord import Embed
from discord.ext import commands

import random

import aiohttp
color = 0x75aef5

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_random_gif_by_theme(theme: str):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"https://api.tenor.com/v1/random?q={theme.replace(' ', '+')}&contentfilter=medium")
        await session.close()
        return response["results"][random.randint(0, len(response["results"]) - 1)]["media"][0]["gif"]["url"]




class Pat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pat', aliases=["patpat"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(embed=Embed(description=f"(　´Д｀)ﾉ(´･ω･`) **{ctx.author.name}** patpats a **{target.name}**",
                                       colour=color)
                           .set_image(url=f"{await get_random_gif_by_theme('anime pat')}"))
        else: await ctx.send("¿De verdad quieres darte unas palmaditas…? No es un problema, pero ...", delete_after=5.0)



def setup(bot):
    bot.add_cog(Pat(bot))