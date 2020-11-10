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
        TITLE_FONT = self.get_font("NotoSansDisplay-Bold", 30, otf=True)

        SUBTITLE_TEXT = subtitle if not SPOTIFY else "By "+(', '.join(spt.artists))
        SUBTITLE_FONT = self.get_font("NotoSansDisplay-Bold", 20, otf=True)

        DESC_TEXT = description if not SPOTIFY else "On "+spt.album
        DESC_FONT = self.get_font("NotoSansDisplay-Bold", 15, otf=True)
        COVER_URL = icon if not SPOTIFY else spt.album_cover_url
        COVER = self.buffer_from_url(COVER_URL).resize((100, 100))
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

        MARGIN_LEFT = 220
        MARGIN_RIGHT = WIDTH - 20
        MARGIN_TOP = 20

        MAIN = Image.new(mode="RGB", color=BACKGROUND_COLOR, size=(WIDTH, 100))
        DRAW = ImageDraw.Draw(MAIN)

        if SPOTIFY:
            SEEK = round(round((t.now() - spt.created_at).total_seconds())/round(spt.duration.total_seconds())*100)
            STR_CURRENT = strftime('%M:%S', gmtime(round((t.now() - spt.created_at).total_seconds())))
            STR_END = strftime('%M:%S', gmtime(round(spt.duration.total_seconds())))
            DURATION_LEFT_SIZE = DRAW.textsize(STR_END, font=SUBTITLE_FONT)[0]

            DRAW.rectangle([(MARGIN_LEFT, MARGIN_TOP + 100), (MARGIN_RIGHT, MARGIN_TOP + 120)], fill=tuple(map(lambda x: x - 25, BACKGROUND_COLOR)))
            DRAW.rectangle([(MARGIN_LEFT, MARGIN_TOP + 100), ((SEEK / 100 * (MARGIN_RIGHT - MARGIN_LEFT)) + MARGIN_LEFT, MARGIN_TOP + 120)], fill=FOREGROUND_COLOR)
            DRAW.text((MARGIN_LEFT, MARGIN_TOP + 130), STR_CURRENT, font=SUBTITLE_FONT, fill=FOREGROUND_COLOR)
            DRAW.text((MARGIN_RIGHT - DURATION_LEFT_SIZE, MARGIN_TOP + 130), STR_END, font=SUBTITLE_FONT, fill=FOREGROUND_COLOR)

        DRAW.text((MARGIN_LEFT, MARGIN_TOP), TITLE_TEXT, font=TITLE_FONT, fill=FOREGROUND_COLOR)
        DRAW.text((MARGIN_LEFT, MARGIN_TOP + 38), SUBTITLE_TEXT, font=SUBTITLE_FONT, fill=FOREGROUND_COLOR)
        DRAW.text((MARGIN_LEFT, MARGIN_TOP + 65), DESC_TEXT, font=DESC_FONT, fill=FOREGROUND_COLOR)

        MAIN.paste(COVER, (50, 50))
        
        return self.buffer(MAIN)

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
                    return await ctx.send(file=discord.File(self.custom_panel(spt=act), 'spotify.png'))
                except: return 
            await ctx.send(file=discord.File(self.custom_panel(spt=act), 'spotify.png'))

def setup(bot):
    bot.add_cog(Spotify(bot)) 