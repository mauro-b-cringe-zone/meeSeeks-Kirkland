import discord 
import asyncio
import datetime as dt  
from discord.ext import commands        
from datetime import datetime
from os import environ as env
color = 7712501
import discord
from discord.ext import commands
import sys
from subprocess import run, PIPE
from inspect import isawaitable
from asyncio import sleep
import os
from termcolor import cprint

class Creador(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    embed = discord.Embed(color=color)


    @commands.command(description="Logout")
    @commands.is_owner()
    async def logout(self, ctx):
        # await ctx.send('Hasta luego!')
        embed = discord.Embed(color=color)
        embed.set_author(name=" |  !Hasta luego!", icon_url="https://img.icons8.com/color/48/000000/shutdown--v1.png")
        await ctx.send(embed=embed)
        await self.bot.logout()

    @commands.command(description="Cerrar la cuenta")
    @commands.is_owner()
    async def cerrar(self, ctx):
        embed = discord.Embed(color=color)
        embed.set_author(name=" |  Cerrando...", icon_url="https://img.icons8.com/color/48/000000/shutdown--v1.png")
        await ctx.send(embed=embed)
        await self.bot.close()


    @commands.command(description="Recargar un cog")
    @commands.is_owner()
    async def reload(self, ctx, name: str, usage="<nombre>"):
        try:
            self.bot.reload_extension(f'cogs.{name}')
            cprint(f"[Cog] Se ha recargado cogs.{name}", "cyan")
        except Exception as e:
            return await ctx.send(e)
        await ctx.send(f"Se ha reiniciado **cosg.{name}.py**")

    @commands.command(description="Responde una reseña", usage="<id del usuario> <respuesta>")
    @commands.is_owner()
    async def rp(self, ctx, *args):
        try:
            user_to_send = self.bot.get_user(int(args[0]))
            em = discord.Embed(title="Hola,   ¡"+user_to_send.name+"!   el propietario del bot envió una respuesta para sus comentarios.", description='**Mensaje de respuesta:**\n'+' '.join(list(args)[1:len(list(args))]), color=color)
            await user_to_send.send(embed=em)
            await ctx.message.add_reaction('✅')
        except Exception as e:
            await ctx.send(f' | Error: `{e}`')

    @commands.command(aliases=['ex','eval'], description="Evalua lo que quieras", usage="<texto>")
    async def evaluate(self, ctx, *, args):
        unprefixed = args.replace('"', "'")
        if int(ctx.message.author.id)==700812754855919667:
            try:
                res = eval(unprefixed)
                if isawaitable(res): 
                    await ctx.send(embed=discord.Embed(title='Éxito de la evaluación', description='📥 **Input:**```py\n'+unprefixed+'```**📤 Output:**```py\n'+str(await res)+'```**Typo de objeto:**```py\n'+str(type(await res))+'```', color=color))
                else: 
                    msg = await ctx.send(embed=discord.Embed(title='Éxito de la evaluación', description='📥 **Input:**```py\n'+unprefixed+'```**📤 Output:**```py\n'+str(res)+'```**Typo de objeto:**```py\n'+str(type(res))+'```', color=color))
                    await msg.add_reaction(str("<:redtick:774983128581668875>"))
                    def _check(reaction, user):
                        return (
                            user == ctx.author
                            and reaction.message.id == msg.id
                        )

                    reaction, user = await self.bot.wait_for("reaction_add", check=_check)
                    if reaction == "<:redtick:774983128581668875>":
                        await msg.delete()
            except Exception as e:
                if 'cannot reuse already awaited coroutine' in str(e): 
                    return
                await ctx.send(embed=discord.Embed(title='La evaluación detectó una excepción', description='Input:```py\n'+unprefixed+'```\nException:```py\n'+str(e)+'```', color=discord.Colour.red()), delete_after=5)
        else:
            await ctx.send(embed=discord.Embed(description=f'No... | ¿Estás buscando el token de Maubot? Bueno aqui esta: `daowihdawasdawpdua.dawd.awdawdd`', color=color))


    @commands.command(description="Logout")
    @commands.is_owner()
    async def restart(self, ctx):
        embed = discord.Embed(color=color, description=f"{ctx.author.mention} El robot se estara reiniciando y estara listo en **10s**")
        embed.set_author(name="Reiniciando...")
        try:
            await ctx.send(embed=embed)
            await bot.close()
        except:
            pass
        finally:
            os.system("python ./src/main.py --cmd run")



def setup(bot):
    bot.add_cog(Creador(bot))
