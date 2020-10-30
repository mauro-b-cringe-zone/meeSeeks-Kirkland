import discord
from discord.ext import commands

from os import environ as env

color = env["COLOR"]

class Mates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # MATES

    @commands.command(description="Sumar dos numeros", usage="<num1><num2>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sum(self, ctx, numOne: int, numTwo: int):
        embed = discord.Embed(title=f"{numOne} + {numTwo} = {numOne + numTwo}", colour=color)
        await ctx.send(embed=embed)
        
    @commands.command(description="multiplicar dos numeros", usage="<num1><num2>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def mul(self, ctx, numOne: int, numTwo: int):
        embed = discord.Embed(title=f"{numOne} x {numTwo} = {numOne * numTwo}", colour=color)
        await ctx.send(embed=embed)

    @commands.command(description="dividir dos numeros", usage="<num1><num2>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def div(self, ctx, numOne: int, numTwo: int):
        embed = discord.Embed(title=f"{numOne} / {numTwo} = {numOne / numTwo}", colour=color)
        await ctx.send(embed=embed)


    @commands.command(description="restar dos numeros", usage="<num1><num2>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def restar(self, ctx, numOne: int, numTwo: int):
        embed = discord.Embed(title=f"{numOne} - {numTwo} = {numOne - numTwo}", colour=color)
        await ctx.send(embed=embed)

    @commands.command(description="Raiz cuadrada de un numero", usage="<num>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rz(self, ctx, numOne: int):
        embed = discord.Embed(title=f"La raiz cuadrda de {numOne} es:    {numOne ** (1/2)}", colour=color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Mates(bot))