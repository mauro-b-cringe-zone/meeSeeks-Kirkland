from discord import Embed
from discord.ext import commands
from random import choice
import aiohttp
from os import environ as env
color = int(env["COLOR"])
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_random_anime_quote():
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, "https://anime-chan.herokuapp.com/api/quotes/random")
        await session.close()
        return response[0]["quote"], response[0]["character"], response[0]["anime"]

class AnimeQuote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='animequote', aliases=["aq"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animequote(self, ctx):
        # await safe_delete(ctx)
        q, c, a = await get_random_anime_quote()
        embed = Embed(title="⊹　 ✺ * ·　", description=f"« {q} »\n— {c} - {a}", colour=color).set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AnimeQuote(bot))