
import discord
from discord.ext import commands
import sys
from io import BytesIO
from requests import get
from aiohttp import ClientSession
from urllib.parse import quote_plus as urlencode
from PIL import Image, ImageFont, ImageDraw, GifImagePlugin, ImageOps, ImageFilter
import re
import random
from os import environ as env
color =   int(env["COLOR"]) 

def randomhash():
    hashh = ''
    for i in range(0, random.randint(13, 21)):
        hashh = hashh + random.choice(list('ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'))
    return hashh

def getUserAvatar(ctx, args, size=1024, user=None, allowgif=False):
    if len(list(args))==0:
        if allowgif: 
            return str(ctx.author.avatar_url).replace('.webp?size=1024', '.png?size'+str(size))
        else: 
            return str(ctx.author.avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', '.png?size'+str(size))
    if len(ctx.message.mentions)>0:
        if not allowgif:
            return str(ctx.message.mentions[0].avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', f'.png?size={size}')
        return str(ctx.message.mentions[0].avatar_url).replace('?size=1024', f'?size={size}')
    name = str(' '.join(list(args))).lower().split('#')[0]
    for i in ctx.guild.members:
        if name in str(i.name).lower():
            user = i; break
        elif name in str(i.nick).lower():
            user = i; break
    if user!=None:
        if not allowgif: 
            return str(user.avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', f'.png?size={size}')
        return str(user.avatar_url).replace('?size=1024', f'?size={size}')
    elif list(args)[0].isnumeric():
        if not allowgif: 
            return str(ctx.guild.get_member(int(list(args)[0])).avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', f'.png?size={size}')
        return str(ctx.guild.get_member(int(list(args)[0])).avatar_url).replace('?size=1024', f'?size={size}')
    if not allowgif: 
        return str(ctx.author.avatar_url).replace('.gif', '.webp').replace('.webp?size=1024', f'.png?size={size}')
    return str(ctx.author.avatar_url).replace('?size=1024', f'?size={size}')

def getUser(ctx, args, user=None, allownoargs=False):
    if len(list(args))==0:
        return ctx.author
    if len(ctx.message.mentions)>0: return ctx.message.mentions[0]
    name = str(' '.join(list(args))).lower().split('#')[0]
    for i in ctx.guild.members:
        if name in str(i.name).lower():
            user = i; break
        elif name in str(i.nick).lower():
            user = i; break
    if user!=None: 
        return user
    if list(args)[0].isnumeric():
        return ctx.guild.get_member(int(list(args)[0]))
    return ctx.author


class Img(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def urlify(self, word):
        return urlencode(word).replace('+', '%20')
        
    def imagefromURL(self, url): 
        return Image.open(BytesIO(get(url).content))

    def buffer(self, data):
        arr = BytesIO()
        data.save(arr, format='PNG')
        arr.seek(0)
        return arr

    def urltoimage(self, url):
        image = self.imagefromURL(url)
        return self.buffer(image)

    @commands.command(aliases=['dym'], description="$didyoumean [hola][adios]", usage="<[texto1]><[texto2]>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def didyoumean(self, ctx, *args):
        async with ctx.message.channel.typing():
            txt1, txt2 = self.urlify(str(ctx.message.content).split('[')[1][:-1]), self.urlify(str(ctx.message.content).split('[')[2][:-1])
            url='https://api.alexflipnote.dev/didyoumean?top='+str(txt1)+'&bottom='+str(txt2)
            await ctx.send(file=discord.File(self.urltoimage(url), 'didyoumean.png'))
                



    @commands.command(description="TU ERES {texto}", usage="texto")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nichijou(self, ctx, arg):
        async with ctx.message.channel.typing():
                embed = discord.Embed(title="dale al titulo para ver la animacion", url=f"https://i.ode.bz/auto/nichijou?text={arg}",colour=color)
                embed.set_image(url=f"https://i.ode.bz/auto/nichijou?text={arg}")
                await ctx.send(embed=embed)

    def urltoimage(self, url):
        image = self.imagefromURL(url)
        return self.buffer(image)

    @commands.command(description="Esta es tu casa", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trash(self, ctx, *args):
        async with ctx.message.channel.typing():
            av = ctx.message.author.avatar_url
            toTrash = getUserAvatar(ctx, args)
            url='https://api.alexflipnote.dev/trash?face='+str(av).replace('webp', 'png')+'&trash='+str(toTrash).replace('webp', 'png')
            data = self.urltoimage(url)
            await ctx.send(file=discord.File(data, 'trashed.png'))

    @commands.command(description="¿Soy una broma para ti?", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def amiajoke(self, ctx, *args):
        source = getUserAvatar(ctx, args)
        url = 'https://api.alexflipnote.dev/amiajoke?image='+str(source)
        await ctx.send(file=discord.File(self.urltoimage(url), 'maymays.png'))

    @commands.command(description="El bot te dice algo", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clyde(self, ctx, *args):
        if len(list(args))==0: 
            await ctx.send('Porfavor ingrese un texto...')
        else:
            async with ctx.message.channel.typing():
                url='https://nekobot.xyz/api/imagegen?type=clyde&text='+'+'.join(list(args))+'&raw=1'
                await ctx.send(embed=discord.Embed(color=color).set_image(url=url))


    @commands.command(description="FELICIDADES HAS CONSEGUIDO UN LOGRO", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def challenge(self, ctx, *args):
        if len(list(args))==0: 
            await ctx.send('¿Cual es el logro?')
        else:
            async with ctx.message.channel.typing():
                txt = '+'.join(args)
                url='https://api.alexflipnote.dev/achievement?text='+str(txt)
                await ctx.send(file=discord.File(self.urltoimage(url), 'minecraft_notice.png'))

    @commands.command(description="Llama ha alguien", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def call(self, ctx, *args):
        if len(list(args))==0: 
            await ctx.send('¿I tu llamada?')
        else:
            async with ctx.message.channel.typing():
                txt = '+'.join(args)
                url='https://api.alexflipnote.dev/calling?text='+str(txt)
                await ctx.send(file=discord.File(self.urltoimage(url), 'minecraft_notice.png'))

    def urlify(self, word):
        return urlencode(word).replace('+', '%20')

    @commands.command(description="$drake [hola][ola]", usage="<[texto1]><[texto2]>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def drake(self, ctx, *args):
        unprefixed = ' '.join(list(args))
        if list(args)[0]=='help' or len(list(args))==0:
            embed = discord.Embed(
                title='Ayuda para drake',
                description='Escribe lo siguiente:\n`'+str(ctx.prefix)+'drake [texto1] [texto2]`\n\nPor ejemplo:\n`'+str(ctx.prefix)+'drake [test1] [test2]`',
                colour=color
            )
            await ctx.send(embed=embed)
        else:
            async with ctx.message.channel.typing():
                txt1 = self.urlify(unprefixed.split('[')[1][:-1])
                txt2 = self.urlify(unprefixed.split('[')[2][:-1])
                url='https://api.alexflipnote.dev/drake?top='+str(txt1)+'&bottom='+str(txt2)
                data = self.urltoimage(url)
                await ctx.send(file=discord.File(data, 'drake.png'))


    @commands.command(description="Maubot no era el impostor", usage="<usuario>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def amongus(self, ctx):
        async with ctx.message.channel.typing():
            try:
                us = ctx.message.mentions[0]
            except:
                return await ctx.send("Menciona ha alguien porfavor")
            impostor = random.choice(["true", "false"])
            rcolor = random.choice(["black","blue","brown","cyan","darkgreen","lime","orange","pink","purple","red","white","yellow"])
            url = f"https://vacefron.nl/api/ejected?name={us.name.replace(' ', '%20')}&impostor={impostor}&crewmate={rcolor}"
            embed = discord.Embed(title=f"{us.name} {'no' if impostor == 'false' else 'si'} era el impostor", color=color).set_image(url=url)
            await ctx.send(embed=embed) 

    @commands.command(description="Don comendias", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def jokeoverhead(self, ctx, *args):
        async with ctx.message.channel.typing():
            av = getUserAvatar(ctx, args)
            url = 'https://api.alexflipnote.dev/jokeoverhead?image='+str(av)
            data = self.urltoimage(url)
            await ctx.send(file=discord.File(data, 'salty.png'))

    @commands.command(description="NIÑO MALO", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bad(self, ctx, *args):
        async with ctx.message.channel.typing():
            av = getUserAvatar(ctx, args)
            url = 'https://api.alexflipnote.dev/bad?image='+str(av)
            data = self.urltoimage(url)
            await ctx.send(file=discord.File(data, 'salty.png'))


    @commands.command(description="Suelo es lava LOL", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def floor(self, ctx, *args):
        if len(list(args))==0: text = 'Lo siento no he puesto argumentos'
        else: 
            text = str(' '.join(args))
        auth = str(ctx.message.author.avatar_url).replace('.gif', '.webp').replace('.webp', '.png')
        async with ctx.message.channel.typing():
            if len(ctx.message.mentions)>0:
                auth = str(ctx.message.mentions[0].avatar_url).replace('.gif', '.webp').replace('.webp', '.png')
                if len(args)>2: 
                    text = str(ctx.message.content).split('> ')[1]
                else:
                     text = 'Lo siento no he puesto argumentos'
            await ctx.send(file=discord.File(self.urltoimage('https://api.alexflipnote.dev/floor?image='+auth+'&text='+self.urlify(text)), 'floor.png'))


    @commands.command(description="¿Quieres ha alguien?", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tinder(self, ctx, *args):
        async with ctx.message.channel.typing():
            av = ctx.message.author.avatar_url
            match = getUserAvatar(ctx, args)
            url=f'https://useless-api.vierofernando.repl.co/tinder?image1={av}?size=1024&image2={match}?size=1024'
            if av == match:
                return await ctx.send("¿Te emparejas con tigo mismo?")
            await ctx.send(embed=discord.Embed(title="Soy perfectos el uno con el otro", color=color).set_image(url=url))

    def jsonisp(self, url):
        from requests import get as decodeurl
        return decodeurl(url).json()

    @commands.command(aliases=['programmerhumor','programmermeme','programming','programmer'], description="Solo los programadores lo entienden")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def programmingmeme(self, ctx):
        data = self.jsonisp('https://useless-api.vierofernando.repl.co/programmermeme')['url']
        return await ctx.send(embed=discord.Embed(title='Meme de programadores', color=color).set_image(url=data))

    def memegen(self, url):
        image = self.imagefromURL(url)
        area = (0, 20, list(image.size)[0], list(image.size)[1]-12)
        cropped_img = image.crop(area)
        data = self.buffer(cropped_img)
        return data

    @commands.command(description="$philosoraptor [lol][xd]", usage="<[texto1]><[texto2]>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def philosoraptor(self, ctx, *args):
        async with ctx.message.channel.typing():
            try:
                top = self.urlify(str(ctx.message.content).split('[')[1].split(']')[0])
                bott = self.urlify(str(ctx.message.content).split('[')[2].split(']')[0])
                name = str(ctx.message.content).split(ctx.prefix)[1].split(' ')[0]
                url='https://memegen.link/'+str(name)+'/'+str(top)+'/'+str(bott)+'.jpg?watermark=none'
                await ctx.send(file=discord.File(self.memegen(url), args[0][1:]+'.png'))
            except Exception as e:
                await ctx.send(f' | Error!\n```{e}```Parametro invalido.')



    @commands.command(description="Un avatar random", usage="[nombre]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def randomavatar(self, ctx, *args):
        if len(list(args))<1: 
            name = randomhash()
        else:
            name = ' '.join(list(args))
        url= 'https://api.adorable.io/avatars/285/{}.png'.format(name)
        await ctx.send(embed=discord.Embed(title="Avatar", url=url, colour=color).set_image(url=url))

    def insp(self, url):
        from requests import get as decodeurl
        return decodeurl(url).text

    @commands.command(aliases=['inspiringquotes', 'lolquote', 'aiquote', 'imagequote', 'imgquote'], description="Te inspirare")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def inspirobot(self, ctx):
        async with ctx.message.channel.typing():
            img = self.insp('https://inspirobot.me/api?generate=true')
            await ctx.send(file=discord.File(self.urltoimage(img), 'inspirobot.png'))

    @commands.command(description="DOODLY GOOGLY")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def googledoodle(self, ctx):
        from datetime import datetime as t
        wait = await ctx.send(f' | Espere... Esto puede tardar unos minutos...')
        data = self.jsonisp('https://www.google.com/doodles/json/{}/{}'.format(str(t.now().year), str(t.now().month)))[0]
        embed = discord.Embed(title=data['title'], colour=color, url='https://www.google.com/doodles/'+data['name'])
        embed.set_image(url='https:'+data['high_res_url'])
        embed.set_footer(text='Dia del evento: '+str('/'.join(
            [str(i) for i in data['run_date_array'][::-1]]
        )))
        await wait.edit(content='', embed=embed)

    def imagetoASCII(self, url):
        im = self.imagefromURL(url).resize((300, 300)).rotate(90).convert('RGB')
        im = im.resize((int(list(im.size)[0]/3)-60, int(list(im.size)[1]/3)))
        total_str = ""
        for i in range(im.width):
            for j in range(im.height):
                br = round(sum(im.getpixel((i, j)))/3)
                if br in range(0, 50): 
                    total_str += '.'
                elif br in range(50, 100): 
                    total_str += '/'
                elif br in range(100, 150): 
                    total_str += '$'
                elif br in range(150, 200): 
                    total_str += '#'
                else: 
                    total_str += '@'
            total_str += '\n'
        return total_str

    @commands.command(aliases=['img2ascii','imagetoascii','avascii','avatarascii','avatar2ascii','av2ascii'], description="Mira el avatar de alguien en caracteres", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def imgascii(self, ctx, *args):
        from requests import post
        url = getUserAvatar(ctx, args)
        wait = await ctx.send(' | Porfavor espera...')
        text = self.imagetoASCII(url)
        data = post("https://hastebin.com/documents", data=text)
        if data.status_code != 200: 
            return await wait.edit(content=" | Uups... un error")
        return await wait.edit(content='Echo | Puedes ver los resultados en **https://hastebin.com/{}**!'.format(data.json()['key']))
    
    @commands.command(aliases=['httpduck'], description="httpdog o httpduck (Estado del servido)", usage="<servidor>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def httpdog(self, ctx, *args):
        code = list(args)[0] if (len(list(args))!=0) else '404'
        url = 'https://random-d.uk/api/http/ABC.jpg' if ('duck' in ctx.message.content) else 'https://httpstatusdogs.com/img/ABC.jpg'
        try:
            await ctx.send(file=discord.File(
                self.urltoimage(url.replace('ABC', code)), 'httpdogduck.png'
            ))
        except:
            await ctx.send('> 404')

class ImgSecundario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def urlify(self, word):
        return urlencode(word).replace('+', '%20')
        
    def imagefromURL(self, url): 
        return Image.open(BytesIO(get(url).content))

    def buffer(self, data):
        arr = BytesIO()
        data.save(arr, format='PNG')
        arr.seek(0)
        return arr

    def urltoimage(self, url):
        image = self.imagefromURL(url)
        return self.buffer(image)

    def jsonisp(self, url):
        from requests import get as decodeurl
        return decodeurl(url).json()

    @commands.command(asliases=['ft'], description="Mira la tienda de fortnite")
    @commands.cooldown(1, 21600, commands.BucketType.user)
    async def fortnite(self, ctx):
        await ctx.send(embed=discord.Embed(color=color).set_image(url='https://api.nitestats.com/v1/shop/image?footer=%20Consigue%20APIs%20gratis%20Codigo-en:%20http://maubot.mooo.com&background=00000014.png&header=Tienda%20de%20fortnite'))

    @commands.command(description="Mira el avatar de alguien descontrolarse", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def magik(self, ctx, *args):
        source = getUserAvatar(ctx, args)
        await ctx.message.channel.trigger_typing()
        await ctx.send(file=discord.File(self.urltoimage(f'https://nekobot.xyz/api/imagegen?type=magik&image={source}&raw=1&intensity={random.randint(5, 10)}'), 'magik.png'))


    def gif2png(self, url):
        img = self.imagefromURL(url)
        img.seek(0)
        return self.buffer(img)
        
    @commands.command(description="Crea un meme con alguien", usage="<usuario> <[texto1]><texto2>")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def shoot(self, ctx, member: discord.Member):
        async with ctx.message.channel.typing():
            try:
                av = ctx.message.mentions[0].avatar_url
                await ctx.send(embed=discord.Embed(title=f"Headshoot, {random.randint(10, 700)} puntos", colour=color).set_image(url=f"https://api.no-api-key.com/api/v2/shoot?image={av.replace('.webp', '.jpg').replace('?size=1024', '')}"))
            except Exception as e:
                await ctx.send(f' | ¡Error!\n```{e}```Parametros invalidos. Ejemplo: `{ctx.prefix}shoot <@Alguien>`')


    @commands.command(description="Cambia mis opiniones", usage="[texto]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def changemymind(self, ctx, *args):
        if len(list(args))==0:
             await ctx.send(" | Necesitas un texto...")
        else:
            async with ctx.channel.typing():
                try:
                    data = self.jsonisp('https://nekobot.xyz/api/imagegen?type=changemymind&text='+'+'.join(list(args)))['message']
                    return await ctx.send(embed=discord.Embed(title='Changemymind', color=color).set_image(url=data))
                except Exception as e:
                    await ctx.send(" | ¡Oops! Un error generando tu meme; `"+str(e)+"`")

    @commands.command(description="Pon un tweet como si fueras trump", usage="<texto>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trumptweet(self, ctx, *args):
        if len(list(args))==0:
             await ctx.send(" | Necesitas un texto...")
        else:
            async with ctx.channel.typing():
                try:
                    data = self.jsonisp('https://nekobot.xyz/api/imagegen?type=trumptweet&text='+'+'.join(list(args)))['message']
                    return await ctx.send(embed=discord.Embed(title='Nuevo tweet', color=color).set_image(url=data))
                except Exception as e:
                    await ctx.send(" | ¡Oops! Un error generando tu meme; `"+str(e)+"`")


    @commands.command(description="QUE MONOOO @usuario", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def awooify(self, ctx, *args):
        source = getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            try:
                data = self.jsonisp('https://nekobot.xyz/api/imagegen?type=awooify&url='+source)["message"]
                return await ctx.send(embed=discord.Embed(title='QUE MONO/A', color=color).set_image(url=data))
            except Exception as e:
                await ctx.send(" | ¡Oops! Un error generando tu meme; `"+str(e)+"`")

    @commands.command(description="Me gusta  la tarta | A mi no", usage="<texto1> | <texto2>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def npc(self, ctx: commands.Context, *, args):
        if "|" in args:
            args = args.split(" | ")
            t1 = args[0]
            t2 = args[1]
            url = f"https://vacefron.nl/api/npc?text1={t1}&text2={t2}".replace(" ", "%20")
            await ctx.send(embed=discord.Embed(color=color).set_image(url=url))
        else: return await ctx.send("Escribe el segundo texto o pon **$help imgsecundario**")

    @commands.command(description="COME COME COME @usuario", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def baguette(self, ctx, *args):
        source = getUserAvatar(ctx, args)
        async with ctx.channel.typing():
            try:
                data = self.jsonisp('https://nekobot.xyz/api/imagegen?type=baguette&url='+source)["message"]
                return await ctx.send(embed=discord.Embed(title='Que hambre...', color=color).set_image(url=data))
            except Exception as e:
                await ctx.send(" | ¡Oops! Un error generando tu meme; `"+str(e)+"`")

    @commands.command(description="No se la diferencia", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def captcha_user(self, ctx, member):
        source = getUserAvatar(ctx, member)
        av = getUser(ctx, member).name
        async with ctx.channel.typing():
            try:
                data = self.jsonisp('https://nekobot.xyz/api/imagegen?type=captcha&url='+source+'&username='+av)["message"]
                return await ctx.send(embed=discord.Embed(title='Tu captcha', color=color).set_image(url=data))
            except Exception as e:
                await ctx.send(" | ¡Oops! Un error generando tu captcha; `"+str(e)+"`")

    @commands.command(description="Policia del lol ¿Què quiere?", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lolice(self, ctx, member):
        source = getUserAvatar(ctx, member)
        async with ctx.channel.typing():
            try:
                data = self.jsonisp('https://nekobot.xyz/api/imagegen?type=lolice&url='+source)["message"]
                return await ctx.send(embed=discord.Embed(title='¿Policia?', color=color).set_image(url=data))
            except Exception as e:
                await ctx.send(" | ¡Oops! Un error generando tu captcha; `"+str(e)+"`")

    @commands.command(description="GG", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def img_girl(self, ctx, member):
        source = getUserAvatar(ctx, member)
        async with ctx.channel.typing():
            try:
                data = self.jsonisp('https://nekobot.xyz/api/imagegen?type=trash&url='+source)["message"]
                return await ctx.send(embed=discord.Embed(title='hm...', color=color).set_image(url=data))
            except Exception as e:
                await ctx.send(" | ¡Oops! Un error generando tu captcha; `"+str(e)+"`")


    @commands.command(description="Haver si lo lees bien", usage="[usuario]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def captcha(self, ctx, *args):
        async with ctx.channel.typing():
            capt = 'Maubot' if len(list(args))==0 else '+'.join(list(args))
            await ctx.send(embed=discord.Embed(title="Captcha",).set_image(url='https://useless-api.vierofernando.repl.co/captcha?text={}'.format(capt)))


    @commands.command(description="Memes random para pasar el tiempo")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        data = self.jsonisp("https://meme-api.herokuapp.com/gimme")
        embed = discord.Embed(colour = color)
        from googletrans import Translator
        trans_title = Translator().translate(data["title"], src='en', dest='es')
        embed.set_author(name=trans_title.text, url=data["postLink"])
        if data["nsfw"]:
            return await ctx.send("Lo siento continuemos")
        else:
            embed.set_image(url=data["url"])
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Img(bot))
    bot.add_cog(ImgSecundario(bot))