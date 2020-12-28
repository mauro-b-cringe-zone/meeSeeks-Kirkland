import json

from os import environ as env
from discord.ext import commands
from discord import Message

import discord

from decorators import Decoradores

color = int(env["COLOR"])

class AntiSpam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Se cambia automaticamente y añade un anti espam. EG: !seguridad = Verdadero, !seguridad = Falso")
    @commands.has_permissions(manage_channels=True)
    async def seguridad(self, ctx):
        if ctx.message.guild is None: return
        with open(str(env["JSON_DIR"] + "ext/seguridad.json"), "r") as f:
            guild = json.load(f)

        if not str(ctx.guild.id) in guild:
            guild[str(ctx.guild.id)] = True
            await ctx.send(embed=discord.Embed(title=f"Se ha cambiado el estado a | verdadero", description=f"**¿Qué implica esto?**\n<:list:774983585727119391> No mas de **5** menciones\n<:list:774983585727119391> No mas de **1500** caracteres en un mensage\n<:list:774983585727119391> Nada de palabrotas\n<:list:774983585727119391> Nada de links que comiencen con **discord.gg**", color=color))
        else:
            if guild[str(ctx.guild.id)] is True: 
                guild[str(ctx.guild.id)] = False
                await ctx.send(embed=discord.Embed(title=f"Se ha cambiado el estado a | falso", description=f"**¿Qué implica esto?**\nMaubot ya no se encargara en analizar los mensages del servidor | **{ctx.guild.name}**", color=color))
            elif guild[str(ctx.guild.id)] is False: 
                guild[str(ctx.guild.id)] = True
                await ctx.send(embed=discord.Embed(title=f"Se ha cambiado el estado a | verdadero", description=f"**¿Qué implica esto?**\n<:list:774983585727119391> No mas de **5** menciones\n<:list:774983585727119391> No mas de **1500** caracteres en un mensage\n<:list:774983585727119391> Nada de palabrotas\n<:list:774983585727119391> Nada de links que comiencen con **discord.gg**", color=color))

        with open(str(env["JSON_DIR"] + "ext/seguridad.json"), "w") as f:
            json.dump(guild, f, indent=4)
    

def setup(bot):
    bot.add_cog(AntiSpam(bot))
