import discord
from discord.ext import commands

from PIL import Image, ImageFont, ImageDraw, GifImagePlugin, ImageOps, ImageFilter
from io import BytesIO

from datetime import datetime as t
from requests import get
import json
import random
from colorthief import ColorThief
from time import gmtime, strftime

from os import environ as env
import asyncio
import numpy as np

color = int(env["COLOR"])

class Smart_ColorThief:
    def __image_from_url(self, url):
        return Image.open(BytesIO(get(url).content))

    def __init__(self, url):
        self.image = self.__image_from_url(url).resize((50, 50))
    
    def get_color(self, right=False):
        if right:
            res = []
            for i in range(self.image.height):
                for j in range(self.image.width):
                    res.append(self.image.getpixel((self.image.width-1, i)))
        else:
            arr_L, arr_R, arr_T, arr_B = [], [], [], []
            for i in range(self.image.height):
                for j in range(self.image.width):
                    arr_L.append(self.image.getpixel((0, i)))
                    arr_R.append(self.image.getpixel((self.image.width-1, i)))
                    arr_T.append(self.image.getpixel((j, 0)))
                    arr_B.append(self.image.getpixel((j, self.image.height-1)))
            res = arr_L + arr_R + arr_T + arr_B
        return max(set(res), key=res.count)

async def getUser(ctx, args, user=None, allownoargs=True):
    if len(args)==0:
        if not allownoargs: await ctx.send("Porfavor include argumentos.")
        return ctx.author
    if len(ctx.message.mentions)>0: return ctx.message.mentions[0]
    name = str(' '.join(list(args))).lower().split('#')[0]
    user = [i for i in ctx.guild.members if ((i.display_name.lower().startswith(name)) or (name in i.display_name.lower()))]
    if len(user) > 0: return user[0]
    if args[0].isnumeric():
        if int(args[0]) not in [i.id for i in ctx.guild.members]: await ctx.send("No se encontro ningun usuario.")
        return ctx.guild.get_member(int(args[0]))
    return ctx.author

def buffer_from_url(url, *args, **kwargs):
    try: return Image.open(BytesIO(get(url, timeout=5).content))
    except: return Image.new(mode='RGB', size=(500, 500), color=(0, 0, 0))

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

def get_color_accent(url, right=False):
    res = Smart_ColorThief(url).get_color(right=right)
    return res[0], res[1], res[2]

def brightness_text(tupl):
    if (sum(tupl)/3) < 127.5: return (255, 255, 255)
    return (0, 0, 0)

def get_font(fontname, size, otf=False):
    ext = 'ttf' if not otf else 'otf'
    return ImageFont.truetype(f'./src/utils/fonts/{fontname}.{ext}', size)

def resize(url, x, y):
    pic = buffer_from_url(url)
    pic = pic.resize((x, y))
    data = buffer(pic)
    return data

