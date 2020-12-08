import discord, asyncio
from discord.ext import commands

from os import environ as env

async def embedType(tipo, color: str, ctx, t = None, texto = None):
    if tipo is 1:
        return discord.Embed(color=color, title="No has puesto el tiempo bien", description=f"{ctx.author.mention} no has puesto el tiempo correctamente\n**eg: m.reminder [minutos] <texto>**")
    if tipo is 2:
        return discord.Embed(color=color, title="RECORDATORIO", description=f"{ctx.author.mention} Has iniciado un recordatorio hace **{t}** minutos. ").add_field(name="Recordatorio", value=texto)


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
            return await ctx.send(embed=await embedType(1, self.color, ctx))
        t = self.CalcularTiempo(tiempo)
        await ctx.send(embed=discord.Embed(color=self.color, title="Recordatorio añadido", description=f"{autor.mention} se te recordara en dentro de **{tiempo}** minuto/s"))
        await asyncio.sleep(t)
        await autor.send(embed=await embedType(2, self.color, ctx, tiempo, texto))


def setup(bot):
    bot.add_cog(Reminder(bot))