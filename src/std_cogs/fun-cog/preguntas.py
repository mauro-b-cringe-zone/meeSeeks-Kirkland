from discord.ext import commands
import asyncio

from os import environ as env
import discord

color = int(env["COLOR"])

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)

class Preguntas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Haz una pregunta a la gente (LUEGO ENVIA MENSAJES CON LAS OPCIONES)")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    async def poll(self, ctx, *, question):

        messages = [ctx.message]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100

        for i in range(20):
            messages.append(await ctx.send(f'Di la opción de encuesta o {ctx.prefix}cancelar para publicar encuesta.'))

            try:
                entry = await self.bot.wait_for('message', check=check, timeout=20.0)
            except asyncio.TimeoutError:
                break

            messages.append(entry)

            if entry.clean_content.startswith(f'{ctx.prefix}cancelar'):
                break

            answers.append((to_emoji(i), entry.clean_content))

        try:
            await ctx.channel.delete_messages(messages)
        except:
            pass 

        answer = '\n'.join(f'{keycap}: {content}' for keycap, content in answers)
        actual_poll = await ctx.send(embed=discord.Embed(color=color, title="Una nueva pregunta", description=f"{ctx.author.mention} pregunta: {question}").add_field(name="Respuestas:", value=answer))
        for emoji, _ in answers:
            await actual_poll.add_reaction(emoji)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

    @commands.command(description="Ej: Nombre_de_la_pregunta opcion1 opcion2")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    async def quickpoll(self, ctx, *questions_and_choices: str):

        if len(questions_and_choices) < 3:
            return await ctx.send('Necesita al menos 1 pregunta con 2 opciones.')
        elif len(questions_and_choices) > 21:
            return await ctx.send('Solo puede tener hasta 20 opciones.')

        perms = ctx.channel.permissions_for(ctx.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Necesita leer el historial de mensajes y agregar permisos de reacciones.')

        question = questions_and_choices[0]
        choices = [(to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])]

        try:
            await ctx.message.delete()
        except:
            pass

        body = "\n".join(f"{key}: {c}" for key, c in choices)
        poll = await ctx.send(f'{ctx.author.mention} pregunta: {question}\n\n{body}')
        for emoji, _ in choices:
            await poll.add_reaction(emoji)


def setup(bot):
    bot.add_cog(Preguntas(bot))
