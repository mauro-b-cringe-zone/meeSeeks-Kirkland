import discord
from discord.ext import commands
from os import environ as env
color = int(env["COLOR"]) # Un int de un hex

def textToBinary(texto: str, sep: str=' '):
    lista = []

    for i in texto:
        asc = ord(i)
        lista.append("{0:b}".format((asc)))

    return(sep.join(lista))

def binaryToText(texto: str, sep: str=' '):
    lista = texto.split(sep)

    nuevaLista = []

    for i in lista:
        bits = i
        n = int(bits, 2)
        nuevaLista.append(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())

    return (''.join(nuevaLista))

class Binario(commands.Cog):
    # La clase del robot de Discord
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="0010010101010 0101010 1010010101", usage="[text]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def binario(self, ctx, *, texto: str = "PON TEXTO IDIOTA"):
        
        if len(texto) > 70: return await ctx.send("No pongas tanto texto")

        resultado = textToBinary(texto)

        embed = discord.Embed(title="Traducido del texto a binario", colour=color)
        embed.add_field(name="Texto original", value=texto)
        embed.add_field(name="Traducido", value="```yml\n" + resultado + " \n```", inline=False) 

        await ctx.send(embed=embed)
        
    @commands.command(description="Hola, mundo", usage="[text]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bin2texto(self, ctx, *, texto: str = "0010010101010 0101010 1010010101"):
        
        resultado = binaryToText(texto)

        embed = discord.Embed(title="Traducido del binario a texto", colour=color)
        embed.add_field(name="Binario original", value=texto)
        embed.add_field(name="Traducido", value="```yml\n" + resultado  + " \n```", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Binario(bot))
