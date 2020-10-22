import random
import discord
import secrets
import asyncio

from discord.ext import commands
from os import environ as env

color = env["COLOR"]


class Contraseñas(commands.Cog):
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

    @commands.command(pass_context=True, description="Adivinare tu contraseña")
    @commands.cooldown(1, 7, commands.BucketType.user)
    async def pass_guess(self, ctx, *, password):
        # print(user_pass)
        if len(list(password)) > 10:
            return await ctx.send("No mas de 10")
        msg = await ctx.send("Porfavor espera esto puede tardar un rato **Sobre todo si las contraseñas son largas**")

        embed = discord.Embed(colour=color)
        embed.title = f"Tu contraseña es {password}"
        embed.add_field(name="Tardanza", value=f"{random.random()} segundos")
        embed.add_field(name="Intentos", value=f"{random.randrange(3, 100000)} intentos")
        await msg.edit(content="", embed=embed)

def setup(bot):
    bot.add_cog(Contraseñas(bot))