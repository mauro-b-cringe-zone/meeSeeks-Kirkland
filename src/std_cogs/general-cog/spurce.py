import discord
from discord.ext import commands

from os import environ as env
import inspect

color = int(env["COLOR"])

class Source(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.url_base = "https://github.com/maubg-debug/maubot/"
        self.logo = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"

    @commands.command(description="Mira el codigo fuente de un comando", usage="[comando]", aliases="command,src".split(","))
    async def source(self, ctx, comando=None):
        if comando is None:
            return await ctx.send(embed=discord.Embed(title="Codigo fuente de Maubot", description=f"Puedes mirarlo dandole al **[link]({self.url_base})**", color=color).set_thumbnail(url=self.logo))
        try:
            cmd = self.bot.get_command(comando)
            root = cmd.module.replace(".", "/") + ".py"
            url = f"{self.url_base}blob/main/src/{root}"
        except:
            return await ctx.send(embed=discord.Embed(color=color, title="No se ha encontrado", description=f"{ctx.author.mention} El comando **{comando}** no existe"))

        lines, first_line_no = inspect.getsourcelines(cmd.callback.__code__)

        lines_extension = f"#L{first_line_no}-L{first_line_no+len(lines)-1}" # Conseguimos la linea final        
        linea = f"{url}{lines_extension}"
        
        msg = await ctx.send(embed=discord.Embed(color=color, title=f"<:github:774580260506435594> | Comando: {cmd.name}", description=f"- El comando se puede encontrar **[aqui]({linea})**").add_field(name="Descripcion", value=cmd.description if cmd.description else "Este comando no tiene descripcion").set_thumbnail(url=self.logo))
        await msg.add_reaction("<:github:774580260506435594>")

def setup(bot):
    bot.add_cog(Source(bot))