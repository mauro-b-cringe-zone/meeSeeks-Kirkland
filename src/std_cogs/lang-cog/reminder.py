import discord, asyncio, time
from discord.ext import commands

from os import environ as env



class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot     
        self.color = int(env["COLOR"])

    def CalcularTiempo(self, t: float):
        return t * 60

    @commands.command(aliases=["remind"], description="Se te recordara una tarea que tu quieras", usage="<Tiempo: minutos> <Recordatorio: texto>")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def reminder(self, ctx: commands.Context, tiempo: float, *, texto):
        autor = ctx.author
        if tiempo is None and texto is None:
            return await ctx.send(embed=discord.Embed(color=self.color, title="No has puesto el tiempo bien", description=f"{ctx.author.mention} no has puesto el tiempo correctamente\n**eg: m.reminder [minutos] <texto>**"))
        t = self.CalcularTiempo(tiempo)
        await ctx.send(embed=discord.Embed(color=self.color, title="Recordatorio añadido", description=f"{autor.mention} se te recordara en dentro de **{tiempo}** minuto/s"))
        await asyncio.sleep(t)
        start = time.perf_counter()
        recormsg = await autor.send(embed=discord.Embed(color=self.color, title="RECORDATORIO", description=f"{ctx.author.mention} Has iniciado un recordatorio hace **{tiempo}** minutos. ").add_field(name="Recordatorio", value=texto))
        end = time.perf_counter()
        speed = round((end - start) * 1000)
        await recormsg.edit(embed=discord.Embed(color=self.color, title="RECORDATORIO", description=f"{ctx.author.mention} Has iniciado un recordatorio hace **{tiempo}** minutos. ").add_field(name="Recordatorio", value=texto).add_field(name="tardanza", description=speed + "ms", inline=False))


def setup(bot):
    bot.add_cog(Reminder(bot))