import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw, GifImagePlugin, ImageOps, ImageFilter
from io import BytesIO
from datetime import datetime as t
from requests import get
import json
import random
from colorthief import ColorThief

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

def add_corners(im, rad, top_only=False, bottom_only=False):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h-rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w-rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w-rad, h-rad))
    im.putalpha(alpha)

def imagefromURL(url): 
    return Image.open(BytesIO(get(url).content))

def get_accent(thief, image):
    data = BytesIO(get(image).content)
    return thief(data).get_color()

def brightness_text(tupl):
    if (sum(tupl)/3) < 127.5: return (255, 255, 255)
    return (0, 0, 0)

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imagefromURL = imagefromURL
        self.get_color_accent = get_accent
        self.thief = ColorThief
        self.add_corners = add_corners
        self.invert = brightness_text


    def buffer(self, data):
        arr = BytesIO()
        data.save(arr, format='PNG')
        arr.seek(0)
        return arr


    def resize(self, url, x, y):
        pic = self.imagefromURL(url)
        pic = pic.resize((x, y))
        data = self.buffer(pic)
        return data

    def _spotify(self, details):
        url = details['url']
        del details['url']
        longest_word = [details[i] for i in list(details.keys()) if len(details[i])==sorted([
            len(details[a]) for a in list(details.keys())
        ])[::-1][0]][0]
        ava, bg = self.imagefromURL(url).resize((250, 250)), self.get_color_accent(self.thief, url)
        fg = self.invert(bg)
        big_font, smol_font = ImageFont.truetype("verdanab.ttf", 60), ImageFont.truetype("consola.ttf", 45)
        longest_font_width = smol_font.getsize(longest_word)[0] if longest_word!=details['name'] else big_font.getsize(details['name'])[0]   
        if longest_font_width < 300: 
            longest_font_width = 300
        main = Image.new(mode='RGB', color=bg, size=(longest_font_width+355, 300))
        self.add_corners(ava, 100)
        main.paste(ava, (20, 20))
        draw = ImageDraw.Draw(main)
        draw.text((300, 50), details['name'], fill=fg, font=big_font)
        draw.text((300, 150), details['album'], fill=fg, font=smol_font)
        draw.text((300, 210), "Por: "+details['artist'], fill=fg, font=smol_font)
        add_corners(main, 25)
        return self.buffer(main)

    def dearray(self, arr):
        return str(', '.join(arr))+'.'

    @commands.command(description="¿Que estas escuchando? (TIENES QUE TENER EL ESTADO DE DISCORD EN SPOTIFY)", usage="[Usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def spotify(self, ctx, *args):
        source = getUser(ctx, args)
        if str(source.activity).lower()!='spotify': 
            await ctx.send(' | Nada, sin escuchar Spotify. Muestre Spotify como su presencia \ny desactive su estado personalizado si lo tiene.')
        else:
            async with ctx.message.channel.typing():
                await ctx.send(file=discord.File(self._spotify({
                    'name': source.activity.title,
                    'artist': self.dearray(source.activity.artists),
                    'album': source.activity.album,
                    'url': source.activity.album_cover_url
                }), 'spotify.png'))

def setup(bot):
    bot.add_cog(Spotify(bot)) 