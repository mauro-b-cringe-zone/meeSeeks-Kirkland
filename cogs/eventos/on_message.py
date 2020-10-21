import discord
from discord.ext import commands
import json
import time
from os import environ as env
color = int(env["COLOR"])

class MessageListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content == "<@!730124969132163093>":
            # file = discord.File("assets/Maubot_tutorial.gif", filename="Maubot_tutorial.gif")
            await message.channel.send(embed=discord.Embed(title="Deja que me presente", 
                                                           description="Hola, mi nombre es Maubot. Si quieres conocer todos mis comandos, usa la ayuda de comandos, es bastante fácil usar todos mis comandos y dominarlos. Si quieres usar todos mis comandos, mi prefijo es (**$**) Y para ver mis commandos solo pon **$help**", 
                                                           colour=color).set_image(url="https://i.gyazo.com/f38490f1ddd304169f60fb1581b53eda.png").add_field(name="Mis comandos", value="¿No saves que hacer? Puedes poner `$help [Seccion]` y veras todos mis comandos disponibles. Si tienes cosas que decir siempre puedes poner `$rate_bot <Reseña>` y te responderemos **lo mas rapido** posible").add_field(name="¿Para que sirvo?", value="Mi dever en tu servidor es hacer que la gente se divierta con mis memes, que la gente le guste la musica y mi sistema de dinero, que el servidor sea bonito y **¡Mucho mas!**"))


        with open("./json/userslvl.json", "r") as f:
            users = json.load(f)

        await self.update_data(users, message.author)
        await self.add_experience(users, message.author, 5)
        await self.level_up(self.bot, users, message.author, message.channel)

        with open("./json/userslvl.json", "w") as f:
            json.dump(users, f)
        # await self.bot.process_commands(message)

    async def update_data(self, users, user):
        if not str(user.id) in users:
            users[str(user.id)] = {}
            users[str(user.id)]["experience"] = 0
            users[str(user.id)]["level"] = 1
            users[str(user.id)]["last_message"] = 0

    async def add_experience(self, users, user, exp):
        users[str(user.id)]["experience"] += exp
        users[str(user.id)]["last_message"] = time.time()

    async def level_up(self, bot, users, user, channel):
        experience = users[str(user.id)]["experience"]
        lvl_start = users[str(user.id)]["level"]
        lvl_end = int(experience ** (1/4))

        if lvl_start < lvl_end and not user.id == 730124969132163093 and not user.id == 755433402299056139:
            await channel.send(embed=discord.Embed(title=f':tada: ¡felicidades!', description=f'{user.mention}, has subido al nivel {lvl_end}! :champagne_glass: ', colour=color))
            users[str(user.id)]['level'] = lvl_end

    def nivel(self, nivel):
        exp = int(nivel - (1/4))
        return exp

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        with open("./json/userslvl.json", "r") as f:
            users = json.load(f)

        if user is None:
            user = ctx.author

        experience = users[str(user.id)]["experience"]
        lvl_end = int(experience ** (1/4))

        exp_res = self.nivel(lvl_end)
        # print(exp_res)
        
        if not str(user.id) in users:
            await ctx.send(f"El usuarion {user} aun no tiene un rango.")
        else:
            embed = discord.Embed(description=f"{user.mention} te quedan `{exp_res}` de experiencia para suvir de nivel", colour=color)
            embed.set_author(name=f"nivel - {user.name}", icon_url=user.avatar_url)
            embed.add_field(name="nivel", value=users[str(user.id)]["level"], inline=True)
            embed.add_field(name="exp", value=users[str(user.id)]["experience"], inline=True)
            await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(MessageListener(bot))