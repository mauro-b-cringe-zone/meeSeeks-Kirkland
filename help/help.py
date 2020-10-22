import re, math, random

import discord
from discord.ext import commands
from os import environ as env
import math

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, cog="1"):
        embed = discord.Embed(title="Ayuda con los comandos", color=int(env["COLOR"]))

        cogs = [c for c in self.bot.cogs.key()]
        paginasTotales = math.ceil(len(cogs) / 4)

        cog = int(cog)
        if cog > paginasTotales or cog < 1:
            return await ctx.send("Numero invalido")

def setup(bot):
    bot.add_cog(Help(bot))