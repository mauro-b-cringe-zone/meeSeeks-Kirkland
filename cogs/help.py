import discord
from discord.ext import commands
import time
import datetime
import asyncio
color = 0x75aef5 

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
   #TODO make this dictionary based on "array"
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

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, sec=None):


        if sec=="fun":

            print("[Log] Ayuda fun enviada")

            emos_fun = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '🎮': 4, '🔴': 'stop'}

            embed1 = discord.Embed(title="COMANDOS DE DIVERSION                   pag(1/4)", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed1.set_author(name="Ayuda para comandos de fun 1", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed1.add_field(name='argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requieres en base a uso', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}say <tu frase>', value='Con este comando puedes hacer que el bot diga una frase sin que nadie se entere de que has sido tu.', inline=False)
            # embed1.add_field(name='cat', value='Si tu pones este commando te saldra una foto de un gato random **advertencia: demasiado monos**', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}f', value='Te saldra una frase de el meme "[f] to show respect"', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}nicememe', value='Te llevara a la mejor pagina web de memes del mundo.', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}pegar <miembro> [razon]', value='Pega al que mas odies.', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}spam', value='Si pones esto habra el mejor spam del mundo. :drooling_face:',  inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}b1nzy', value='GATO ANIKILATOOOOOOOOOOOOOR... YEA :smirk_cat:', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}cykablyat', value='meme ruso...', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}sombra', value='Respondera una calavera gigante', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}lenny', value='Te da una cara graciosa', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}tableflip', value='Estas enfadado', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}doubleflip', value='Eswtas **muy** enfadado', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}misc_weeb_face', value='Te has cabrado', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}gun', value='||︻芫═───||', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}coin', value='Gira la moneda', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}gl <Busqueda>', value='Te busca algo en google', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}psat', value='Memes de psat random', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}ball <tu frase>', value=f'Respondera a cualquier pregunta con **ex: {ctx.prefix}ball cual es el significado de la vida?**', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}actdrunk', value='enviara mensajes al server como un borracho', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}rate [usuario]', value='dara una evaluacion de 10 al usuario que quieras', inline=False)
            embed1.add_field(name=f'•| {ctx.prefix}insult <usuario>', value=f'Insultara al usuario que menciones acompañado de ** {ctx.prefix}insult **', inline=False)
            # embed1.add_field(name='•| owo <tu frase>', value='pondra owo en tu frase', inline=False)
            embed1.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga {ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed1.add_field(name="Unete a nuestro servidor de ayuda", value="**servidor -->  ( https://discord.gg/4gfUZtB )**")
            embed1.set_footer(text=ctx.author.name + "   pag(1/4)   ", icon_url=ctx.author.avatar_url)




            embed2 = discord.Embed(title="COMANDOS DE DIVERSION                   pag(2/4)", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed2.set_author(name="Ayuda para comandos de fun 2", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed2.add_field(name=f'•| {ctx.prefix}plzmsgme <tu frase>', value='Te hara un mensaje directo con la frase que tu quieras.', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}quote', value='Un savio dijo una vez...', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}twentyoneify <tu frase>', value='Cambia todas las o y 0 por ø y Ø', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}spellout <tu frase>', value='Te deletreara la palabra/frase que tu pongas.', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}trigger <usuario>', value='Trigger meme',  inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}reverse <tu frase>', value='Dira la frase/palabra alreves.', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}roulette', value='Ruleta rusa **Si perdes te expulsan**', inline=False)
            # embed2.add_field(name='•| encodemorse <tu frase>', value='lo traduce a coodigo morse', inline=False)
            # embed2.add_field(name='•| decodemorse <tu frase>', value='de morse a abecedario', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}randomnumber <numero>', value='Numero random minimo del numero que tu pongas', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}roll <cuantas veces lo quieres girar> <cuantas caras>', value='Junto a este comando tendraws que poner las veces que quieres tirar y las caras.', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}md5 <tu frase>', value='Traduce tu palabra/frase a md5', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}sha256 <tu frase>', value='Traduce tu palabra/frase a sha256', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}edited [edited] <tu frase>', value=f'Esto es un poco complicado tienes que poner `|` donde quieres que valla la marca de editado. ejemplo: **{ctx.prefix}edited hola soy | mauro**', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}fml', value='Te dice historias graciosas de personas', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}randomavatar', value='Te da un avatar random', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}sha512 <tu frase>', value='Traduce tu palabra/frase a sha512', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}secret', value='Tengo un secreto para ti', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}factcore', value='¿Quieres algo interesante?', inline=False)
            embed2.add_field(name=f'•| {ctx.prefix}rhyme [palabra]', value='Vera si hay una letra repetida en tu palabra', inline=False)
            embed2.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga {ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed2.add_field(name="Unete a nuestro servidor de ayuda", value="**servidor -->  ( https://discord.gg/4gfUZtB )**")


            embed2.set_footer(text=ctx.author.name + "   pag(2/4)   ", icon_url=ctx.author.avatar_url)


            embed3 = discord.Embed(title="COMANDOS DE DIVERSION                   pag(3/4)", timestamp=datetime.datetime.utcnow(), description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", colour=color)
            embed3.set_author(name="Ayuda para comandos de fun 3", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed3.add_field(name=f'•| {ctx.prefix}uppercase <tu frase>', value='pone tu palabra/frase en mallusculas', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}lowercase <tu frase>', value='pone tu palabra/frase en minusculas', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}fight', value='Batalla contra un usuario y escoje arma', inline=False)
            embed3.add_field(name=f"•| {ctx.prefix}honkhonk", value="No hay muchos de estos memes pero molan", inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}notu', value='Respondera con "no tu"', inline=False)
            # embed3.add_field(name='•| fortune', value='Eleccion random de que pasara (esta en ingles)', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}intellect <tu frase>', value='Pondra tu frase/palabra con mayusculas y minusculas random para poder vacilar a tus amigos', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}hack <usuario>', value='Hackea a alguien que odies', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}animequote', value='Te dara una frase de algun anime', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}anime <Tipo de anime>', value='Busca tu anime preferido', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}guapo [usuarop]', value='Mira que guapo es el avatar del usuario', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}letra_repetida <palabra>', value='Haver cuantas letras hay repetidas en esta palabra', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}djenerate', value='Te dara un tab aleatorio de Djent', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}binario <Texto>', value='Traduce el texto que quieras a binario', inline=False)
            # embed3.add_field(name=f'•| {ctx.prefix}binario <Texto>', value='Traduce el texto que quieras a binario', inline=False)
            embed3.add_field(name=f'•| {ctx.prefix}inspirobot', value='¿Frustado?', inline=False)
            embed3.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga {ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed3.add_field(name="Unete a nuestro servidor de ayuda", value="**servidor -->  ( https://discord.gg/4gfUZtB )**")

            embed3.set_footer(text=ctx.author.name + "   pag(3/4)   ", icon_url=ctx.author.avatar_url)

            embed4= discord.Embed(title="COMANDOS DE DIVERSION                   pag(4/4)", timestamp=datetime.datetime.utcnow(), description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", colour=color)
            embed4.set_author(name="Ayuda para comandos de fun 4", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed4.add_field(name=f'•| {ctx.prefix}googledoodle', value='Estate al dia con google', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}bored', value='¿Aburrido?', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}imgascii [Usuario]', value='Mira tu perfil con caracteres de teclado', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}joke', value='¿Te are reir?', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}httpdog o httpduck [Estado del servidor]', value='Mira tu perfil con caracteres de teclado', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}garfield', value='Este comando te dara un comic de garfield', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}tts [numeros, frases, lo qu quieras]', value='Se reproducira un audio con lo que tu quieras', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}avmeme <@mecion> [texto de arriba] [texto de abajo]', value=f'Ejemplo: `{ctx.prefix}avmeme <@Alguien> [Texto de arriba] [Texto de abajo]`', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}pokeinfo [pokemon]', value='¿Te gustan los pokemons? Esto sera perfecto para ti.', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}tv [serie o pelicula]', value='Busca la serie que quiras **(Titulo en ingles)**.', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}ascii [palabra]', value='TEXTO GRANDEEEE', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}nasa [Termino]', value='Te dare informacion de el espacio', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}lyrics <Cantante/banda>', value='1... 2... 3... 4... yeahhh', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}nuke <usuario>', value='Puhhhhh *efectos especiales*', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}mc <nombre>', value='[Me encanta el minecraft ¿Y a ti?](https://youtu.be/EhdkGOoOOuo?t=130)', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}pass_guess <contraseña>', value='Yo creo que el titulo lo ha dicho todo **MAXIMO 10 CARACTERES**', inline=False)
            embed4.add_field(name=f'•| {ctx.prefix}password <Longitud>', value='Te creo una contraseña segura', inline=False)
            embed4.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga {ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed4.add_field(name="Unete a nuestro servidor de ayuda", value="**servidor -->  (https://discord.gg/4gfUZtB)**")

            embed4.set_footer(text=ctx.author.name + "   pag(4/4)   ", icon_url=ctx.author.avatar_url)
            
            
            embedf= discord.Embed(title="COMANDOS DE JUEGOS                   ", timestamp=datetime.datetime.utcnow(), description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", colour=color)
            embedf.add_field(name='-- JUEGOS --', value='Seccion de juegos', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}hangman', value='Te dara Info para jugar al hangman', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}connect4', value='Se juega con personas pero si no pones a nadie te salen las reglas', inline=False)
            # embedf.add_field(name=f'•| {ctx.prefix}chess', value='Se juega con personas pero si no pones a nadie te salen las reglas', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}rps', value='Piedra papel o tijera...', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}mathquiz', value='¿Eres bueno con las mates?', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}trivia', value='¿Eres bueno con las mates?', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}mathquiz', value='Siencias HUUUUUUUUUUUUUUUUUUUUUUUUU', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}guessnum', value='Intenta adivinar el numero', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}guessavatar', value='Intenta adivinar el avatar de un usuario random', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}bomb', value='Desactiva la bomba', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}geoquiz', value='¿Cuanto conozes ha este mundo?', inline=False)
            embedf.add_field(name=f'•| {ctx.prefix}minesweeper [Bombas] [Filas] [Columnas]', value='**BOOM** Ups...', inline=False)



            msg_fun = await ctx.send(embed=embed1)
            # await ctx.send(embed=embed2)

            for emo in emos_fun:
                await msg_fun.add_reaction(emo)

        


            def check_f(reaction, user):
                return (
                    reaction.emoji in emos_fun.keys()
                    and user == ctx.author
                    and reaction.message.id == msg_fun.id
                )

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=check_f)
                except Exception as e:
                    print("[Log] un error: " + e)
                else:
                    em = None
                    if reaction.emoji == '🔴':
                        await msg_fun.delete()
                        break
                    elif reaction.emoji == '1️⃣':
                        em = embed1
                    elif reaction.emoji == '2️⃣':
                        em = embed2
                    elif reaction.emoji == '3️⃣':
                        em = embed3
                    elif reaction.emoji == '4️⃣':
                        em = embed4
                    elif reaction.emoji == '🎮':
                        em = embedf
                    await msg_fun.edit(embed=em)
                    await msg_fun.remove_reaction(reaction, user)
                            

       
        
        if sec=="img":
            embedimg_1 = discord.Embed(title="COMANDOS PARA IMAGENES  pag(1/3)", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embedimg_1.set_author(name="Ayuda para comandos imagenes", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embedimg_1.add_field(name='argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requieres en base a uso', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}infinite', value='Un fig infinito', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}dad', value='Callate mi padre trabaja en discord.', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}captcha <Texto>', value='Te creara un captcha customatizable\n\n', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}meme', value='Recibiras un meme random de los trendings de reddit\n\n', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}programmerhumor', value='Memes de programador', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}qr o barcode <Texto>', value='Te creara un codigo qr customatizable\n\n', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}pikachu', value='pika pika... CHUUUU', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}wasted <usuario>', value='Haz que alguien muera', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}sleep', value='Buenas noches...', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}pat', value='Enfadate', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}shrug', value='Sientete ofendido', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}pout', value='Demuestra quien eres', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}facepalm', value='Agh...', inline=False)
            embedimg_1.add_field(name=f'•| {ctx.prefix}cry', value='-lloras-', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}gray <Usuario>', value='Pones el avatar del usuario en gris', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}glass <Usuario>', value='El usuario esta atrapado en hielo', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}sepia <Usuario>', value='No se como explicarlo', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}gay <Usuario>', value='Pones el avatar del usuario en gris', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}scroll <Texto[maximo 100]>', value='Pone tu texto en un papel sagrado', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}facts <Texto[maximo 100]>', value='Mira el libro', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}nichijou <palabra>', value='Que te diran...', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}didyoumean <[Texto1]> <texto2>', value=f'escribe {ctx.prefix}didyoumean [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}supreme [--dark < o > --light] <Texto>', value='Creara una imagen con el fondo personalizable a blanco y negro como vemos en el ejemplo y luego con su texto', inline=False)            
            embedimg_1.add_field(name=f'•| {ctx.prefix}trash <Usuario>', value='Tira a alguien por la basura', inline=False) 
            embedimg_1.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            # LIMITE

            embedimg_2 = discord.Embed(title="COMANDOS PARA IMAGENES  pag(2/3)", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embedimg_2.add_field(name=f'•| {ctx.prefix}facepalm', value='Agh...', inline=False)
            embedimg_2.add_field(name=f'•| {ctx.prefix}cry', value='-lloras-', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}gray <Usuario>', value='Pones el avatar del usuario en gris', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}glass <Usuario>', value='El usuario esta atrapado en hielo', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}sepia <Usuario>', value='No se como explicarlo', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}gay <Usuario>', value='Pones el avatar del usuario en gris', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}scroll <Texto[maximo 100]>', value='Pone tu texto en un papel sagrado', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}facts <Texto[maximo 100]>', value='Mira el libro', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}nichijou <palabra>', value='Que te diran...', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}didyoumean <[Texto1]> <texto2>', value=f'escribe {ctx.prefix}didyoumean [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}supreme [--dark < o > --light] <Texto>', value='Creara una imagen con el fondo personalizable a blanco y negro como vemos en el ejemplo y luego con su texto', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}trash [Usuario]', value='Tira a alguien por la basura', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}clyde [Usuario]', value='¿Sabes ese bot?', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}challenge  [texto]', value='Logro conseguido', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}call [texto]', value='Lamma a alguien', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}amiajoke [Usuario]', value='¿Soy una broma para ti?', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}drake', value='No, SI', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}salty [usuario]', value='How estas un poco salado', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}floor [texto]', value='How estas un poco salado', inline=False)           
            embedimg_2.add_field(name=f'•| {ctx.prefix}ship [usuario]', value='Te quiero..', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}jokeoverhead [usuario]', value='Eres una broma HA', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}bad [usuario]', value='Ha que te regaño', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}magik [usuario]', value='¿Esto es normal?', inline=False)            
            embedimg_2.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            

            embedimg_3 = discord.Embed(title="COMANDOS PARA IMAGENES  pag(3/3)", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embedimg_3.add_field(name=f'•| {ctx.prefix}changemymind <texto>', value=f'Maubot es increible **Cambia mi mente**', inline=False)            
            embedimg_3.add_field(name=f'•| {ctx.prefix}trumptweet <Texto>', value=f'D. Trump a publicado un mensaje:', inline=False)            
            embedimg_3.add_field(name=f'•| {ctx.prefix}iphonex [Usuario]', value=f'Estas atrapado en un movil **LOL**', inline=False)            
            embedimg_3.add_field(name=f'•| {ctx.prefix}awooify [Usuario]', value=f'QUE MONOO/A', inline=False)            
            embedimg_3.add_field(name=f'•| {ctx.prefix}threats [usuario]', value=f'No te me hacerques. Tengo un cuchillo y **no** se usarlo', inline=False)            
            embedimg_3.add_field(name=f'•| {ctx.prefix}baguette [Usuario]', value=f'Te vas a poner gorda **xd**', inline=False)            
            embedimg_3.add_field(name=f'•| {ctx.prefix}captcha_user [Usuario]', value=f'Haveces pienso que soy un bot...', inline=False)            
            embedimg_3.add_field(name=f'•| {ctx.prefix}lolice [Usuario]', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            
            # embedimg_3.add_field(name=f'•| {ctx.prefix}philosoraptor <[texto]><[texto]>', value=f'escribe {ctx.prefix}philoraptor [tu texto][tu texto] y mira lo que evia **los dos textos tienen que estar entre brackets**', inline=False)            


            embedimg = await ctx.send(embed=embedimg_1)


            await embedimg.add_reaction('◀️')
            await embedimg.add_reaction('▶️')
            await embedimg.add_reaction('🖼️')
            await embedimg.add_reaction('🟥')

            emojis = {
                '🟥': 0, 
                '🖼️': 1, 
                '▶️': 2, 
                '◀️': 3,
            }



            def check_img(reaction, user):
                return (
                    reaction.emoji in emojis.keys()
                    and user == ctx.author
                    and reaction.message.id == embedimg.id
                )

            while True:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=check_img)
                except Exception as e:
                    print(e)
                else:
                    em = None
                    if reaction.emoji == '🟥':
                        await embedimg.delete()
                        break
                    elif reaction.emoji == '◀️':
                        em = embedimg_1
                    elif reaction.emoji == '▶️':
                        em = embedimg_2
                    elif reaction.emoji == '🖼️':
                        em = embedimg_3
                    await embedimg.edit(embed=em)
                    await embedimg.remove_reaction(reaction, user)
            
        if sec == "ban":
            print("[Log] Ayuda de banear enviada")

            embed = discord.Embed(title="COMANDOS DE BANEAR", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed.set_author(name="Ayuda para comandos de banear", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed.add_field(name='Advertencia:', value='Este comando para banear a gente, tienes que tener (administrador) o (tener permisos para banear)\n\n', inline=False)
            embed.add_field(name='argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requieres en base a uso', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}ban <usuario>', value=f'Cuando esté comando es utilizado tienes que meter otro argumento y es la mencion del usuario al que quieres mutear, `ex: {ctx.prefix}mute @usuario`\n\n')
            embed.add_field(name=f'•| {ctx.prefix}unban <id de usuario>', value='Al usar este commando el usuario tiene que estar baneado primero, y luego tener permisos (obiamente), por ultimo tienes que saver que se usa como el commando de (ban)\n\n')
            embed.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga "{ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed.add_field(name="Unete a nuestro servidor de ayuda", value="servidor -->  **( https://discord.gg/4gfUZtB )**")

            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

            msg = await ctx.send(embed=embed)


        if sec == "musica":
            # print("Ayuda de voz enviada")

            embed = discord.Embed(title="COMANDOS DE VOZ", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed.set_author(name="Ayuda para comandos de voz", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed.add_field(name='argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requieres en base a uso', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}join', value='Cuando esté en un canal de voz, use esto para que el bot se una a dicho canal de voz', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}leave', value='Cuando desee que el bot salga del canal de voz (debe estar en el canal con el bot para que esto funcione)', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}play <palabras claves>', value='Se usa para reproducir con palabras claves o links de youtube **tambien sirve para poner canciones en la cola**', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}summon', value='Si el robot ya esta conectado pon este commando para que se mueva de canal', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}next', value='Si el audio está en cola, esto detendrá el audio que se está reproduciendo actualmente y comenzará el siguiente.',  inline=False)
            embed.add_field(name=f'•| {ctx.prefix}pause', value='Esto pausará la reproducción de audio', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}resume', value='Resumira la cancion actual **Necesita estar parada primero**', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}shuffle', value='Barajeas las canciones de la cola', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}loop', value='Se cambia el modo del loop para que se repita o no', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}queue [numero de la pagina]', value='Puedes ver cuantas cancione hay en la cola y si hay mas de 10 en una pagina se creara otra y trendras que poner el numero de la pagina', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}remove <numero de la cancion>', value='Elimina la cancion que quieras', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}now', value='Con este comando podras ver lam cancion actual que se esta reproduciendo', inline=False)
            embed.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga "{ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed.add_field(name="Unete a nuestro servidor de ayuda", value="servidor -->  **( https://discord.gg/4gfUZtB )**")

            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            
            msg = await ctx.send(embed=embed)


        if sec == "animals":

            embed = discord.Embed(title="COMANDOS PARA ANIMALES", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed.add_field(name='-- ANIMALES --', value='Que monooooooooooos 🐶', inline=False)         
            embed.add_field(name=f'•| {ctx.prefix}dog', value='Si tu pones este commando te saldra una foto de un perro random **advertencia: demasiado monos**', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}fox', value='Si tu pones este commando te saldra una foto de un zorro random **advertencia: demasiado monos**\n\n', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}bird', value='Si tu pones este commando te saldra una foto de un pajaro random **advertencia: demasiado monos**\n\n', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}cat', value='Si tu pones este commando te saldra una foto de un gato random **advertencia: demasiado monos**\n\n', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}duck', value='Si tu pones este commando te saldra una foto de un pato random **advertencia: demasiado monos**\n\n', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}coffee', value='Si tu pones este commando te saldra una foto de un cafe random\n\n', inline=False)

            msg = await ctx.send(embed=embed)

        if sec == "currency":
            embed = discord.Embed(title="AYUDA CURRENCY", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed.set_author(name="Ayuda para los comandos de currency", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed.add_field(name='argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requieres en base a uso', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}balance [usuario]', value='Si usas este commando el robot enseñara un embed de el dinero que tienes (se empieza con 100.0).', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}beg', value='Una persona te dara dinero y se guardara en tu prefil.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}top [numero de usuarios]', value='Te dara una lista de los 10 usuarios mas ricos de tu servidor **(Necesitas tener 10 usuarios en tu servidor para hacer este commando)**.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}transfer <usuario> <Monedas>', value=f'Al lado de este commando pon el usuario al que quieras transferir dinero y luego pon cuanto quieres transferir **ej: {ctx.prefix}transfer @user 100**.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}slots <Monedas>', value=f'Juega en el casino haver si tienes **suerte**.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}deposit <Monedas>', value=f'Deposita dinero al banco.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}withdraw <Monedas>', value=f'Saca dinero del banco.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}shop', value=f'¿Que ara en la tienda?', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}buy', value=f'Comprate algo en la tienda', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}bag', value=f'Puedes irar tu inventario', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}sell <objeto> [cantidad]', value=f'Vende lo que no necesites - wallapop', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}rob <Usuario>', value=f'Ladroon un ladrrooon.', inline=False)
            embed.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga "{ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed.add_field(name="Unete a nuestro servidor de ayuda", value="servidor -->  **( https://discord.gg/4gfUZtB )**")

            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            
            msg = await ctx.send(embed=embed)



        if sec == "general":

            embed = discord.Embed(title="AYUDA PARA COMANDOS GENERALES", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed.add_field(name='argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requieres en base a uso', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}wikipedia <La busqueda>', value='Te dara un resumen de wikipedia pero tienes que poner una busqueda muy especifica.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}youtube <busqueda>', value='Te dara un video a base de tus palabras claves.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}ping', value='Mira la tardanza de respuesta del bot.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}avatar [usuario]', value='Puedes ver la imagen del usuario que quieras.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}owner', value='Te dice el creador del servidor.', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}permisos [usuario]", value='Te dicen todo lo que puede hacer un usuario **SOLO EL OWNER PUEDE USARLO**', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}poll <pregunta>", value='Una pregunta con varias opciones', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}quickpoll <pregunta> <respuestas>", value='Una pregunta rapida', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}userinfo [usuario]", value='Mira la informacion de la gente qur tu quieras', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}palmadas <tu frase>", value='Cambia los espacion por 👏', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}translate [tu frase]", value='Traduce lo que quieras al ingles', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}vanish", value='Desaparece del servidor', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}weather <Ciudad>", value='Mira el tiempo en tu calle', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}recipe <Plato de primera>", value='Haver que hat de cocinar hoy...', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}isitdown <link de web>", value='Mira el ping the alguna pagina web', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}spotify [usuario o id]", value='**Tienes que tener** el estado quitado y escuchando musica para este comando', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}itunes <Cancion>", value='Haver si encuentras alguna musica way', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}bots", value='Mira la lista de bots', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}iotd", value='Imagen del dia', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}joinposition", value='Mira tu posicion dependiendo de hace cuando te has unido', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}ufo", value='Me e colado en el area 51 no se lo digas a nadie', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}AFK [Razon]", value='¿Necesitas ir al baño? Yo te cubro.', inline=False)
            embed.add_field(name=f"•| {ctx.prefix}invites", value='Sopongo que abras ayudado a este servidor **¿no?**.', inline=False)
            embed.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga "{ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed.add_field(name="Unete a nuestro servidor de ayuda", value="servidor -->  **( https://discord.gg/4gfUZtB )**")

            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)

            msg = await ctx.send(embed=embed)


        if sec == "lang":
            
            embed = discord.Embed(title="AYUDA DE LANG", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", colour=color)

            x = 45
            for index in LANGUAGES["array"]:
                # print(LANGUAGES["array"][index]["command"])
                embed.add_field(name=ctx.prefix + LANGUAGES["array"][index]["command"] + " | " + LANGUAGES["array"][index]["version"], value="\uFEFF", inline=False)

            msg = await ctx.send(embed=embed)

        if sec == "mates":

            embedM = discord.Embed(title="AYUDA DE MATES", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", colour=color)
            embedM.add_field(name='argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requiere en base a uso', inline=False)
            embedM.add_field(name=f'•| {ctx.prefix}sum <numbero1> <numero2>', value='numero1 **+** numero2 = (respuesta). (Pero sin el +, ej: {ctx.prefix}sum 1 3)', inline=False)
            embedM.add_field(name=f'•| {ctx.prefix}mul <numbero1> <numero2>', value='numero1 **x** numero2 = (respuesta). (Pero sin el x, ej: {ctx.prefix}mul 3 5)', inline=False)
            embedM.add_field(name=f'•| {ctx.prefix}div <numbero1> <numero2>', value='numero1 **/** numero2 = (respuesta). (Pero sin el /, ej: {ctx.prefix}div 90 10)', inline=False)
            embedM.add_field(name=f'•| {ctx.prefix}restar <numbero1> <numero2>', value='numero1 **-** numero2 = (respuesta). (Pero sin el -, ej: {ctx.prefix}res 10 5)', inline=False)
            embedM.add_field(name=f'•| {ctx.prefix}rz <numbero>', value='Te busca la raiz cuadrda de lo que quieras', inline=False)
            embedM.add_field(name=f'\uFEFF', value='\uFEFF', inline=False)
            embedM.add_field(name=f'•| {ctx.prefix}discordpy [busqueda]', value='Progamadores aqui teneis', inline=True)
            embedM.add_field(name=f'•| {ctx.prefix}pythondocs [busqueda]', value='Progamadores de pytohn aqui teneis')
            embedM.add_field(name=f'•| {ctx.prefix}help lang', value='Progamadores aqui teneis', inilne=False)
            embedM.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, "{ctx.prefix}_bot config" y crea un mensaje para la configuracion del robot, para ver toda la información del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embedM.add_field(name="Únete a nuestro servidor de ayuda", value="servidor -> **( https://discord.gg/4gfUZtB )**")

            msg = await ctx.send(embed=embedM)



        if sec == "channel":

            embed = discord.Embed(title="AYUDA CANALES DE TEXTO", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed.set_author(name="Ayuda para los comandos para los canales", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed.add_field(name=f'argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requiere en base a uso', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}new_category <nombre de la categoria>', value='Alado de este commando por el nombre que le vas a poner a la categoria.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}new_textchannel <nombre de el canal>', value='Alado de este commando por el nombre que le vas a poner al canal de texto.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}help ban', value='Una gia para banear agente y al igual que expulsar **tienes que tener permisos**', inline=False)
            # embed.add_field(name=f'•| {ctx.prefix}help mute', value='Exactamente igual que expulsar y banear **tienes que tener permisos**', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}new_voicechannel <nombre de el canal>', value='Alado de este commando por el nombre que le vas a poner al canal de voz.', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}kick <usuario>', value='Puedes expulsar a la gente con este comando poniendo el nombre del usuario. **Advertencia: tienes que tener permisos para expulsar**',  inline=False)
            embed.add_field(name=f'•| {ctx.prefix}infoserver', value='Al usar este commando te saldra un mensaje de la informacion del servidor como; creador, id, etc', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}warn <Usuario> [razon]', value='Pon una guarnicion al usuario que se porte mal', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}unwarn <Usuario>', value='Pon una guarnicion al usuario que se porte mal', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}warnlist [Usuario]', value='Pon una guarnicion al usuario que se porte mal', inline=False)
            embed.add_field(name=f'•| {ctx.prefix}kick <Usuario> [razon]', value='Expulsa al que quieras', inline=False)
            embed.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, haga "{ctx.prefix}_bot config", esto creará un mensaje para la configuracion del robot, para ver toda la informacion del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed.add_field(name="Unete a nuestro servidor de ayuda", value="servidor -->  **( https://discord.gg/4gfUZtB )**")


            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            
            msg = await ctx.send(embed=embed)




        if sec=="creador":
            if ctx.author.id == 700812754855919667:
                embed = discord.Embed(title="AYUDA PARA MI CREADOR", timestamp=datetime.datetime.utcnow(), colour=color)
                embed.set_author(name="Ayuda para los comandos para los canales")
                embed.add_field(name=f'•| {ctx.prefix}logout', value='Se apage el robot.', inline=False)
                embed.add_field(name=f'•| {ctx.prefix}cerrar', value='Se desactiva del todo.', inline=False)
                embed.add_field(name=f'•| {ctx.prefix}reload <nombre>', value='Reinicia algun cog.', inline=False)
                embed.add_field(name=f'•| {ctx.prefix}rp <Usuario id> <respuesta>', value='Enviar respuesta a un usuario.', inline=False)
                msg = await ctx.send(embed=embed)
            if not ctx.author.id == 700812754855919667:
                await ctx.send("No tienes permisos para ver esta lista de comandos")



        if sec!="creador" and sec!="lang" and sec!="animals" and sec!="img" and sec!="mates" and sec!="mute" and sec!="musica" and sec!="ban" and sec!="fun" and sec!="currency" and sec!="channel" and sec!="general":
            print("[Log] Ayuda enviada")

            embed = discord.Embed(title="AYUDA", description=f"Hola, mi prefijo actualmente es `{ctx.prefix}`. Si quieres contactar a mi creador siempre puedes unirte a [mi servidor](https://discord.gg/4gfUZtB), o escribe <@730124969132163093> para conocerme.", timestamp=datetime.datetime.utcnow(), colour=color)
            embed.set_author(name="Ayuda para los comandos", icon_url="https://img.icons8.com/color/48/000000/help--v1.png")
            embed.add_field(name='argumentos', value='> `<>` » Requerido\n> `[]` » opcional\n> `{}` » Se requiere en base a uso', inline=False)
            embed.add_field(name=f'💰  | {ctx.prefix}help currency', value='Con este comando podrás ver todos los comandos de currency.', inline=False)
            embed.add_field(name=f'🌏  | {ctx.prefix}help general', value='Mira los comandos comunes para el robot.', inline=False)
            embed.add_field(name=f'🔢  | {ctx.prefix}help mates', value='Por si necesitas ayuda con las mates 😉', inline=False)
            embed.add_field(name=f'⚙️  | {ctx.prefix}_bot <info | config>', value=f'Escoje este comando para saber su info con **_bot info** o poniendo **_bot config** para configurar.', inline=False)
            embed.add_field(name=f'👮  | {ctx.prefix}help channel', value=f'Mira todos los camandos para los canales. **Advertencia: ¡Tienes que tener permisos de editar canales!**.', inline=False)
            embed.add_field(name=f'⭐  | {ctx.prefix}help creador', value=f'Solo el creador puede verlo.', inline=False)
            embed.add_field(name=f'🖼️  | {ctx.prefix}help img', value=f'Mira las opciones que tienes con las imagenes.', inline=False)
            embed.add_field(name=f'🎉  | {ctx.prefix}help fun', value=f'¿Aburrido? haver si algo te puede alegrar el dia.', inline=False)
            embed.add_field(name=f'🐶  | {ctx.prefix}help animals', value=f'Mira las opciones que tienes con los animales.', inline=False)
            embed.add_field(name=f'🎵  | {ctx.prefix}help musica', value=f'Podras ver todos los comandos de voz', inline=False)
            embed.add_field(name="Informacion importante", value=f'```Para comenzar a configurar el bot, "{ctx.prefix}_bot config" y crea un mensaje para la configuracion del robot, para ver toda la información del bot pon "{ctx.prefix}_bot info".```', inline=False)
            embed.add_field(name="Únete a nuestro servidor de ayuda", value="servidor -->  **(https://discord.gg/4gfUZtB)**")


            embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
            
            msg = await ctx.send(embed=embed)


        # await ctx.message.add_reaction('📝')


def setup(bot):
    bot.add_cog(Help(bot))