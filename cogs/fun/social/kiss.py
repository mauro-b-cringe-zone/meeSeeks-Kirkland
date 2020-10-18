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




class Kiss(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kiss', aliases=['smack'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, target: User):
        if ctx.message.author != target:
            await ctx.send(embed=Embed(description=f"(✿˘ω˘)˘ε˘˶ ) **{ctx.author.name}** a besado a **{target.name}**",
                                       color=0x2F3136)
                           .set_image(url=f"{await get_random_gif_by_theme('anime kiss')}"))
        else: await ctx.send("Tu no quieres hacer esto solo ¿no?.. ?", delete_after=5.0)



def setup(bot):
    bot.add_cog(Kiss(bot))