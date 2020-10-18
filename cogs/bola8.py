import aiohttp
from discord.ext.commands import MissingRequiredArgument, BadArgument, MissingPermissions, BotMissingPermissions
from discord.ext import commands
from discord import Embed, Member
from datetime import date
from googletrans import Translator


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


async def get_answer(question: str):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"https://8ball.delegator.com/magic/JSON/{question}")
        await session.close()
        return response["magic"]["answer"]

class Ball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ball(self, ctx, *, question: str):
        trans = Translator()
        translated_response = trans.translate(await get_answer(question), src='en', dest='es')
        await ctx.send(f"{ctx.message.author.mention}, ¡{translated_response.text}!")


def setup(bot):
    bot.add_cog(Ball(bot))