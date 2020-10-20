import discord
from discord.ext import commands
import json

color = 0x75aef5 

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.comandos = {
            'tag': 'Buscar una tag',
            'crear': 'Crear una tag',
            'edit': 'Editar una tag',
            'eliminar': 'Eliminar una tag',
            'listar': 'Listar todas las tags (O un numero que tu quieras)',
            'renombrar': 'Renombrar una tag',
        }

    @commands.group()
    async def tag(self, ctx, *, nombre_de_tag=None):
        if nombre_de_tag is None:
            embed=discord.Embed(title="Ayuda con los tags", description="Aqui tienes unos comandos para los tags", color=color)
            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            # 
            #    CONTINUAR
            # 
            # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            # for index in self.comandos:
                # embed.add_field(name=)
            return await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Tags(bot))