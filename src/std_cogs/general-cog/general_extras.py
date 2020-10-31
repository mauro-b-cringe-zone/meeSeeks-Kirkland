import discord
from discord.ext import commands
import time
import datetime
import asyncio
from termcolor import cprint
import re
import random
import aiohttp
import json
from utils.hack import hackflow
from utils.fun.lists import drunkaf, fight_results, insults, honkhonkfgt
import hashlib
from os import environ as env
color = int(env["COLOR"])

class GeneralExtra(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # @commands.command(description="Busca lago en Youtube", usage="")
    # @commands.cooldown(1, 15, commands.BucketType.user)
    # async def youtube(self, ctx, *search):
    #     import urllib.parse
    #     import urllib.request
    #     query_string = urllib.parse.urlencode({'search_query': search})
    #     html_content = urllib.request.urlopen('http://www.youtube.com/results?'+str(query_string))
    #     search_results = re.findall('href=\"\\/watch\\?v=(.{11})', html_content.read().decode())
    #     print(search_results)
    #     await ctx.send('https://www.youtube.com/watch?v='+str(search_results[0]))

    # BUSCADOR DE IMAGENES

    ############################################
    # SYSTEMA DE NIVELES | no palabrotas |spam #
    ############################################

    @commands.command(description="Cambia el nombre del robot", usage="[nombre]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def rename_bot(self, ctx, *, text='Maubot'):
        await ctx.message.guild.me.edit(nick=text)
        await ctx.send(f'Apodo establecido a **{text}**')



    # JUEGOS





    # RE = NECESITA REPARACION

    @commands.command(aliases=["honk"], description="Honk?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def honkhonk(self, ctx):
        await ctx.send(random.choice(honkhonkfgt))

    @commands.command(description="Di algo", usage="[Mensage]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def say(self, ctx, *, message:str):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(message)

    # @commands.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def cat(ctx):
    #     async with ctx.session.get('htts://api.thecatapi.com/v1/images/search') as resp:
    #         if resp.status != 200:
    #             return await ctx.send('No se encontro ningun gato :(')
    #         js = await resp.json()
    #         await ctx.send(embed=discord.Embed(title='Meowwww').set_image(url=js[0]['url']))

    # @commands.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def dog(ctx):
    #     async with ctx.channel.typing():
    #         async with aiohttp.ClientSession() as cs:
    #             async with cs.get("https://random.dog/woof.json") as r:
    #                 data = await r.json()

    #                 embed = discord.Embed(title="Woof Woof", colour=color)
    #                 embed.set_image(url=data['url'])
    #                 embed.set_footer(text="http://random.dog/")

    #                 await ctx.send(embed=embed)

    @commands.command(description="Imagenes random de zorros")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fox(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Floof", colour=color)
                    embed.set_image(url=data['image'])
                    embed.set_footer(text="https://randomfox.ca/")

                    await ctx.send(embed=embed)


    @commands.command(description="OOOOOOOOOOOOOOOOOOOOOOOOOO")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def infinite(self, ctx):

        await ctx.send("https://media1.tenor.com/images/1c50bdbc44d5433fa3c67758dde775d2/tenor.gif")

    @commands.command(description="Chiste de padres")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dad(self, ctx):

        await ctx.send("https://cdn.discordapp.com/attachments/265156322012561408/744860278683992094/dad.jpg")

    # @commands.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def info_animal(ctx, animal: str):
    #     if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
    #         fact_url = f"https://some-random-api.ml/facts/{animal}"
    #         image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

    #         async with request("GET", image_url, headers={}) as response:
    #             if response.status == 200:
    #                 data = await response.json()
    #                 image_link = data["link"]

    #             else:
    #                 image_link = None

    #         async with request("GET", fact_url, headers={}) as response:
    #             if response.status == 200:
    #                 data = await response.json()

    #                 embed = Embed(title=f"Info de {animal.title()}",
    #                                 description=data["fact"],
    #                                 colour=colo)
    #                 if image_link is not None:
    #                     embed.set_image(url=image_link)
    #                 await ctx.send(embed=embed)
    #             else:
    #                 await ctx.send(f"El api a devuelto el estado '{response.status}'")

    #     else:
    #         embed_error = discord.Embed(title="No se a conseguido conseguir informacion", description="Aqui tienes una lista de animales validos\n> dog\n> panda\n> cat\n> koala\n> fox\n> bird", colour=color_error)
    #         await ctx.send(embed=embed_error)





    @commands.command(description="F en el chat")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def f(self, ctx):
        with open('./src/utils/languages/spanish.json', 'r') as f:
            Language = json.load(f)
        await ctx.send(Language.get("fun.respects", ctx).format(ctx.author, random.randint(1, 10000)))

    @commands.command(description="Buen meme")
    @commands.cooldown(1, 25, commands.BucketType.user)
    async def nicememe(self, ctx):
        await ctx.send("http://niceme.me")

    @commands.command(description="Espamea el server")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def spam(self, ctx):
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("./docs/images/spam.png"))

    # @commands.command()
    # async def random(ctx, subreddit: str=""):
    #     async with ctx.channel.typing():
    #         if ctx.reddit:

    #             chosen_subreddit = REDDIT_EANABLE_MEME_SUBREDDITS[0]
    #             if subreddit:

    #                 if subreddit in REDDIT_EANABLE_MEME_SUBREDDITS:
    #                     chosen_subreddit = subreddit

    #                 else:

    #                     ctx.send("Porfavor pon un subrredit valido")
    #             submissions = ctx.reddit.subreddit(chosen_subreddit).hot()

    #             post_to_pick = random.randqint(1,10)

    #             for i in range(0, post_to_pick):

    #                 submisions = next(x for x in submissions if not x.stickied) 
    #             await ctx.send(submissions.url)

    #         else:

    #             await ctx.send("Esto no funciona contacta al administrador o creador")


    @commands.command(description="Hackea ha alguien", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hack(self, ctx, *args):
        foundArgs, tohack = False, None
        try:
            tohack = ctx.guild.get_member(int(list(args)[0]))
            assert tohack!=None
            foundArgs = True
        except: 
            pass
        if len(ctx.message.mentions)<1 and not foundArgs:
            await ctx.send(f'Porfavor pon a alguien!\nejemplo: {ctx.prefix}hack <@'+str(ctx.message.author.id)+'>')
        if tohack==None: 
            tohack = ctx.message.mentions[0]
        console = 'maubot@HACKERMAN:/$ '
        if len(ctx.message.mentions)>0 or foundArgs:
            main = await ctx.send('Abriendo consola...\n```bash\nCargando...```')
            flow = hackflow(tohack)
            for i in range(0, len(flow)):
                console = console + flow[i][1:]
                await main.edit(content=f"```bash\n{console}```")
                await asyncio.sleep(random.randint(5, 6))
        else:
            console += 'ERROR: TAG INVALIDP.\nACCESO DENEGADO.\n\nCódigo cifrado en base64 con codificación hash:\n'+bin(ctx.message.author.name)+ '\n' + console
            await ctx.send(f'```bash\n{console}```')


    @commands.command(description="¿Cara o cruz?")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def coin(self, ctx):
        n = random.randint(0, 1)
        if n == 0:
            msg = "Cara"
        elif n == 1:
            msg = "Cruz"
        await ctx.send(f"Ha tocado: **{msg}**")

    @commands.command(description="¿Un gato?")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def b1nzy(self, ctx):
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("./docs/images/b1nzy_with_banhammer.png"))

    @commands.command(description="Russia")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def cykablyat(self, ctx):
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("./docs/images/cykablyat.jpg"))

    @commands.command(description="¿A que da miedo?")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def sombra(self, ctx):
        await ctx.send("```\n                       :PB@Bk:                         \n                   ,jB@@B@B@B@BBL.                     \n                7G@B@B@BMMMMMB@B@B@Nr                  \n            :kB@B@@@MMOMOMOMOMMMM@B@B@B1,              \n        :5@B@B@B@BBMMOMOMOMOMOMOMM@@@B@B@BBu.          \n     70@@@B@B@B@BXBBOMOMOMOMOMOMMBMPB@B@B@B@B@Nr       \n   G@@@BJ iB@B@@  OBMOMOMOMOMOMOM@2  B@B@B. EB@B@S     \n   @@BM@GJBU.  iSuB@OMOMOMOMOMOMM@OU1:  .kBLM@M@B@     \n   B@MMB@B       7@BBMMOMOMOMOMOBB@:       B@BMM@B     \n   @@@B@B         7@@@MMOMOMOMM@B@:         @@B@B@     \n   @@OLB.          BNB@MMOMOMM@BEB          rBjM@B     \n   @@  @           M  OBOMOMM@q  M          .@  @@     \n   @@OvB           B:u@MMOMOMMBJiB          .BvM@B     \n   @B@B@J         0@B@MMOMOMOMB@B@u         q@@@B@     \n   B@MBB@v       G@@BMMMMMMMMMMMBB@5       F@BMM@B     \n   @BBM@BPNi   LMEB@OMMMM@B@MMOMM@BZM7   rEqB@MBB@     \n   B@@@BM  B@B@B  qBMOMB@B@B@BMOMBL  B@B@B  @B@B@M     \n    J@@@@PB@B@B@B7G@OMBB.   ,@MMM@qLB@B@@@BqB@BBv      \n       iGB@,i0@M@B@MMO@E  :  M@OMM@@@B@Pii@@N:         \n          .   B@M@B@MMM@B@B@B@MMM@@@M@B                \n              @B@B.i@MBB@B@B@@BM@::B@B@                \n              B@@@ .B@B.:@B@ :B@B  @B@O                \n                :0 r@B@  B@@ .@B@: P:                  \n                    vMB :@B@ :BO7                      \n                        ,B@B                           ```")

    @commands.command(description="( ͡° ͜ʖ ͡° )")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lenny(self, ctx):
        await ctx.send("( ͡° ͜ʖ ͡° )")

class GeneralSecExtra(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="(╯°□°）╯︵ ┻━┻")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tableflip(self, ctx):
        await ctx.send("(╯°□°）╯︵ ┻━┻")

    @commands.command(description="┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def doubleflip(self, ctx):
        await ctx.send("┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻")

    @commands.command(description="¡¡¡Que careto!!!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def misc_weeb_face(self, ctx):
        await ctx.send("(・`ω´・)")

    @commands.command(description="︻芫═───")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gun(self, ctx):
        await ctx.send("︻芫═───")

    # @commands.command()
    # @commands.cooldown(1, 25, commands.BucketType.user)
    # async def ball(ctx, *, question:str):
    #     await ctx.send("{}: {}".format(ctx.author.name, random.choice(magic_conch_shell)))

    @commands.command(description="Insulta ha alguien", usage="[usuario]")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def insult(self, ctx, *, user:str):
        await ctx.send("{} {}".format(user, random.choice(insults)))

    @commands.command(description="AUUUUUUUUUUUUUEEEEEEEUAUUAE")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def actdrunk(self, ctx):
        await ctx.send(random.choice(drunkaf))

    @commands.command(description="Tedoy un -10 de 20", usage="[usuario]")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def rate(self, ctx, user:discord.User=None):
        with open('mauutils/languages/spanish.json', 'r') as f:
            Language = json.load(f)
        if user is None or user.id == ctx.author.id:
            await ctx.send(Language.get("fun.rate_author", ctx).format(random.randint(10)))
        elif user == ctx.commandsuser:
            await ctx.send(Language.get("fun.rate_self", ctx))
        else:
            await ctx.send(Language.get("fun.rate_user", ctx).format(user.name, random.randint(0, 10)))

    @commands.command(description="Mandame un mensage", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def plzmsgme(self, ctx, *, message:str):

        with open('./src/utils/languages/spanish.json', 'r') as f:
            Language = json.load(f)

        await ctx.author.send(message)
        await ctx.send(Language.get("fun.plzmsgme", ctx))

    @commands.command(description="Høla ¿unø que remplaze las øs y 0s?", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def twentyoneify(self, ctx, *, input:str):
        await ctx.send(input.replace("O", "Ø").replace("o", "ø"))

    @commands.command(description="Spell RED, LIAHWDIOAHWDOAWHDOAIWHDOAIWHDN", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spellout(self, ctx, *, msg:str):

        await ctx.send(" ".join(list(msg.upper())))


    @commands.command(description="egasnem nu", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reverse(self, ctx, *, msg:str):
        await ctx.send("🔁 " + msg[::-1])

    @commands.command(description="awldkhjAWOLIHDWOAIHDalkwjdKjdaldj", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def intellect(self, ctx, *, msg:str):
        await ctx.channel.trigger_typing()
        intellectify = ""
        for char in msg:
            intellectify += random.choice([char.upper(), char.lower()])
        await ctx.send(intellectify)


    @commands.command(description="Numero random (PUEDES PONER CUANTOS DIGITOS)", usage="[digito]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def randomnumber(self, ctx, *, digits:int=1):

        number = ""
        for i in range(digits):
            number += str(random.randint(0, 9))
        embed = discord.Embed(title="Numero random", description=number, colour=color)
        embed.set_footer(text=f"Numero random | {ctx.prefix}help para mas informacion")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, description="Gira el dado", usage="<dados><lados>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roll(self, ctx, dice_amount: int, sides: int):

        if dice_amount > 999:
            await ctx.send(f"{ctx.message.author.mention}, superaste el límite de la cantidad de dados de 999")
            return
        if sides > 999:
            await ctx.send(f"{ctx.message.author.mention}, superaste el límite del lado de los dados de 999")
            return
        if sides == 1: 
            await ctx.send(f"{ctx.message.author.mention}, No apunta a tirar un dado de 1 cara")
            return



        run_l1 = True
        dice_a1 = dice_amount
        total = 0
        dice_track = []  

        while run_l1:  
            if dice_a1 != 0:
                dice_roll = random.randint(1, sides)  # roll
                cprint("[Log]" + dice_a1, 'red')
                dice_track.append(dice_roll) 
                dice_a1 -= 1
            else:
                run_l1 = False

        for roll_num in dice_track:
            total += roll_num


        try:
            await ctx.send(f"{ctx.message.author.mention} a girado el dado {dice_amount} veces y {sides} caras. "
                        f"Total: {total}")
        except:
            await ctx.send("Soy una computadora que conozco, ¡pero eso es mucho incluso para mí!")

    @commands.command(description="9cdfb439c7876e703e307864c9167a15", usage="<mensage>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def md5(self, ctx, *, msg:str):
        await ctx.send("`{}`".format(hashlib.md5(bytes(msg.encode("utf-8"))).hexdigest()))\


    @commands.command(description="Pega ha alguien", usage="<usuario>[razon]")
    async def pegar(self, ctx, member: discord.Member, *, reason: str = "ninguna razon"):
        await ctx.send(f"{ctx.author.display_name} a pegado a {member.mention} por {reason}!")


    @commands.command(description="07123e1f482356c415f684407a3b8723e10b2cbbc0b8fcd6282c49d37c9c1abc", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sha256(self, ctx, *, msg:str):
        await ctx.send("`{}`".format(hashlib.sha256(bytes(msg.encode("utf-8"))).hexdigest()))

    @commands.command(description="3dd28c5a23f780659d83dd99981e2dcb82bd4c4bdc8d97a7da50ae84c7a7229a6dc0ae8ae4748640a4cc07ccc2d55dbdc023a99b3ef72bc6ce49e30b84253dae", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sha512(self, ctx, *, msg:str):
        await ctx.send("`{}`".format(hashlib.sha512(bytes(msg.encode("utf-8"))).hexdigest()))

class GeneralMasExtras(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="HOLA", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uppercase(self, ctx, *, msg:str):
        await ctx.send(msg.upper())

    @commands.command(description="hola", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lowercase(self, ctx, *, msg:str):
        await ctx.send(msg.lower())


    @commands.command(description="NO TU")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def notu(self, ctx):
        await ctx.message.delete()
        await ctx.send("no tu")

    # @commands.command()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def fortune(ctx):
    #     await ctx.send("```{}```".format(random.choice(fortunes)))

    # @commands.command()
    # async def owo(ctx, *, text:str):
    #     # RE
    #     print(owofy(text))
    #     await ctx.send(owoify(text))




    @commands.command(description="(PRAISE INTENSE)")
    async def praise(self, ctx):
        await ctx.send('https://i.imgur.com/K8ySn3e.gif')

    @commands.command(description="Que lio")
    async def css(self, ctx):
        await ctx.send('http://i.imgur.com/TgPKFTz.gif')


def setup(bot):
    bot.add_cog(GeneralExtra(bot))
    bot.add_cog(GeneralMasExtras(bot))
    bot.add_cog(GeneralSecExtra(bot))
