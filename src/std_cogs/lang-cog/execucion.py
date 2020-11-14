import asyncio 

import re
import json
import base64
import aiohttp
from http.client import responses
from datetime import datetime

import discord
from discord.ext import commands
from discord import Embed, Color


from typing import Optional, List

from os import environ as env

from datetime import datetime as dt
from dataclasses import dataclass

from discord import Colour
from termcolor import cprint

AUTH_HEADER = 'X-RapidAPI-Key'
AUTH_KEY = env['COMP_KEY'] # Llave
BASE_URL = 'https://judge0.p.rapidapi.com'
PREFIX = '$'
NEWLINES_LIMIT = 10 
CHARACTERS_LIMIT = 300


START_TIME = dt.utcnow()

LANGUAGES = {
   "array": {
    45: {
        'command': 'assembly',
        'version': 'Assembly (NASM 2.14.02)',
        'icon': 'https://i.imgur.com/ObWopeS.png',
        'emoji': '<:assembly:662723858859556865>',
        },
    46: {
        'command': 'bash',
        'aliases': ['sh'],
        'version': 'Bash (4.4)',
        'icon': 'https://i.imgur.com/6BQ4g4J.png',
        'emoji': '<:bash:623909088572735498>',
        },
    50: {
        'command': 'c',
        'version': 'C (GCC 9.2.0)',
        'icon': 'https://i.imgur.com/Aoo95wm.png',
        'emoji': '<:c_:623909093136138240>',
        },
    54: {
        'command': 'cpp',
        'version': 'C++ (GCC 9.2.0)',
        'aliases': ['c++'],
        'icon': 'https://i.imgur.com/CJYqkG5.png',
        'emoji': '<:cpp:623909088459227149>',
        },
    51: {
        'command': 'csharp',
        'version': 'C# (Mono 6.6.0.161)',
        'aliases': ['c#'],
        'icon': 'https://i.imgur.com/M1AQVY2.png',
        'emoji': '<:csharp:623909092402003999>',
        },
    55: {
        'command': 'lisp',
        'version': 'Common Lisp (SBCL 2.0.0)',
        'icon': 'https://i.imgur.com/ms9qW6e.png',
        'emoji': '<:common_lisp:662723858066964490>',
        },
    56: {
        'command': 'd',
        'version': 'D (DMD 2.089.1)',
        'icon': 'https://i.imgur.com/uoeBAsf.png',
        'emoji': '<:d_language:662725748552892437>',
        },
    57: {
        'command': 'elixir',
        'version': 'Elixir (1.9.4)',
        'icon': 'https://i.imgur.com/0tigIIL.png',
        'emoji': '<:elixir:623909093148590094>',
        },
    58: {
        'command': 'erlang',
        'version': 'Erlang (OTP 22.2)',
        'icon': 'https://i.imgur.com/5dVX2NF.png',
        'emoji': '<:erlang:623909088782450707>',
        },
    60: {
        'command': 'go',
        'version': 'Go (1.13.5)',
        'aliases': ['golang'],
        'icon': 'https://i.imgur.com/a3yrHtU.png',
        'emoji': '<:golang:623909092913840128>',
        },
    61: {
        'command': 'haskell',
        'version': 'Haskell (GHC 8.8.1)',
        'icon': 'https://i.imgur.com/NpyZ3z7.png',
        'emoji': '<:haskell:623909088622936065>',
        },
    62: {
        'command': 'java',
        'version': 'Java (OpenJDK 13.0.1)',
        'icon': 'https://i.imgur.com/5OwBztX.png',
        'emoji': '<:java:623909088614678544>',
        },
    63: {
        'command': 'javascript',
        'aliases': ['js'],
        'version': 'JavaScript (Node.js 12.14.0)',
        'icon': 'https://i.imgur.com/YOsQqBF.png',
        'emoji': '<:javascript:623909088727924747>',
        },
    64: {
        'command': 'lua',
        'version': 'Lua (5.3.5)',
        'icon': 'https://i.imgur.com/WVKZnEo.png',
        'emoji': '<:lua:662723859593691156>',
        },
    65: {
        'command': 'ocaml',
        'version': 'OCaml (4.09.0)',
        'icon': 'https://i.imgur.com/pKLADe6.png',
        'emoji': '<:ocaml:623909088597901342>',
        },
    66: {
        'command': 'octave',
        'version': 'Octave (5.1.0)',
        'icon': 'https://i.imgur.com/dPwBc2g.png',
        'emoji': '<:octave:623909089033846834>',
        },
    67: {
        'command': 'pascal',
        'version': 'Pascal (FPC 3.0.4)',
        'icon': 'https://i.imgur.com/KjSF3JE.png',
        'emoji': '<:pascal:624678099518357504>',
        },
    68: {
        'command': 'php',
        'version': 'PHP (7.4.1)',
        'icon': 'https://i.imgur.com/cnnYSIE.png',
        'emoji': '<:php:662723859572588564>',
        },
    69: {
        'command': 'prolog',
        'version': 'Prolog (GNU Prolog 1.4.5)',
        'icon': 'https://i.imgur.com/yQAknfK.png',
        'emoji': '<:prolog:662723857878089809>',
        },
    71: {
        'command': 'python',
        'version': 'Python (3.8.1)',
        'aliases': ['py'],
        'icon': 'https://i.imgur.com/N4RyEvG.png',
        'emoji': '<:python:623909092989075468>',
        },
    72: {
        'command': 'ruby',
        'version': 'Ruby (2.7.0)',
        'icon': 'https://i.imgur.com/u9xb12N.png',
        'emoji': '<:ruby:623909093471420446>',
        },
    73: {
        'command': 'rust',
        'version': 'Rust (1.40.0)',
        'icon': 'https://i.imgur.com/l1TnRxU.png',
        'emoji': '<:rust:623909092628496384>',
        },
    74: {
        'command': 'typescript',
        'aliases': ['ts'],
        'version': 'TypeScript (3.7.4)',
        'icon': 'https://i.imgur.com/IBjXVQv.png',
        'emoji': '<:typescript:662723857643208716>',
        }
   },

    "ids": {
        'assembly': 45, 'bash': 46, 'sh': 46,
        'c': 50, 'cpp': 54, 'c++': 54, 'csharp': 51,
        'c#': 51, 'lisp': 55, 'd': 56, 'elixir': 57,
        'erlang': 58, 'go': 60, 'golang': 60,
        'haskell': 61, 'java': 62, 'javascript': 63,
        'js': 63, 'lua': 64, 'ocaml': 65, 'octave': 66,
        'pascal': 67, 'php': 68, 'prolog': 69, 'python': 71,
        'py': 71, 'ruby': 72, 'rust': 73,
        'typescript': 74, 'ts': 74
        }
}


