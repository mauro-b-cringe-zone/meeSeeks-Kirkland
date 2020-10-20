import discord
from discord.ext import commands
import json

from termcolor import cprint

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

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, nombre_de_tag=None):
        if nombre_de_tag is None:
            embed=discord.Embed(title="Ayuda con los tags", description="Aqui tienes unos comandos para los tags", color=color)
            for index in self.comandos:
                embed.add_field(name=self.comandos[index]['nombre'], value=self.comandos[index]['desc'])
            return await ctx.send(embed=embed)
        else:
            tags = self.abrir_json()
            if nombre_de_tag in tags:
                nombre = tags[nombre_de_tag]['titulo']
                desc = tags[nombre_de_tag]['desc']
                creador = tags[nombre_de_tag]['creador']
                embed = discord.Embed(title=f"Tag: {nombre}", description=f"Descripcion:\n **{desc}**", color=color)
                embed.add_field(name="creador:", value=creador, inline=False)
                await ctx.send(embed=embed)
            else:
                return await ctx.send(embed=discord.Embed(title="404", description=f"{ctx.author.mention} No se encontro nada\n\n(Igual quieres crear una poniendo **{ctx.prefix}tag crear nombre|descripcion)**", color=color))
            self.cerrar_json()

    @tag.command()
    async def crear(self, ctx: commands.Context, *, args: str=""):
        if len(args) <= 2:
            return await ctx.send(f"Porfavor escribe tu numbre de tag y separado por un | **Ej: {ctx.prefix}tag crear nombre|descripcion**")
        else:
            if "|" in args:
                titulo = args.split('|')[0]
                desc = args.split('|')[1]
                creador = ctx.author.name
                nombre = titulo
                # print(titulo)
                # print(desc)
                tags = self.abrir_json()

                if str(nombre) in str(tags[nombre]):
                    return await ctx.send(f"Esa tag ya existe **{ctx.prefix}tag {nombre}**")
                tags[nombre] = {}
                tags[nombre]["titulo"] = titulo
                tags[nombre]["desc"] = desc
                tags[nombre]["creador"] = creador

                self.cerrar_json(tags)
            else:
                return await ctx.send(f"Porfavor escribe tu numbre de tag y separado por un | **Ej: {ctx.prefix}tag crear hola|¿Què tal?**")


    @tag.command()
    async def eliminar(self, ctx, *, args: str=""):
        if len(str(args)) <= 2:
            return await ctx.send(f"Escribe tu tag que quieras eliminar **(Tienes que haverla creado tu)**")
        else:
            tags = self.abrir_json()

            eliminador = ctx.author.name
            if str(args) in tags:
                if not eliminador in tags[str(args)]['creador']:
                    return await ctx.send("¡¡¡TU NO ERES EL CREADOR DE ESTE TAG!!!") 
                else:
                    try:
                        # print(tags[args])
                        del tags[str(args)]
                        await ctx.send(embed=discord.Embed(title="Eliminado", description=f"{ctx.author.mention} Se ha eliminado {args} correctamente", color=color))
                        self.cerrar_json(tags)
                    except Exception as e:
                        cprint(str("[Log] Un error ha ocurrido:  " + e), 'red')
            else:
                return await ctx.send(f"{ctx.author.mention} ¡¡¡Esa tag no existe!!!")
            self.cerrar_json(tags)
            
    @tag.command()
    async def editar(self, ctx, *, args: str=""):
        if len(str(args)) <= 2:
            return await ctx.send(f"Escribe tu tag que quieras editar **(Tienes que haverla creado tu)**")
        else:
            tags = self.abrir_json()

            eliminador = ctx.author.name
            if str(args) in tags:
                if not eliminador in tags[str(args)]['creador']:
                    return await ctx.send("¡¡¡TU NO ERES EL CREADOR DE ESTE TAG!!!") 
                else:
                    try:
                        ### CONTINUAR
                        await ctx.send(embed=discord.Embed(title="Editadp", description=f"{ctx.author.mention} Se ha editado {args} correctamente", color=color))
                        self.cerrar_json(tags)
                    except Exception as e:
                        cprint(str("[Log] Un error ha ocurrido:  " + e), 'red')
            else:
                return await ctx.send(f"{ctx.author.mention} ¡¡¡Esa tag no existe!!!")
            self.cerrar_json(tags)

def setup(bot):
    bot.add_cog(Tags(bot))