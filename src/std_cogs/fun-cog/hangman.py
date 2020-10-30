import random
import os
from typing import Dict, List

import discord
from discord.ext import commands
from os import environ as env
color = int(env["COLOR"])

from googletrans import Translator

trans = Translator()

hangman_embed = discord.Embed(title="Juego 'Hangman' con reacciones", color=color).set_footer(text='Consejo: Busca "regional" en la barra de reacciones.')


def module_perms(ctx):
    return ctx.channel.id == 567179438047887381


class HangmanGame:
    word: str
    visible: str
    errors: int
    guesses: List[str]

    def __init__(self, word):
        # print(word)
        self.word = word
        self.guesses = []
        self.visible = '*' * len(word)
        self.errors = 0
    
    def guess(self, letter):
        if letter not in self.guesses:
            self.guesses.append(letter)
            self.updateStatus()

    def updateStatus(self):
        self.errors = len([c for c in self.guesses if c not in self.word])
        if self.errors > 5:
            self.visible = self.word
        else:
            self.visible = ''.join('*' if c not in self.guesses else c for c in self.word)
    

class Hangman(commands.Cog):
    games: Dict[str, HangmanGame]
    words: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        self.words = []

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_dict()
    
    async def load_dict(self):
        with open("./src/utils/fun/dictionary.txt", "r") as dictionary:

            self.words = [s.lower() for s in dictionary.read().splitlines() if len(s) >= 6]

    @commands.command(pass_context=True, name="hangman", description="Haver si adivinas la palabra")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hangman_command(self, ctx):
        hangman = HangmanGame(random.choice(self.words))
        msg = await ctx.send(embed=self.render_embed(hangman))
        self.games[msg.id] = hangman

    


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        if payload.message_id in self.games and guild is not None and len(payload.emoji.name) == 1:
            letter = chr(ord(payload.emoji.name) - 127365)
            if letter >= 'a' and letter <= 'z':
                channel = guild.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                hangman = self.games[payload.message_id]
                hangman.guess(letter)
                if '*' not in hangman.visible:
                    del self.games[payload.message_id]
                await message.edit(embed=self.render_embed(hangman))
                await message.clear_reaction(payload.emoji)

    
    def render_embed(self, hangman: HangmanGame):
        global hangman_embed
        embed = hangman_embed.copy()

        head = '()' if hangman.errors > 0 else '  '
        torso = '||' if hangman.errors > 1 else '  '
        left_arm = '/' if hangman.errors > 2 else ' '
        right_arm = '\\' if hangman.errors > 3 else ' '
        left_leg = '/' if hangman.errors > 4 else ' '
        right_leg = '\\' if hangman.errors > 5 else ' '
        diagram = f"``` {head}\n{left_arm}{torso}{right_arm}\n {left_leg}{right_leg}```"

        embed.add_field(name="Diegtrama", value=diagram)
        embed.add_field(name="Palabra", value=' '.join("🟦" if c == '*' else chr(ord(c) + 127365) for c in hangman.visible))

        embed.add_field(name="\u200b", value="\u200b")

        if len(hangman.guesses) > 0:
            embed.add_field(name="Suposiciones", value=' '.join(chr(ord(c) + 127365) for c in hangman.guesses) + "\n\n\n")

        if hangman.errors > 5:
            embed.add_field(name="Resultado:", value=f"¡Has perdido!")
        elif '*' not in hangman.visible:
            embed.add_field(name="Resultado:", value=f"¡Has ganado!")

        return embed


def setup(bot):
    bot.add_cog(Hangman(bot))
