import discord
from discord.ext import commands
import json
from os import environ as env
color = int(env["COLOR"])

class AfkCmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['AFK', 'afuera'], description="Dile a la gente que no estas disponible", usage="[razon]")
    async def afk(self, ctx: commands.Context, *, razon: str = "AFK"):

        user = ctx.author

        with open(env["JSON_DIR"] + "afk.json", "r") as f:
            users = json.load(f)
        
        if str(user.id) in users:
            users[str(user.id)]["afk"] = "1"
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["afk"] = "1"
            users[str(user.id)]["status"] = "False"
            users[str(user.id)]["razon"] = razon

        with open(env["JSON_DIR"] + "afk.json", "w") as f:
            json.dump(users,f)        
        
        await ctx.send(embed=discord.Embed(title="Usuario AFK", description=f"{user.mention} Ha sido puesto en **AFK** por favor no lo molesteis", colour=color).add_field(name="Razon", value=razon))


    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        menciones = []
        if len(message.mentions) > 0:
            for i in message.mentions: menciones.append(i)

        with open(env["JSON_DIR"] + "afk.json", "r") as f:
            users = json.load(f)

        for i in menciones:
            if str(i.id) in users: await message.channel.send(embed=discord.Embed(title="¿No saves leer?", color=color, description=f"{user.mention}, Como dice bien **mi** mensage {i.mention} esta AFK\n\n**Razon:** {users[str(i.id)]['razon']}"))

        if str(user.id) in users:   
            try:
                if users[str(user.id)]["status"] == "True":
                    del users[str(user.id)]

                    await message.channel.send(embed=discord.Embed(title="Mira quien ha vuelto", description=f"{user.mention} ha vuelto de su descanso. **bienvenido**",colour=color))

                if users[str(user.id)]["afk"] == "1":
                    users[str(user.id)]["status"] = "True"

                with open(env["JSON_DIR"] + "afk.json", "w") as f:
                    json.dump(users,f)    
            except: pass

def setup(bot):
    bot.add_cog(AfkCmd(bot))
