import re, math, random

import discord
from discord.ext import commands
from os import environ as env
import math

from termcolor import cprint

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Ayuda para los comandos")
    async def help(self, ctx, cog="1"):
        embed = discord.Embed(title="Ayuda con los comandos", color=int(env["COLOR"]))

        cogs = [c for c in self.bot.cogs.keys()]
        paginasTotales = math.ceil(len(cogs) / 4)

        if re.search(r"\d", str(cog)):
            cog = int(cog)
            if cog > paginasTotales or cog < 1:
                return await ctx.send(f"Numero invalido: `{cog}`. Porfavor escoje de {paginasTotales} paginas.\nO tambien lo que puedes hacer es que puedes pone {ctx.prefix}help [categoria]")

            embed.set_footer(
                text=f"<> - Requirido & [] - Opcional | Pagina {cog} de {paginasTotales}"
            )

            CogsNecesitados = []
            for i in range(4):
                x = i + (int(cog) - 1) * 4
                try:
                    CogsNecesitados.append(cogs[x])
                except IndexError as e:
                    cprint(f"[Log] Un error en el commando de ayuda: {e}", 'red')
                
            for cog in CogsNecesitados:
                ListaDeComandos = ""
                for comando in self.bot.get_cog(cog).walk_commands():
                    if comando.hidden:
                        continue

                    ListaDeComandos += f"**{ctx.prefix}{comando.name}** - *{comando.description}*\n"
                ListaDeComandos += "\n"

                embed.add_field(name=f"|---------{cog}---------|\n", value=ListaDeComandos, inline=False)

        elif re.search(r"[a-zA-Z]", str(cog)):
            congMinusculas = [c.lower() for c in cogs]
            if cog.lower() not in congMinusculas:
                return await ctx.send(f"Argumento invalido: `{cog}`. Porfavor escoje de {paginasTotales} paginas.\nO tambien lo que puedes hacer es que puedes pone {ctx.prefix}help [categoria]")

            embed.set_footer(
                text=f"<> - Requirido &  [] - Opcional | Cog {congMinusculas.index(cog.lower())+1} de {len(congMinusculas)}"
            )

            textoDeAyuda = ""

            for comando in self.bot.get_cog(cogs[congMinusculas.index(cog.lower())]).walk_commands():
                if comando.hidden:
                    continue
            
                textoDeAyuda += f"**|-------------- {comando.name} ----------------|** {comando.description}\n"
            
                if len(comando.aliases) > 0:
                    textoDeAyuda += f"**Aliados ----|** {', '.join(comando.aliases)}"
                textoDeAyuda += '\n'
            

                prefijo = ctx.prefix

                textoDeAyuda += f"**Formateo:** `{prefijo}{comando.name} {comando.usage if comando.usage is not None else ''}`\n\n\n"
            embed.description = textoDeAyuda

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))