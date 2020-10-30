import asyncio
import functools
import itertools
import math
import random
import os
from termcolor import cprint
import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

from flask import Flask
from threading import Thread

from os import environ as env

color =  int(env["COLOR"])

app = Flask('')

@app.route('/')
def home():
	return 'Estoy dentro!'

def run():
    app.run(
		host='0.0.0.0',
		port=random.randint(2000,9000)
	)

def keep_alive():
	'''
	Crea e inicia un nuevo hilo que ejecuta la función run.
	'''
	t = Thread(target=run)
	t.start()

# Silenciar mensajes de informes de errores inútiles
youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.release_year = data.get('release_year')
        self.alt_title = data.get('alt_title')
        self.comment_count = data.get('comment_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** por **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} dias'.format(days))
        if hours > 0:
            duration.append('{} horas'.format(hours))
        if minutes > 0:
            duration.append('{} minutos'.format(minutes))
        if seconds > 0:
            duration.append('{} segundos'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        if self.source.duration == "":
            self.source.duration = "🔴 En directo"
        embed = (discord.Embed(title='{0.source.title}'.format(self),
                               colour=color,
                               url='{0.source.url})'.format(self))
                 .set_author(name=f"  Reproduciendo ahora  |  {self.source._volume}%  🔊", icon_url="https://img.icons8.com/color/48/000000/music-record--v1.png")
                 .add_field(name='Duracion', value=self.source.duration)
                 .add_field(name='Autor', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='Propuesto por', value=self.requester.mention)
                 .set_footer(text=f"Propuesto por {self.requester.name}", icon_url="https://img.icons8.com/color/48/000000/international-music.png")
                 .set_thumbnail(url=self.source.thumbnail))

        return embed

    def create_embed_next(self):
        if self.source.duration == "":
            self.source.duration = "🔴 En directo"
        embed = (discord.Embed(title='{0.source.title}'.format(self),
                               colour=color,
                               url='{0.source.url})'.format(self))
                 .set_author(name=f"  S¡iguiente cancion...  |  {self.source._volume}%  🔊", icon_url="https://img.icons8.com/color/48/000000/music-record--v1.png")
                 .add_field(name='Duracion', value=self.source.duration)
                 .add_field(name='Autor', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='Propuesto por', value=self.requester.mention)
                 .set_footer(text=f"Propuesto por {self.requester.name}", icon_url="https://img.icons8.com/color/48/000000/international-music.png")
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Intente obtener la siguiente canción en 3 minutos.
                # Si no se agregará ninguna canción a la cola a tiempo,
                # el reproductor se desconectará debido al rendimiento
                # razones.
                try:
                    async with timeout(180):  # 3 minutos
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))
        
        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None



