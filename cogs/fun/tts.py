import discord
from discord.ext import commands
import sys
sys.path.append('/home/runner/hosting601/modules')
import astroid.brain.brain_numpy_random_mtrand
from aiohttp import ClientSession
from io import BytesIO
import asyncio
from gtts import gTTS

class Tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['talk','gtts','texttospeech','text-to-speech'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tts(self, ctx, *args):
        if len(list(args))==0: 
            return await ctx.send("Introduce algun argumento por ejemplo **123**")
        if len(list(args))>5:
            return await ctx.send("El maximo de el tts es **5**")
        res = BytesIO()
        tts = gTTS(text=' '.join(list(args)), lang='es', slow=False)
        tts.write_to_fp(res)
        res.seek(0)
        await ctx.send(content="Dale al archivo que pone **tts.mp3** para descargartelo", file=discord.File(fp=res, filename='tts.mp3'))

def setup(bot):
    bot.add_cog(Tts(bot))