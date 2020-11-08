import aiohttp
from discord.ext.commands import MissingRequiredArgument, BadArgument, MissingPermissions, BotMissingPermissions
from discord.ext import commands
from discord import Embed, Member
from datetime import date
from googletrans import Translator


import random

import aiohttp
from os import environ as env
color = int(env["COLOR"])

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_answer(question: str):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, f"https://8ball.delegator.com/magic/JSON/{question}")
        await session.close()
        return response["magic"]["answer"]

class Ball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="¿Qué tocaraa...?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ball(self, ctx: commands.Context, *, question: str):
        trans = Translator()
        translated_response = trans.translate(await get_answer(question), src='en', dest='es')
        await ctx.send(f"{ctx.message.author.mention}, ¡{translated_response.text}!")


def setup(bot):
    bot.add_cog(Ball(bot))