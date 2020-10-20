import discord
from discord.ext import commands
import json

color = 0x75aef5 

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.comandos =  {
            
            1: {
                'nombre': 'tag',
                'desc':' Buscar una tag'
            },

            2: {
                'nombre': 'crear', 
                'desc': 'Crear una tag'
            },
            3: {
                'nombre': 'edit', 
                'desc': 'Editar una tag'
            },
            4: {
                'nombre': 'eliminar', 
                'desc': 'Eliminar una tag'
            },
            5: {
                'nombre': 'listar', 
                'desc': 'Listar todas las tags (O un numero que tu quieras)'
            },
            6: {
                'nombre': 'renombrar', 
                'desc': 'Renombrar una tag'
            }
        }

    def abrir_json(self):
        with open('./json/tags.json', "r") as f:
            tags = json.load(f)
        return tags

    def cerrar_json(self, tags):
        with open('./json/tags.json', "w") as f:
            json.dump(tags, f)

    @commands.group(pass_context=True)
    async def tag(self, ctx, *, nombre_de_tag=None):
        if nombre_de_tag is None:
            embed=discord.Embed(title="Ayuda con los tags", description="Aqui tienes unos comandos para los tags", color=color)
            for index in self.comandos:
                embed.add_field(name=self.comandos[index]['nombre'], value=self.comandos[index]['desc'])
            return await ctx.send(embed=embed)
        else:
            tags = self.abrir_json()
            if nombre_de_tag in tags:
                nombre = tags[nombre_de_tag]['nombre']
                desc = tags[nombre_de_tag]['desc']
                embed = discord.Embed(title=f"Tag: {nombre}", description=f"Descripcion: {desc}", color=color)
            else:
                return await ctx.send(embed=discord.Embed(title="404", description=f"{ctx.author.mention} No se encontro nada\n\n(Igual quieres crear una poniendo **{ctx.prefix}tag crear)**", color=color))
            self.cerrar_json()

    @tag.command(pass_context=True)
    async def crear(self, ctx, *, args: str):
        if len(args) <= 2:
            return await ctx.send(f"Porfavor escribe tu numbre de tag y separado por un | **Ej: {ctx.prefix}tag crear hola|¿Què tal?**")
        else: # SOLUCIONAR LOS SUBCOMANDOS
            if "|" in args:
                titulo = args.split('|')[0]
                desc = args.split('|')[1]
                print(titulo)
                print(desc)
            else:
                return await ctx.send(f"Porfavor escribe tu numbre de tag y separado por un | **Ej: {ctx.prefix}tag crear hola|¿Què tal?**")


def setup(bot):
    bot.add_cog(Tags(bot))