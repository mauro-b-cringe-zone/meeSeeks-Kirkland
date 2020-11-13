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
        with open(str(env["JSON_DIR"] + "ext\seguridad.json"), "r") as f:
            guild = json.load(f)

        if not str(ctx.guild.id) in guild:
            guild[str(ctx.guild.id)] = True
        else:
            if guild[str(ctx.guild.id)] is True: guild[str(ctx.guild.id)] = False
            elif guild[str(ctx.guild.id)] is False: guild[str(ctx.guild.id)] = True
        await ctx.send(embed=discord.Embed(title=f"Se ha cambiado el estado a | {guild[str(ctx.guild.id)]}", color=color))

        with open(str(env["JSON_DIR"] + "ext\seguridad.json"), "w") as f:
            json.dump(guild, f, indent=4)
    
    @commands.Cog.listener()
    async def on_message(self, msg: Message):
        ctx = await self.bot.get_context(msg)
        d = await Decoradores().EsEspam(ctx=ctx)
        if d:
            if len(msg.raw_mentions) >= 10:
                await msg.channel.send(embed=discord.Embed(title=f"Demasiado...", description=f"{ctx.author.mention} Este servidor esta en modo antiespam asique no puedes poner **mas de 10** menciones", color=color).set_footer(text="$seguridad | Para desactivarlo"))
                await msg.delete()
        else:
            pass


def setup(bot):
    bot.add_cog(AntiSpam(bot))
