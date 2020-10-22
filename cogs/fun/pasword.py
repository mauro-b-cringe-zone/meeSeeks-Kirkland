import random
import discord
import urllib
import secrets
import asyncio
import aiohttp
import re

from io import BytesIO
from discord.ext import commands


class Password(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Te enviare una contraseña (CON LA LONGUITUD QUE TU QUIERAS)")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def password(self, ctx, nbytes: int = 18):
        if nbytes not in range(3, 1401):
            return await ctx.send("Solo acepto numeros entre 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"Creando y enviando tu contraseña **{ctx.author.mention}**")
        await ctx.author.send(f"🎁 **Aqui esta tu contraseña:**\n{secrets.token_urlsafe(nbytes)}")


def setup(bot):
    bot.add_cog(Password(bot))