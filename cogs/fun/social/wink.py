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




class Wink(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='wink')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wink(self, ctx, target: User):
        await ctx.send(embed=Embed(description=f"(✿-◡•̀) **{ctx.author.name}** giña a **{target.name}**",
                                    colour=color)
                        .set_image(url=f"{await get_random_gif_by_theme('anime wink')}"))



def setup(bot):
    bot.add_cog(Wink(bot))