@dataclass
class Emoji:
    """
    Representa el almacenamiento de emojis personalizados y externos.
    """
    class Workers:
        """
        Representa emojis para el control de salud de los trabajadores.
        (comando en bot.cogs.information)
        """
        total= "<:total:620744869429641236>"
        available = "<:available:620705066604560405>"
        idle = "<:idle:620702759414661120>"
        working = "<:working:620704067672342528>"
        paused = "<:paused:620704067479666688>"
        failed = "<:failed:620704067525672980>"

    class Execution:
        loading = "<a:typing:705421984141672470>"
        error = "<:dnd:705421983952666674>"
        successful = "<:online:705421983927763055>"
        offline = "<:offline:705421983873105920>"
        idle = "<:idle:705421983906660454>"

@dataclass
class Color:
    difficulties = [5025872, 9225035, 13491257, 16772154, 16761352, 16750593, 16668450, 16073527]


class Execution(commands.Cog):
    """
    Representa un Cog para ejecutar códigos fuente.
    """

    def __init__(self, bot):
        self.bot = bot

    async def __create_output_embed(
        self,
        token: str,
        source_code: Optional[str],
        stdout: str,
        stderr: str,
        compile_output: str,
        time: float,
        memory: int,
        language: str,
        language_id: int,
        language_icon: str,
        description: str,
        author_name: str,
        author_icon: str,
    ):
        """
        Crea una incrustación de Discord para la ejecución del envío.
        
        Incluye:
            Autor de la presentación.
            Color verde o rojo del incrustado según descripción.
            Salida (stdout, stderr, compilar salida)
            Enlace para salida completa (si corresponde)
            Uso de tiempo y memeroy
            Nombre, icono y versión del idioma.
            Fecha y hora de la ejecución.
        """
        color =   Colour.green() if description == "Aceptado" else Colour.red()

        embed = Embed(color=0x75aef5, timestamp=datetime.utcnow())
        embed.set_author(name=f"Codigo de ejecucion de {author_name}", icon_url=author_icon)


        output = Execution.concat_output(stdout, stderr, compile_output)
        embed = Execution.resize_output_for_embed(output, embed, token)

        if time:
            embed.add_field(name="Tiempo", value=f"{time} s")
        if memory:
            embed.add_field(name="Memoria", value=f"{round(memory / 1000, 2)} MB")
        embed.set_footer(text=f"{language} | Aceptado", icon_url=language_icon)

        return embed

    def __create_how_to_pass_embed(self, lang):
        """
        Crea una guía de incrustación de Discord para pasar el código.
        Incluye los 3 métodos para pasar el código fuente.
        """
        embed = Embed(title=f"¿Cómo pasar {lang['version'].split('(')[0]}código fuente?")
        embed.color =   int(env["COLOR"])

        embed.set_thumbnail(url=lang['icon'])
        embed.add_field(
            name="Método 1 (Plain)",
            value=(f"{PREFIX}{lang['command']}\n" "Codigo"),
            inline=False,
        )
        embed.add_field(
            name="Método 2 (Code block)",
            value=(f"{PREFIX}{lang['command']}\n" "\`\`\`Codigo\`\`\`"),
            inline=False,
        )
        embed.add_field(
            name="Método 3 (Syntax Highlighting)",
            value=(f"{PREFIX}{lang['command']}\n" f"\`\`\`{lang['command']}\n" "Codigo\`\`\`"),
            inline=False,
        )
        return embed

    async def __execute_code(self, ctx, lang, code: Optional[str]):
        """
        El método principal para ejecutar el código fuente de un mensaje.  
        Si se pasa la verificación de versión para arg, envía solo la versión de idioma.
        Los pasos para ejecutar el código:
            quita el código fuente
            crea y espera la salida de sumbisión
            si hay error envía el error
            de lo contrario, crea una inserción para la salida y la envía en el mismo chat
        """

        if code == None:
            await ctx.send(embed=self.__create_how_to_pass_embed(lang))
            await ctx.message.add_reaction(Emoji.Execution.idle)
            return

        if code.startswith("-v") or code.startswith("--version"):
            await ctx.send(embed=Embed(title=f"Version para {lang['command']}", color=int(env["COLOR"])).set_thumbnail(url=lang["icon"]).add_field(name="\uFEFF", value=f"> {lang['version']}"))
            cprint(f"[Log] Se ha pedido la version de {lang['command']}, Version: {lang['version']}", "green")
            # await ctx.author.message.add_reaction(Emoji.Execution.idle)
            return

        # await ctx.author.message.add_reaction(Emoji.Execution.loading)
        code = self.strip_source_code(code)
        submission = await self.get_submission(code, lang['id'])

        if isinstance(submission, str):  # it is error code
            await ctx.message.add_reaction(Emoji.Execution.offline)
            await ctx.send(submission)
            await ctx.message.remove_reaction(
                Emoji.Execution.loading, self.bot.user
            )
            return

        await ctx.send(
            embed=await self.__create_output_embed(
                token=submission["token"],
                source_code=submission["source_code"],
                stdout=submission["stdout"],
                stderr=submission["stderr"],
                compile_output=submission["compile_output"],
                time=submission["time"],
                memory=submission["memory"],
                language=lang['version'],
                language_id=submission["language_id"],
                language_icon=lang['icon'],
                description=submission["status"]["description"],
                author_name=str(ctx.message.author),
                author_icon=ctx.message.author.avatar_url,
            )
        )
        if submission["status"]["description"] == "Aceptado":
            await ctx.message.add_reaction(Emoji.Execution.successful)
        else:
            await ctx.message.add_reaction(Emoji.Execution.error)
        await ctx.message.remove_reaction(
            Emoji.Execution.loading, self.bot.user
        )

    @commands.group(pass_context=True, aliases=list(LANGUAGES['ids'].keys()), usage="[codigo]")
    async def run(self, ctx, *, code: Optional[str]):
        """
        El comando principal que maneja el proceso de ejecución del código.
        """

        if str(ctx.invoked_with) == "run" and code is None:
            return await ctx.send(f"Pon **{ctx.prefix}run --list** para ver la lista de lenguages")

        if str(ctx.invoked_with) == "run" and code == "list" or code == "--list":
            embed = Embed(title="Lista de lenguages", color=int(env["COLOR"]))
            listaDeLenguages = ""
            c = 0
            for i in LANGUAGES["array"]:
                c += 1
                # print(i)
                lang_id = LANGUAGES["array"][i]
                # print(lang_id)
                listaDeLenguages += f"**{c}. {ctx.prefix}{lang_id['command']}** | {lang_id['version']}\n"
            embed.description = listaDeLenguages
            await ctx.send(embed=embed)

        lang_id = LANGUAGES['ids'][str(ctx.invoked_with)]
        lang = LANGUAGES['array'][lang_id]
        lang.update({'id': lang_id})

        await self.__execute_code(ctx, lang, code)
        # if ctx.invoked_subcommand is None:
        #     await ctx.wait('Se pasó un subcomando no válido...')

    @staticmethod
    def prepare_paylad(source_code: Optional[str],
                       language_id: int,
                       stdin: str = "",
                       expected_output: str = ""):
        base64_code = base64.b64encode(source_code.encode()).decode()
        base64_stdin= base64.b64encode(stdin.encode()).decode()
        
        payload = {"source_code": base64_code,
                   "language_id": language_id,
                   "stdin": base64_stdin}
    
        if expected_output:
            payload["expected_output"] = expected_output
        return payload

    @staticmethod
    def concat_output(stdout: str, stderr: str, compile_output: str):
        """
        Concate los parámetros de salida en un valor de salida.
        """
        output = str()
        for each in (stdout, stderr, compile_output):
            if each:
                output += base64.b64decode(each.encode()).decode()
        if not output:
            return "No output"
        return output
    
    @staticmethod
    def resize_output_for_embed(output, embed, token):
        """
        Cambia el tamaño de la salida para la inserción si es demasiado grande.
        Demasiado grande si contiene muchos caracteres o muchas líneas nuevas.
        Esto evita el abuso de salida grande que molesta a los usuarios en el chat.
        """
        if len(output) > 300 or output.count("\n") > 10:
            embed.description = f"Salida demasiado grande - [Salida completa](http://maubot.mooo.com/maucompilador/?{token})"

            if output.count("\n") > 10:
                output = "\n".join(output.split("\n")[:10]) + "\n(...)"
            else:
                output = output[:300] + "\n(...)"
        else:
            embed.description = f"Edite este código en un IDE en línea - [Aqui](http://maubot.mooo.com/maucompilador/?{token})"

        embed.add_field(name="Salida", value=f"```yaml\n{output}```", inline=False)
        return embed
    
    @staticmethod
    async def wait_submission(cs, base_url, token: str, headers: dict) -> dict:
        while True:
            submission = await cs.get(f"{base_url}{token}?base64_encoded=true", headers=headers)
            if submission.status not in [200, 201]:
                return f"{submission.status} {responses[submission.status]}"

            data = await submission.json()
            if data["status"]["id"] not in [1, 2]:
                break
        return data

    @staticmethod
    async def get_submission(
        source_code: Optional[str], language_id: int, stdin=""
    ) -> dict:
        """
        Envia la submision del codigo del usuario 
        """
        base_url = f"{BASE_URL}/submissions/"
        payload = Execution.prepare_paylad(source_code, language_id, stdin)
        headers = {
            'X-RapidAPI-Host': 'judge0.p.rapidapi.com',
            AUTH_HEADER: AUTH_KEY,
            }    
        
        async with aiohttp.ClientSession() as cs:
            async with cs.post(f"{base_url}?base64_encoded=true",
                               json=payload,
                               headers=headers) as r:

                if r.status not in [200, 201]:
                    return f"{r.status} {responses[r.status]}"
                
                res = await r.json()
            token = res["token"]
            data = await Execution.wait_submission(cs, base_url, token, headers)

        data["token"] = token
        data.update(payload)
        return data

    @staticmethod
    def strip_source_code(code: Optional[str]):
        """
        Elimina el código fuente de un mensaje de Discord.
        
        Despoja:
            código envuelto en comillas invertidas `(código de una línea)
            código envuelto en triple backtick `` `(código multilínea)
            código envuelto en comillas triples y
                 palabra clave del lenguaje `` python (resaltado de sintaxis)
        """
        code = code.strip("`")
        if re.match(r"\w*\n", code):
            code = "\n".join(code.split("\n")[1:])
        return code

def setup(bot):
    bot.add_cog(Execution(bot))