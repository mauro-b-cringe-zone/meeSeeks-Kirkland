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

    # @commands.command()
    # async def reiniciar(self, ctx):
    #     id = str(ctx.author.id)
    #     if id == '700812754855919667':
    #         embed = discord.Embed(title="Reiniciando...", colour=color)
    #         msg = await ctx.send(embed=embed)
    #         await msg.add_reaction('✅')
    #         await self.bot.close()
    #     else:
    #         await ctx.send("¡No tienes permisos para hacer esta accion!")


    # @commands.command(aliases=['sh'])
    # async def bash(self, ctx, *args):
    #     unprefixed = ' '.join(list(args))
    #     if int(ctx.message.author.id)==700812754855919667:
    #         try:
    #             if len(list(args))==0: 
    #                 raise OSError('Eres idiota')
    #             if len(unprefixed.split())==1: 
    #                 data = run([unprefixed], stdout=PIPE).stdout.decode('utf-8')
    #             else: 
    #                 data = run([unprefixed.split()[0], ' '.join(unprefixed.split()[1:len(unprefixed)])], stdout=PIPE).stdout.decode('utf-8')
    #             await ctx.send(embed=discord.Embed(title='Terminal', description='Input:```sh\n'+str(unprefixed)+'```**Output:**```sh\n'+str(data)+'```', color=color))
    #         except Exception as e:
    #             await ctx.send(embed=discord.Embed(title='Error en la execucion', description='Input:```sh\n'+str(unprefixed)+'```**Error:**```py\n'+str(e)+'```', color=color))
    #     else:
    #         await ctx.send(embed=discord.Embed(title='Error en la execucion', description='Input:```sh\n'+str(unprefixed)+'```**Error:**```py\nDenegado por Maubot.py```', color=color))


    @commands.command(aliases=['ex','eval'], description="Evalua lo que quieras", usage="<texto>")
    async def evaluate(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if int(ctx.message.author.id)==7008127548553919667:
            try:
                res = eval(unprefixed.replace('"', "'"))
                if isawaitable(res): 
                    await ctx.send(embed=discord.Embed(title='Éxito de la evaluación', description='📥 Input:```py\n'+unprefixed+'```**📤 Output:**```py\n'+str(await res)+'```Typo de objeto:```py\n'+str(type(await res))+'```', color=color))
                else: 
                    await ctx.send(embed=discord.Embed(title='Éxito de la evaluación', description='📥 Input:```py\n'+unprefixed+'```**📤 Output:**```py\n'+str(res)+'```Typo de objeto:```py\n'+str(type(res))+'```', color=color))
            except Exception as e:
                if 'cannot reuse already awaited coroutine' in str(e): 
                    return
                await ctx.send(embed=discord.Embed(title='La evaluación detectó una excepción', description='Input:```py\n'+unprefixed+'```\nException:```py\n'+str(e)+'```', color=discord.Colour.red()), delete_after=5)
        else:
            await ctx.send(embed=discord.Embed(description=f'{self.bot.get_emoji(":sad:")} | ¿Estás buscando el token de Maubot? Bueno aqui esta: `daowihdawasdawpdua.dawd.awdawdd`', color=color))

    @commands.command(aliases=['bots'], description="Mira los bots")
    async def botmembers(self, ctx):
        botmembers, off, on, warning = "", 0, 0, 'Triángulos hacia abajo significa que el bot está caído. Y los triángulos arriba significan que el bot está bien'
        for i in range(0, int(len(ctx.message.guild.members))):
            if i > 20: break
            if len(botmembers)>1900:
                warning = str(' | Error: Muchos bots algunos estan alistados arriba.')
                break
            if ctx.message.guild.members[i].bot==True:
                if str(ctx.message.guild.members[i].status)=='offline':
                    off += 1
                    botmembers += ':small_red_triangle_down: '+ ctx.message.guild.members[i].name + '\n'
                else:
                    on += 1
                    botmembers += ':small_red_triangle: ' + ctx.message.guild.members[i].name + '\n'
        embed = discord.Embed( title = 'Bots de '+ctx.message.guild.name+':', description = '**Online: '+str(on)+' ('+str(round(on/(off+on)*100))+'%)\nOffline: '+str(off)+' ('+str(round(off/(off+on)*100))+'%)**\n\n'+str(botmembers), colour = color)
        embed.set_footer(text=warning)
        await ctx.send(embed=embed)

    @commands.command(description="Logout")
    @commands.is_owner()
    async def restart(self, ctx):
        # await ctx.send('Hasta luego!')
        embed = discord.Embed(color=color)
        embed.set_author(name="Reiniciando...")
        try:
            await ctx.send(embed=embed)
            await bot.close()
        except:
            pass
        finally:
            os.system("python ./src/main.py")



def setup(bot):
    bot.add_cog(Creador(bot))