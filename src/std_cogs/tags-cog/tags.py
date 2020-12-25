import discord
from discord.ext import commands
import json

from termcolor import cprint

import operator
from os import environ as env

color = int(env["COLOR"])

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
                'nombre': 'editar', 
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
        with open(env["JSON_DIR"] + 'tags.json', "r") as f:
            tags = json.load(f)
        return tags

    def cerrar_json(self, tags):
        with open(env["JSON_DIR"] + 'tags.json', "w") as f:
            json.dump(tags, f)

    @commands.group(invoke_without_command=True, aliases=["tags"], description="Buscar una tag", usage="[nombre]")
    async def tag(self, ctx, *, nombre_de_tag=None):
        if nombre_de_tag is None:
            embed=discord.Embed(title="❯ Tags", description="Aqui tienes unos comandos para los tags", color=color)
            for index in self.comandos:
                embed.add_field(name="• " + self.comandos[index]['nombre'], value=self.comandos[index]['desc'], inline=False)
            return await ctx.send(embed=embed)
        else:
            tags = self.abrir_json()
            if nombre_de_tag in tags:
                nombre = tags[nombre_de_tag]['titulo']
                desc = tags[nombre_de_tag]['desc']
                creador = tags[nombre_de_tag]['creador']
                vis = tags[nombre_de_tag]["visitas"]
                embed = discord.Embed(title=f"Tag: {nombre}", color=color)
                embed.add_field(name="Id del creador:", value=creador, inline=True)
                c = self.bot.get_user(int(creador))
                embed.add_field(name="Mencion del creador:", value=c.mention, inline=True)
                embed.add_field(name="Visitas:", value=vis+1, inline=True)
                await ctx.send(f"**Descripcion de la tag:**\n\n{desc}")
                await ctx.send(embed=embed)
                tags[nombre_de_tag]["visitas"] += 1
                self.cerrar_json(tags)
            else:
                return await ctx.send(embed=discord.Embed(title="404", description=f"{ctx.author.mention} No se encontro nada\n\n(Igual quieres crear una poniendo **{ctx.prefix}tag crear nombre|descripcion)**", color=color))
            self.cerrar_json(tags)

    @tag.command(description="Crear una tag", usage="<nombre>|<descripcion (Max 2000 car)>")
    async def crear(self, ctx: commands.Context, *, args: str=""):
        if len(args) <= 2:
            return await ctx.send(f"Porfavor escribe tu numbre de tag y separado por un | **Ej: {ctx.prefix}tag crear nombre|descripcion**")
        else:
            if "|" in args:
                if '@everyone' in args or '@here' in args or len(ctx.message.channel_mentions) > 0 or ctx.message.mention_everyone or len(ctx.message.mentions) >= 1 or len(ctx.message.role_mentions) >= 1: return await ctx.send("No puedes mencionar")
                titulo = args.split('|')[0].strip()
                desc = args.split('|')[1]
                creador = ctx.author.id
                nombre = titulo
                # print(titulo)
                # print(desc)
                if len(desc) >= 2000:
                    return await ctx.send("La descripcion es muy larga **sry**")
                tags = self.abrir_json()

                if nombre in tags:
                    return await ctx.send(f"Esa tag ya existe **{ctx.prefix}tag {nombre}**")
                tags[nombre] = {}
                tags[nombre]["titulo"] = titulo
                tags[nombre]["desc"] = desc
                tags[nombre]["creador"] = creador
                tags[nombre]["visitas"] = 0

                self.cerrar_json(tags)
                await ctx.send(embed=discord.Embed(title="Tag creada", description=f"{ctx.author.mention} se ha creado tu tag **{nombre}** correctamente" ,color=color))
            else:
                return await ctx.send(f"Porfavor escribe tu numbre de tag y separado por un | **Ej: {ctx.prefix}tag crear hola|¿Què tal?**")


    @tag.command(description="Eliminar una tag", usage="<nombre>")
    async def eliminar(self, ctx, *, args: str=""):
        if len(str(args)) <= 2:
            return await ctx.send(f"Escribe tu tag que quieras eliminar **(Tienes que haverla creado tu)**")
        else:
            tags = self.abrir_json()

            eliminador = ctx.author.id
            if str(args) in tags:
                if not eliminador == tags[str(args)]['creador']:
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
            
    @tag.command(description="Editar una tag", usage="<nombre de la tag>|<descripcion nueva>") # enabled=False
    async def editar(self, ctx: commands.Context, *, args: str=""):
        if len(str(args)) <= 2:
            return await ctx.send(f"Escribe tu tag que quieras editar **(Tienes que haverla creado tu)** | **EJ: {ctx.prefix}tag editar `nombre de la tag`|Descripcion que quieras editar**")
        else:
            tags = self.abrir_json()

            eliminador = ctx.author.id
            # print(args)
            args = args.split("|")
            # print(args[0])
            # print(tags[args[0]])
            if str(args[0].strip()) in str(tags):
                if not eliminador == tags[str(args[0].strip())]['creador']:
                    return await ctx.send("¡TU NO ERES EL CREADOR DE ESTE TAG!") 
                else:
                    try:
                        tags[args[0].strip()]["desc"] = args[1]
                        await ctx.send(embed=discord.Embed(title="Editado", description=f"{ctx.author.mention} Se ha editado la descripcion de **{args[0]}** correctamente", color=color))
                        self.cerrar_json(tags)
                    except Exception as e:
                        cprint(str("[Log] Un error ha ocurrido:  " + e), 'red')
                        return await ctx.send("Ups.. Un error editando tu tag")
            else:
                return await ctx.send(f"{ctx.author.mention} ¡Esa tag no existe!")
            self.cerrar_json(tags)
   

    @tag.command(description="Renombrar una tag", usage="<nombre>|<nombre cambiado>") # enabled=False
    async def renombrar(self, ctx: commands.Context, *, args: str=""):
        if len(str(args)) <= 2:
            return await ctx.send(f"Escribe tu tag que quieras editar **(Tienes que haverla creado tu)** \n **EJ: {ctx.prefix}tag renombrar nombre|nombre2**")
        else:
            tags = self.abrir_json()

            eliminador = ctx.author.id
            args = args.split("|")
            # print(args[0])
            # print(tags[args[0]])
            try:
                if str(args[0].strip()) in str(tags):
                    if not eliminador == tags[str(args[0].strip())]['creador']:
                        return await ctx.send("¡TU NO ERES EL CREADOR DE ESTE TAG!") 
                    else:
                        try:
                            tags[args[1]] = {}
                            tags[args[1]]["titulo"] = args[1]
                            tags[args[1]]["desc"] = tags[args[0].strip()]["desc"]
                            tags[args[1]]["creador"] = tags[args[0].strip()]["creador"]
                            tags[args[1]]["visitas"] = int(tags[args[0].strip()]["visitas"])
                            del tags[args[0].strip()]
                            await ctx.send(embed=discord.Embed(title="Renombrado", description=f"{ctx.author.mention} Se ha renombrado la tag **{args[0]}** correctamente a **{args[1]}**", color=color))
                            self.cerrar_json(tags)
                        except Exception as e:
                            cprint(str("[Log] Un error ha ocurrido:  " + e), 'red')
                            return await ctx.send("Ups.. Un error renombrando tu tag")
                else:
                    return await ctx.send(f"{ctx.author.mention} ¡Esa tag no existe!")
            except Exception as e:
                cprint(str("[Log] Un error ha ocurrido en \"cogs.tags.__main__.py\""), 'red')
                return await ctx.send("Ups.. Un error renombrando tu tag")
            self.cerrar_json(tags)

    @tag.command(description="Renombrar una tag", usage="[num]") # enabled=False
    async def listar(self, ctx, num: int = 5):
        tabla_lista = {}
        total = []
        if not num:
            return await ctx.send(f"Puedes ver las tags mas vistas ponuendo **{ctx.prefix}tag listar [num]**")
        else:
            tags = self.abrir_json()
            try:
                if not num >= 50:    
                    if num > len(tags): return await ctx.send(embed=discord.Embed(title="No hay tantas tags", description=f"{ctx.author.mention} No hay tantas tangs, Las tags que hay actualmente son: **{len(tags)}**", color=color))
                    for tag in tags:

                        visitas_totales = tags[tag]['visitas']
                        tabla_lista[visitas_totales] = tags[tag]
                        total.append(visitas_totales)
                    total = sorted(total, reverse=True)

                    index = 1
                    embed = discord.Embed(title=f"Top {num} tags", color=color)

                    for i in total:
                        creador = self.bot.get_user(tabla_lista[i]['creador'])
                        embed.add_field(name=f"{index}. {tabla_lista[i]['titulo']} | Visitas: {tabla_lista[i]['visitas']}", value=f"> Creador: {creador.mention}\n> Invocacion: {ctx.prefix}tag {tabla_lista[i]['titulo']}", inline=False)

                        if index == num:
                            break
                        else:
                            index += 1
                    await ctx.send(embed=embed)
                else:
                    return await ctx.send("No se pueden tantos")
            except Exception as e:
                cprint(f"[Log] Un error: {e}", 'red')
                return await ctx.send("Lo setimos pero ha havido un *error*")
            self.cerrar_json(tags)

def setup(bot):
    bot.add_cog(Tags(bot))
