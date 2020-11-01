import re, math, random

import discord
from discord.ext import commands
from os import environ as env
import math

from termcolor import cprint
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ayuda(self, ctx, cog, cogs, paginasTotales, embed):
        cog = int(cog)
        if cog > paginasTotales or cog < 1:
            return await ctx.send(f"Numero invalido: `{cog}`. Porfavor escoje de {paginasTotales} paginas.\nO tambien lo que puedes hacer es que puedes pone {ctx.prefix}help [categoria]")

        embed.set_footer(
            text=f"Puedes poner @Maubot#6247 para mas info | Pagina {cog} de {paginasTotales}"
        )

        CogsNecesitados = []
        for i in range(6):
            x = i + (int(cog) - 1) * 6
            try:
                CogsNecesitados.append(cogs[x])
            except IndexError as e:
                cprint(f"[Log] Un error en el commando de ayuda: {e}", 'red')
            
        for cog in CogsNecesitados:
            ListaDeComandos = ""
            for comando in self.bot.get_cog(cog).walk_commands():
        
                if comando.hidden:
                    continue

                ListaDeComandos += f"`{ctx.prefix}{comando.name}`, "
            ListaDeComandos = ListaDeComandos[:-2]
            ListaDeComandos += "\n"
            embed.add_field(name=f"║━━━━ {cog} ━━━━║\n", value=ListaDeComandos, inline=False)
        return embed

        cprint(f"[Log] caracteres de 'help':  {len(ListaDeComandos)}", 'yellow')

    @commands.command(description="Ayuda para los comandos", usage="[cog]")
    async def help(self, ctx, cog="1"):
        try:
            embed = discord.Embed(title="Ayuda con los comandos", color=int(env["COLOR"]))

            cogs = [c for c in self.bot.cogs.keys()]
            cprint(f"[Log] Cogs: {len(cogs)}", 'yellow')
            paginasTotales = math.ceil(len(cogs) / 6)

            if re.search(r"\d", str(cog)):

                embedh = await self.ayuda(ctx, cog, cogs, paginasTotales, embed)

                msg = await ctx.send(embed=embedh)
                # emos = ["◀️", "▶️", "❌"]
                # def _check(reaction, user):
                #     return (
                #         reaction.emoji in emos
                #         and user == ctx.author
                #         and reaction.message.id == msg.id
                #     )
                # for n in range(50):
                #     for i in ["◀️", "▶️", "❌"]:
                #         await msg.add_reaction(i)                    
                #     try:
                #         reaction, user = await self.bot.wait_for("reaction_add", check=_check)
                #     except Exception as e:
                #         cprint(f"[Log] Un error en help: {e}", "red")
                #     else:
                #         try:
                #             if reaction.emoji == emos[0]:
                #                 if cog != 1:
                #                     # await msg.edit(embed=discord.Embed())
                #                     await msg.edit(embed=await self.ayuda(ctx, cog-1, cogs, paginasTotales, embed))
                #                 await msg.clear_reactions()
                #             if reaction.emoji == emos[1]:
                #                 cog += 1
                #                 print(cogs)
                #                 print(paginasTotales)
                #                 print(embed)
                #                 # await msg.edit(embed=discord.Embed())
                #                 await msg.edit(embed=await self.ayuda(ctx, cog, cogs, paginasTotales, embed))
                #                 await msg.clear_reactions()
                #             if reaction.emoji == emos[2]:
                #                 await msg.delete()
                #                 return
                #         except:
                #             if reaction.emoji == emos[0]:
                #                 if cog != 1:
                #                     await msg.edit(embed=await self.ayuda(ctx, cog+1, cogs, paginasTotales, embed))
                #                     await msg.clear_reactions()
                #             if reaction.emoji == emos[1]:
                #                 await msg.edit(embed=await self.ayuda(ctx, cog+1, cogs, paginasTotales, embed))
                #                 await msg.clear_reactions()
                #             if reaction.emoji == emos[2]:
                #                 await msg.delete()
                #                 return

                return
                

            elif re.search(r"[a-zA-Z]", str(cog)):
                congMinusculas = [c.lower() for c in cogs]
                if cog.lower() not in congMinusculas:
                    return await ctx.send(f"Argumento invalido: `{cog}`. Porfavor escoje de {paginasTotales} paginas.\nO tambien lo que puedes hacer es que puedes pone {ctx.prefix}help [categoria]")

                embed.set_footer(
                    text=f"Puedes poner @Maubot#6247 para mas info | Cog {congMinusculas.index(cog.lower())+1} de {len(congMinusculas)}"
                )

                textoDeAyuda = ""

                for comando in self.bot.get_cog(cogs[congMinusculas.index(cog.lower())]).walk_commands():
                    if comando.hidden:
                        continue
                
                    textoDeAyuda += f"** {comando.name} ║** {comando.description}\n"
                
                    if len(comando.aliases) > 0:
                        textoDeAyuda += f"**Aliados ║** {', '.join(comando.aliases)}\n"
                    textoDeAyuda += ''
                

                    prefijo = ctx.prefix

                    textoDeAyuda += f"**Formateo:** `{prefijo}{comando.name} {comando.usage if comando.usage is not None else ''}`\n\n"
                embed.description = textoDeAyuda

                await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("Upsss.... Un error **Reportando al creador**")
            return cprint(f"[Log] Un error ha ocurrido:  {e}", 'red')


def setup(bot):
    bot.add_cog(Help(bot))