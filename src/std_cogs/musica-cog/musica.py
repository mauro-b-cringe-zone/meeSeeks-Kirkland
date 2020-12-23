import asyncio
import datetime as dt
import random
import re
import typing as t
from enum import Enum

import discord
import wavelink
from discord.ext import commands

from utils.Logger.Logger import Logger

from os import environ as env
import threading
from time import sleep
from tqdm import tqdm

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}

color = int(env["COLOR"])


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel
     

        channel = getattr(ctx.author.voice, "channel", channel)
        if channel is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(embed=discord.Embed(title="Añadido a la cola", description=f"{ctx.author.mention}, se ha añadido **{tracks[0].title}** a la cola", color=color, url=tracks[0].uri).add_field(name="Autor", value=tracks[0].author).add_field(name="Duracion", value=f"{int(tracks[0].duration) / 60}  Minutos").add_field(name="Musica puesta por", value=ctx.author.mention).set_footer(icon_url=ctx.author.avatar_url).set_thumbnail(url=tracks[0].thumb))
        else:
            track = await self.choose_track(ctx, tracks)
            if track is not None:
                self.queue.add(track)
                await ctx.send(embed=discord.Embed(title="Añadido a la cola", description=f"{ctx.author.mention}, se ha añadido **[{tracks[0].title}]({tracks[0].uri})** a la cola", color=color, url=tracks[0].uri).add_field(name="Autor", value=tracks[0].author).add_field(name="Duracion", value=f"{int(int(tracks[0].duration) / 60)}  Minutos").add_field(name="Musica puesta por", value=ctx.author.mention).set_footer(icon_url=ctx.author.avatar_url).set_thumbnail(url=tracks[0].thumb))

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Escoge una cancion",
            description=(
                "\n".join(
                    f"**{i+1} |** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})"
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=color,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Resultados de canciones", icon_url="https://img.icons8.com/clouds/100/000000/music.png")
        embed.set_footer(text=f"Invocado por {ctx.author.name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            track = self.queue.get_next_track()
            if track is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()
                # await ctx.send(embed=discord.Embed(title="¿Se acabo la fiesta?", color=color, description="Me he salido de el canal porque "))

    def cargar(self, texto, t):
        for i in tqdm(range(1, 100), desc=texto, leave=False): 
            sleep(t)

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        x = threading.Thread(target=self.cargar, args=("Cargando musica", .01,))
        x.start()
        x.join()
        Logger.info(f"MUSICA Wavelink preparado en el nodo: `{node.identifier}`.", separador=True)

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("Los comandos de musica no disponibles para DMs.")
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "maubot.maucode.com",
                "port": 2333,
                "rest_uri": "http://maubot.maucode.com:2333/",
                "password": "youshallnotpass",
                "identifier": "MAIN",
                "region": "europe",
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)
            
    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="connect", aliases=["join"], description="Maubot se unira a un canal de voz", usage="[canal]")
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        embed = discord.Embed(title=f"Me he unido a {channel.name}", colour=color)
        await ctx.send(embed=embed)

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send("Ya estoy en un canal.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No se ha encontrado ningun canal de voz.")
        if isinstance(exception, commands.BotMissingPermissions):
            await ctx.send("No tengo los permisos para hacer esto.")

    @commands.command(name="disconnect", aliases=["leave"], description="Maubot se ira a un canal de voz")
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        embed = discord.Embed(title=f"Me he ido de el canal", colour=color)
        await ctx.send(embed=embed)

    @commands.command(name="resume", description="Continua la musica")
    async def resume_command(self, ctx):
        player = self.get_player(ctx)
        await player.set_pause(False)
        await ctx.send(embed=discord.Embed(title="Reproducción reanudada.", color=color))

    @commands.command(name="play", description="Si Maubot no esta conectado a un canal se unira, Maubot añadira una cancion a la cola si ya hay una por lo contrario reproducira la cancion. Si no hay cancion Maubot resumira la cancion", usage="[cancion]")
    async def play_command(self, ctx, *, query: t.Optional[str]):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send(embed=discord.Embed(title="Reproducción reanudada.", color=color))

        else:
            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("No hay canciones para reproducir porque la cola está vacía.")
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send("No se proporcionó ningún canal de voz adecuado.")
        if isinstance(exception, commands.BotMissingPermissions):
            await ctx.send("No tengo los permisos para hacer esto.")

    @commands.command(name="pause", description="Pausa la musica")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.message.add_reaction('⏯')

        embed = discord.Embed(colour=color)
        embed.set_author(name=" |  Pausando...", icon_url="https://img.icons8.com/color/48/000000/circled-pause.png")
        await ctx.send(embed=embed)

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send("Ya pausado.")

    @commands.command(name="stop", description="Eliminara la cola y no reproducira la musica")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        if player.queue.is_empty:
            return await ctx.send("Maubot ya se ha parado")
        await player.stop()
        await ctx.message.add_reaction('⏹')

        embed = discord.Embed(description="¿La cola a sido vaciada?... Si\n¿Reproductor parada?... Si\n\nTodo ha ido bien", colour=color)
        embed.set_author(name="parando...", icon_url="https://img.icons8.com/color/48/000000/stop-squared.png")
        await ctx.send(embed=embed)

    @commands.command(name="next", aliases=["skip"], description="Reproduce la siguiente cancion")
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.message.add_reaction('⏭')

        embed = discord.Embed(color=color)
        embed.set_author(name=f"Siguiente cancion... |  50%  🔊")
        await ctx.send(embed=embed)

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("Esto no se pudo ejecutar porque la cola está actualmente vacía.")
        elif isinstance(exc, NoMoreTracks):
            await ctx.send("No hay más pistas en la cola.")

    @commands.command(name="previous", description="Reproduce la cancion anterior")
    async def previous_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        embed = discord.Embed(color=color)
        embed.set_author(name=f"Poniendo la cancion anterior...")
        await ctx.send(embed=embed)

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("Esto no se pudo ejecutar porque la cola está actualmente vacía.")
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send("No hay pistas anteriores en la cola.")

    @commands.command(name="shuffle", description="Varajea la cola")
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        await ctx.message.add_reaction('✅')
        embed = discord.Embed(title='Varajeando la cola', colour=color)
        await ctx.send(embed=embed)

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send("La cola no se pudo barajar porque actualmente está vacía.")

    @commands.command(name="repeat", aliases=["loop"], description="Escribe el modo en el que se repitira la cancion", usage="[<none (Se cancela el loop)><1 (Repite la cancion 1 vez)><all (Repite la cancion asta que se diga que no)>]")
    async def repeat_command(self, ctx, mode: str):
        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        await ctx.message.add_reaction('✅')

        embed = discord.Embed(title=f'cambiando loop a ({mode})', colour=color)
        await ctx.send(embed=embed)         

    @commands.command(name="queue", description="Mira la lista de canciones", usage="[numero maximo de canciones en la cola]")
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Cola de canciones",
            description=f"Mostrando hasta las siguientes **{show}** pistas",
            colour=color,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name="Resultados de la cola")
        embed.set_footer(text=f"Solicitado por {ctx.author.mention}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Reproduciendo",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing."),
            inline=False
        )
        upcoming = player.queue.upcoming
        if upcoming:
            canciones = ""
            for t in upcoming[:show]:
                canciones += t.title + "\n"
            embed.add_field(name="Siguiente", value=canciones, inline=False)

        msg = await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(embed=discord.Embed(title="Nada...", color=color, description="Actualmente, la cola está vacía."))


def setup(bot):
    # Con lavalink
    bot.add_cog(Music(bot))