class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    # async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
    #     await ctx.send('Ups.. un error: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True, description="Unirse ha un canal", usage="<cancion>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _join(self, ctx: commands.Context):
        ctx.voice_state.songs.clear()
        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        embed = discord.Embed(title=f"Me he unido a {ctx.author.voice.channel}", colour=color)
        await ctx.send(embed=embed)

    @commands.command(name='summon', description="Cambiarse de canal", usage="[canal]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):

        if not channel and not ctx.author.voice:
            raise VoiceError('No está conectado a un canal de voz ni ha especificado un canal para unirse.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        
        embed = discord.Embed(title=f"Me he movido a {ctx.author.voice.channel}", colour=color)
        await ctx.send(embed=embed)

    @commands.command(name='leave', aliases=['disconnect'], description="Irse del canal")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        # Borra la cola y sale del canal de voz.

        if not ctx.voice_state.voice:
            return await ctx.send('No conectada a ningún canal de voz.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

        
        embed = discord.Embed(title=f"Me he ido de {ctx.author.voice.channel}", colour=color)
        await ctx.send(embed=embed)

    @commands.command(name='volume', description="Cambia el volumen de la cancion", usage="<volumen>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _volume(self, ctx: commands.Context, *, volume: int):

        if not ctx.voice_state.is_playing:
            return await ctx.send('No se está reproduciendo nada en este momento.')

        if volume < 0 or volume > 100:
            return await ctx.send('El volumen debe estar entre 0 y 100')

        try:
            ctx.voice_state.volume = volume / 100
        except Exception as e:
            cprint(str("[Log] un error: " + e), 'red')
            
        embed = discord.Embed(colour=color)
        embed.set_author(name=' |  Volumen del jugador configurado en {}%'.format(volume), icon_url="https://img.icons8.com/color/48/000000/speaker.png")
        await ctx.send(embed=embed)

    @commands.command(name='now', aliases=['current', 'playing'], description="¿Que estas escuchando?")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _now(self, ctx: commands.Context):
        # te dice la cancion actual
        embed = ctx.voice_state.current.create_embed()
        # embed.add_field(name="Curso", value="━━━━━━━━[x]━━━━━━━━━━━━━━━", inline=False)
        await ctx.send(embed=embed)

        # embed = discord.Embed(title="Reproduciendo ahora", description=ctx.voice_state.current, colour=color)
        # await ctx.send(embed=embed)

    @commands.command(name='pause', description="Pausa la musica")
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _pause(self, ctx: commands.Context):

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

            embed = discord.Embed(colour=color)
            embed.set_author(name=" |  Pausando...", icon_url="https://img.icons8.com/color/48/000000/circled-pause.png")
            await ctx.send(embed=embed)

    @commands.command(name='resume', description="Continua con la musica")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

            embed = discord.Embed(colour=color)
            embed.set_author(name=" |  Resumiendo...", icon_url="https://img.icons8.com/color/48/000000/circled-play--v1.png")
            await ctx.send(embed=embed)

    @commands.command(name='stop', description="Para la musica y limpia la cola")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        # lo elimina todo de la cola y para el reproductor

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

            embed = discord.Embed(description="¿La cola a sido vaciada?... Si\n¿Reproductor parado?... Si\n\nTodo ha ido bien", colour=color)
            embed.set_author(name="parando...", icon_url="https://img.icons8.com/color/48/000000/stop-squared.png")
            await ctx.send(embed=embed)
        if not ctx.voice_state.is_playing:
            await ctx.send("**NO**")

    @commands.command(name='next', aliases=['skip'], description="Siguiente porfavor")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _skip(self, ctx: commands.Context):
        """
            Vota para saltarte una canción. El solicitante puede omitir automáticamente.
            Se necesitan 3 votos para omitir la canción.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('No reproduzco música en este momento ...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

            embed = ctx.voice_state.current.create_embed_next()
            embed.set_author(name=f"Siguiente cancion... |  {self.source._volume}%  🔊")
            await ctx.send(embed=embed)

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()

                embed = ctx.voice_state.current.create_embed_next ()
                embed.set_author(name=f"Siguiente cancion... |  {self.source._volume}%  🔊")
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title='voto para omitir agregado, actualmente en **{}/3**'.format(total_votes), colour=color)
                await ctx.send(embed=embed)
        else:
            await ctx.send('Ya votaste para omitir esta canción.')

    @commands.command(name='queue', description="Mira la cola de canciones", usage="[pagina]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """
            Muestra la cola del jugador.
            Opcionalmente, puede especificar la página que se mostrará. Cada página contiene 10 elementos.
        """

        if len(ctx.voice_state.songs) == 0:
            embed = discord.Embed(title='La cola esta vacia', description="Estaria bien añadir alguna cancion.", colour=color)
            return await ctx.send(embed=embed)

        items_per_page = 5
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '**#{0}** |  [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} pistas:**\n\n{}'.format(len(ctx.voice_state.songs), queue), colour=color)
                 .set_author(name=" |  Cola", icon_url="https://img.icons8.com/color/48/000000/music-library.png")
                 .set_footer(text='Viendo la pagina {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle', description="Varajea las canciones en la cola")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _shuffle(self, ctx: commands.Context):

        if len(ctx.voice_state.songs) == 0:
            embed = discord.Embed(title='La cola esta vacia', description="Estaria bien añadir alguna cancion.", colour=color)
            await ctx.send(embed=embed)
            return await ctx.send(embed=embed)

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')
        embed = discord.Embed(title='Varajeando la cola', colour=color)
        await ctx.send(embed=embed)

    @commands.command(name='remove', description="Quita una cancion de la cola", usage="<index>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _remove(self, ctx: commands.Context, index: int):
        # Elimina una canción de la cola en un índice determinado.

        if len(ctx.voice_state.songs) == 0:
            embed = discord.Embed(title='La cola esta vacia', description="Estaria bien añadir alguna cancion.", colour=color)
            await ctx.send(embed=embed)
            return await ctx.send(embed=embed)

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

        embed = discord.Embed(title='Quitando cvancion de la cola', colour=color)
        await ctx.send(embed=embed)        

    @commands.command(name='loop', description="Haz que se repita la musica (Verdadero : Falso)")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _loop(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send('No se está reproduciendo nada en este momento.')

        # Valor booleano inverso para repetir y desbloquear.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

        embed = discord.Embed(title=f'cambiando loop a ({ctx.voice_state.loop})', colour=color)
        await ctx.send(embed=embed)           

    @commands.command(name='play', description="Pon una musica o añade una cancion a la cola", usage="<cancion>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _play(self, ctx: commands.Context, *, search: str):

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('Se produjo un error al procesar esta solicitud: {}'.format(str(e)))
            else:
                if not ctx.voice_state.is_playing:
                    try:
                        song = Song(source)
                        cprint('[Log] poniendo cancion', 'yellow')
                        await ctx.voice_state.songs.put(song)
                        cprint('[Log] reproduciendo', 'green')
                    except Exception as e:
                        cprint('[Log] un error\n\n{e}', 'red')
                if ctx.voice_state.is_playing:
                    try:
                        song = Song(source)
                        await ctx.voice_state.songs.put(song)
                        embed_queue = discord.Embed(title='Añadiendo a la cola', desciption=f"{str(source)}", colour=color)
                        await ctx.send(embed=embed_queue)      
                    except Exception as e:
                        cprint(str("[Log] un error: " + e), 'red') 

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('No estás conectado a ningún canal de voz.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot ya está en un canal de voz.')

def setup(bot):
    bot.add_cog(Music(bot))