def buffer(data):
    arr = BytesIO()
    data.save(arr, format='PNG')
    arr.seek(0)
    return arr

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.imagefromURL = imagefromURL
        self.get_color_accent = get_color_accent
        self.thief = ColorThief
        self.add_corners = add_corners
        self.invert = brightness_text
        self.get_font = get_font
        self.buffer = buffer
        self.getUser = getUser
        self.buffer_from_url = buffer_from_url


    def custom_panel(self, title="Title text", subtitle="Subtitle text", description="Description text here", icon="https://cdn.discordapp.com/embed/avatars/0.png", spt=None):
        SPOTIFY = False if (spt is None) else True
        TITLE_TEXT = title if not SPOTIFY else spt.title
        TITLE_FONT = self.get_font("NotoSansDisplay-Bold", 15, otf=True)

        SUBTITLE_TEXT = subtitle if not SPOTIFY else "By "+(', '.join(spt.artists))
        SUBTITLE_FONT = self.get_font("NotoSansDisplay-Bold", 10, otf=True)

        DESC_TEXT = description if not SPOTIFY else "On "+spt.album
        DESC_FONT = self.get_font("NotoSansDisplay-Bold", 10, otf=True)
        COVER_URL = icon if not SPOTIFY else spt.album_cover_url
        COVER = self.buffer_from_url(COVER_URL).resize((100, 100))
        SPOTIFY_ICON = self.buffer_from_url("https://www.clipartmax.com/png/full/293-2938089_icono-spotify-png-bic-sports-downwind-kayak-sail-31657.png").resize((50, 50))
        BACKGROUND_COLOR = self.get_color_accent(COVER_URL, right=True)
        FOREGROUND_COLOR = self.invert(BACKGROUND_COLOR)

        if len(TITLE_TEXT) > 25: TITLE_TEXT = TITLE_TEXT[0:25] + "..."
        if len(SUBTITLE_TEXT) > 35: SUBTITLE_TEXT = SUBTITLE_TEXT[0:35] + "..."
        if len(DESC_TEXT) > 45: DESC_TEXT = DESC_TEXT[0:45] + "..."

        TITLE_SIZE = TITLE_FONT.getsize(TITLE_TEXT)
        SUBTITLE_SIZE = SUBTITLE_FONT.getsize(SUBTITLE_TEXT)
        DESC_SIZE = DESC_FONT.getsize(DESC_TEXT)
        WIDTH = max([TITLE_SIZE[0], SUBTITLE_SIZE[0], DESC_SIZE[0]]) + 270

        if WIDTH < 500:
            WIDTH = 500

        MARGIN_LEFT = 140
        MARGIN_RIGHT = WIDTH - 20
        MARGIN_TOP = 5

        MAIN = Image.new(mode="RGB", color=BACKGROUND_COLOR, size=(WIDTH, 120))
        DRAW = ImageDraw.Draw(MAIN)

        if SPOTIFY:
            SEEK = round(round((t.now() - spt.created_at).total_seconds())/round(spt.duration.total_seconds())*100)
            STR_CURRENT = strftime('%M:%S', gmtime(round((t.now() - spt.created_at).total_seconds())))
            STR_END = strftime('%M:%S', gmtime(round(spt.duration.total_seconds())))
            DURATION_LEFT_SIZE = DRAW.textsize(STR_END, font=SUBTITLE_FONT)[0]

            
            DRAW.rectangle([(MARGIN_LEFT, MARGIN_TOP + 60), (MARGIN_RIGHT, MARGIN_TOP + 85)], fill=tuple(map(lambda x: x - 25, BACKGROUND_COLOR)), outline="#ddd")
            DRAW.rectangle([(MARGIN_LEFT, MARGIN_TOP + 60), ((SEEK / 100 * (MARGIN_RIGHT - MARGIN_LEFT)) + MARGIN_LEFT, MARGIN_TOP + 85)], fill="#2ecc71")       
            DRAW.text((MARGIN_LEFT, MARGIN_TOP + 90), STR_CURRENT, font=SUBTITLE_FONT, fill="#2ecc71")
            DRAW.text((MARGIN_RIGHT - DURATION_LEFT_SIZE, MARGIN_TOP + 90), STR_END, font=SUBTITLE_FONT, fill="#2ecc71")

        DRAW.text((MARGIN_LEFT, MARGIN_TOP), TITLE_TEXT, font=TITLE_FONT, fill=FOREGROUND_COLOR)
        DRAW.text((MARGIN_LEFT, MARGIN_TOP + 25), SUBTITLE_TEXT, font=SUBTITLE_FONT, fill=FOREGROUND_COLOR)
        DRAW.text((MARGIN_LEFT, MARGIN_TOP + 40), DESC_TEXT, font=DESC_FONT, fill=FOREGROUND_COLOR)

        MAIN.paste(COVER, (25, 10))
        SPI = SPOTIFY_ICON.rotate(-10)
        MAIN.paste(SPI, (400, 10), SPI)
        
        return self.buffer(MAIN)

    async def spotify_gen2(self, album_cover, artist, title, album_title, dom_color, timestamp, local_file, hidden):
            smallfont = ImageFont.truetype(
                './src/utils/fonts/Arial-Unicode-MS.ttf', size=40)
            bigfont = ImageFont.truetype(
                './src/utils/fonts/Arial-Unicode-MS.ttf', size=50)
            boldfont = ImageFont.truetype(
                './src/utils/fonts/Arial-Unicode-Bold.ttf', size=60)

            width = 1280
            height = 400

            if hidden:
                width -= 100
                height -= 100

            canvas = Image.new('RGB', (width, height), dom_color[0])

            img = Image.open(album_cover).convert('RGBA').resize((height, height))
            canvas_fade = await self.fade(canvas.crop((0, 0, height, height)), 'right', 58 if hidden else 78)

            canvas.paste(img, (width - height, 0), img)
            canvas.paste(canvas_fade, (width - height, 0), canvas_fade)

            texts = (boldfont, title), (bigfont, artist)
            text_area = width - height - 50
            title, artist, fontcolor = await asyncio.gather(*([self.get_text(f, t, text_area) for f, t in texts] + \
                                                [self.get_font_color(*dom_color)]))
            alt_color = [self.get_alt_color(fontcolor, i, dom_color[0]) for i in (20, 30)]
            alt_color.append(fontcolor)

            reverse = self.get_luminosity(dom_color[0]) > 128
            alt_color, lighter_color, fontcolor = sorted(alt_color, key=self.get_luminosity, reverse=reverse)

            spotify_logo = Image.open('./docs/images/spotify.png').convert('RGBA').resize((50, 50))
            data = np.array(spotify_logo)
            red, green, blue, alpha = data.T
            non_transparent_areas = alpha > 0
            data[..., :-1][non_transparent_areas.T] = lighter_color

            spotify_logo = Image.fromarray(data)
            canvas.paste(spotify_logo, (50, 50), spotify_logo)

            draw = ImageDraw.Draw(canvas)

            spotify_text = 'Spotify \u2022'
            if local_file:
                album_title = 'Local Files'
            else:
                album_title = await self.get_text(smallfont, f'{album_title}', width - height - 280)

            draw.text((120, 50), spotify_text, font=smallfont, fill=lighter_color)
            draw.text((280, 50), album_title, font=smallfont, fill=alt_color)
            draw.text((50, 110), title, font=boldfont, fill=fontcolor)
            draw.text((50, 190), artist, font=bigfont, fill=alt_color)

            if hidden:
                y1 = 70
                y2 = 80
            else:
                y1 = 80
                y2 = 70

            draw.line(((width-90, y1), (width-79, y2)), fill=lighter_color, width=5)
            draw.line(((width-81, y2), (width-70, y1)), fill=lighter_color, width=5)

            await self.add_corners(canvas, 50)
            if hidden:
                return canvas

            rectangle_length = timestamp[2] / 100 * (width - 100)
            elapsed_bar = self.round_rectangle((width - 100, 10), 5, (*lighter_color, 255)).crop((0, 0, int(rectangle_length), 10))
            bar = self.round_rectangle((width - 100, 10), 5, (*lighter_color, 150))

            canvas.paste(bar, (50, 300), bar)
            canvas.paste(elapsed_bar, (50, 300), elapsed_bar)

            r = 15

    @commands.command(aliases='spot,splay,listeningto,sp'.split(","))
    async def spotify(self, ctx, *args):
        source, act = await self.getUser(ctx, tuple([
                i for i in args if '--force' not in i
            ])), None
        if ''.join(args).endswith('--force'):
            force = True
            act = source.activity
        else:
            force = False
            for i in source.activities:
                if isinstance(i, discord.Spotify): act = i
            if act is None: 
                return await ctx.send(embed=discord.Embed(title="ups...", description=f"Lo siento, pero  {source.mention} no esta escuchando espotify.", color=color))
        async with ctx.channel.typing():
            print(act)
            if force:
                try:
                    return await ctx.send(file=discord.File(spotify_gen2(), 'spotify.png'))
                except: return 
            await ctx.send(file=discord.File(self.spotify_gen2(act.album_cover_url, act.artist, act.title, act.album_title, self.get_color_accent(act.album_cover_url, right=True), strftime('%M:%S', gmtime(round((t.now() - act.created_at).total_seconds()))), False, False), 'spotify.png'))

def setup(bot):
    bot.add_cog(Spotify(bot)) 