import discord
from discord.ext import commands
import binascii
import asyncio
from os import environ as env
color = int(env["COLOR"])

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

def texto_a_binario(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def binario_a_texto(bits, encoding='utf-8', errors='surrogatepass'):
    bits = bits.replace(' ', '')
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

class Binario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="0010010101010 0101010 1010010101")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def binario(self, ctx, *, texto = "PON TEXTO IDIOTA"):
        
        resultado = texto_a_binario(texto)

        embed = discord.Embed(title="Traducido del texto a binario", colour=color)
        embed.add_field(name="Texto original", value=texto)
        embed.add_field(name="Traducido", value=resultado, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/746668731060715551/746761731942121532/unknown.png")     

        await ctx.send(embed=embed)
        
    


def setup(bot):
    bot.add_cog(Binario(bot))