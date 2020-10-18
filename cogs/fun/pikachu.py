import discord
from discord.ext import commands
import aiohttp
color = 0x75aef5

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()

async def get_link_from_API(api):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, api)
        await session.close()
        return response["link"]




class Pikachu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pikachu', aliases=['pika'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pikachu(self, ctx):
        embed = discord.Embed(title="Pika Pika.. CHUUUUU", colour=color)
        embed.set_image(url=await get_link_from_API('https://some-random-api.ml/img/pikachu'))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Pikachu(bot))