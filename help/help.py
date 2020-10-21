import re, math, random

import discord
from discord.ext import commands
from os import environ as env
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, cog="1"):
        embed = discord.Embed(color=int(env["COLOR"]))

def setup(bot):
    bot.add_cog(Help(bot))