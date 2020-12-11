import discord
from discord.ext import commands
from os import environ as env
color = int(env["COLOR"])

def textToBinary(text: str, sep: str=' '):
    list = []

    for i in text:
        asc = ord(i)
        list.append("{0:b}".format(asc))

    return(sep.join(list))

def binaryToText(text: str, sep: str=' '):
    list = text.split(sep)

    newList = []

    for i in list:
        bits = i
        n = int(bits, 2)
        newList.append(n.to_bytes((n.bit_length() + 7) // 8, 'big').decode())

    return (''.join(newList))

class Binario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="0010010101010 0101010 1010010101", usage="[text]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def binario(self, ctx, *, texto = "PON TEXTO IDIOTA"):
        
        resultado = textToBinary(texto)

        embed = discord.Embed(title="Traducido del texto a binario", colour=color)
        embed.add_field(name="Texto original", value=texto)
        embed.add_field(name="Traducido", value="```yaml " + resultado + "```", inline=False) 

        await ctx.send(embed=embed)
        
    @commands.command(description="Hola, mundo", usage="[text]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bin2texto(self, ctx, *, texto = "0010010101010 0101010 1010010101"):
        
        resultado = binaryToText(texto)

        embed = discord.Embed(title="Traducido del binario a texto", colour=color)
        embed.add_field(name="Binario original", value=texto)
        embed.add_field(name="Traducido", value=resultado, inline=False)

        await ctx.send(embed=embed)
    


def setup(bot):
    bot.add_cog(Binario(bot))