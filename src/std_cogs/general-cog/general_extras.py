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
from utils.fun.lists import drunkaf, fight_results, insults, honkhonkfgt
import hashlib
from os import environ as env
import requests
color = int(env["COLOR"])

class GeneralSecExtra(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="(╯°□°）╯︵ ┻━┻")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tableflip(self, ctx):
        await ctx.send(embed=discord.Embed(color=color).set_image(url=f'https://vacefron.nl/api/tableflip?user={ctx.author.avatar_url}?size=2048'))

    @commands.command(description="┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def doubleflip(self, ctx):
        await ctx.send("┻━┻ ﾐヽ(ಠ益ಠ)ノ彡┻━┻")

    @commands.command(description="¡¡¡Que careto!!!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def water(self, ctx: commands.Context, *, message):
        if len(message) >= 10:
            return await ctx.send("No tanto texto")
        await ctx.send(embed=discord.Embed(color=int(color)).set_image(url=f'https://vacefron.nl/api/water?text={str(message.replace(" ", "%20"))}'))

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
        with open('./src/utils/languages/spanish.json', 'r') as f:
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
        await ctx.send(embed=discord.Embed(color=color, description="🔁 " + msg[::-1]))

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

    @commands.command(description="NO TU")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def notu(self, ctx):
        await ctx.message.delete()
        await ctx.send("no tu")


def setup(bot):
    bot.add_cog(GeneralSecExtra(bot))
