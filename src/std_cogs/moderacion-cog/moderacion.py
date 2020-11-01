import discord 
from discord.ext import commands
import time
import json
from discord import guild
from termcolor import cprint
from os import environ as env
color =  int(env["COLOR"])

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Quita mensajes de el chat", usage="[num]")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        msg = await ctx.send(f'Se an borrado {amount} mensajes')
        time.sleep(1.2)
        await msg.delete()

    @commands.command(description="Expulsa ha alguien", usage="<usuario> [razon]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)    
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        
        await member.kick(reason=reason)
        embed = discord.Embed(title=f"Eliminado", description=f"Se a eliminado a {member.mention} del servidor",colour=color)
        await ctx.send(embed=embed)

    @commands.command(description="Banea ha alguien", usage="<usuario> [razon]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, razon=None):

        if razon is None:
            await member.ban(reason=razon)
            embed = discord.Embed(title=f"Baneado", description=f"Se a baneado a {member.mention} del servidor",colour=color)
            return await ctx.send(embed=embed)
        await member.ban(reason=razon)
        embed = discord.Embed(title=f"Baneado", description=f"Se a baneado a {member.mention} del servidor\n\n**Razon** {razon}",colour=color)
        await ctx.send(embed=embed)
        

    @commands.command(description="Desbanea a un baneado **uso: $unban <id del usuario>**", usage="<id del usuario>")
    @commands.has_permissions(manage_messages=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member=None):
        if not member is None:
            member = await self.bot.fetch_user(int(member))
            await ctx.guild.unban(user=member, reason="Se le a quitado el baneo")
            embed = discord.Embed(title=f"Desbaneado", description=f"Se a desbaneado a {member.mention} del servidor",colour=color)
            return await ctx.send(embed=embed)
        else:
            return await ctx.send("**uso: $unban <id del usuario>**")
        

    @commands.command(pass_context=True, description="Haz un haviso ha alguien", usage="<usuario> [razon]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def warn(self, ctx, member: discord.Member, *, razon="Sin especificar"):
        with open('./src/json/warnings.json', 'r') as f:
            warns = json.load(f)
        # print(warns)
        try:
            if not str(ctx.guild.id) in warns:
                warns[str(ctx.guild.id)] = {}
            if str(member.id) in warns[str(ctx.guild.id)]:
                warns[str(ctx.guild.id)][str(member.id)]["warns"] += 1
                warns[str(ctx.guild.id)][str(member.id)]["razones"].append(razon)          
            else:
                warns[str(ctx.guild.id)][str(member.id)] = {}
                warns[str(ctx.guild.id)][str(member.id)]["warns"] = 1
                warns[str(ctx.guild.id)][str(member.id)]["razones"] = []
                warns[str(ctx.guild.id)][str(member.id)]["razones"].append(razon)
        except Exception as e:
            cprint(f"[log] Un problema:  {e}", 'red')
        if warns[str(ctx.guild.id)][str(member.id)]["warns"] >= 5:
            try:
                await member.kick(reason="Mas de 5 warniciones")
                embed = discord.Embed(title="Expulsado", description=f"{member.mention} ha sido expulsado  Razon: Mas de 5 warniciones", colour=color)   
                del warns[str(ctx.guild.id)][str(member.id)]
                return await ctx.send(embed=embed)
            except:
                cprint('[Log] Un error intentando eliminar a alguien por 5 warniciones', 'red')
                return await ctx.send(f"En error intentando eliminar a {member.mention}, Razon: Mas de 5 warniciones")
        with open("./src/json/warnings.json","w") as f:
            json.dump(warns,f)    
        embed = discord.Embed(title="Warnicion", description=f"{member.mention}  Razon: {razon}\n\nLe quedan {5-warns[str(ctx.guild.id)][str(member.id)]['warns']} warniciones", colour=color)   
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, description="Quitale el aviso ha alguien", usage="<usuario>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def unwarn(self, ctx, member: discord.Member):
        with open('./src/json/warnings.json', 'r') as f:
            warns = json.load(f)
        if str(member.id) in warns[str(ctx.guild.id)]:
            warns[str(ctx.guild.id)][str(member.id)]["warns"] -= 1
            warns[str(ctx.guild.id)][str(member.id)]["razones"].remove(warns[str(ctx.guild.id)][str(member.id)]["razones"][warns[str(ctx.guild.id)][str(member.id)]["warns"]])
        if warns[str(ctx.guild.id)][str(member.id)]["warns"] == 0:
            del warns[str(ctx.guild.id)][str(member.id)]
        if warns[str(ctx.guild.id)] == {}:
            del warns[str(ctx.guild.id)]
        with open("./src/json/warnings.json","w") as f:
            json.dump(warns,f)    
        embed = discord.Embed(title="Warnicion quitada", description=f"{member.mention}  Se le a quitado una guarnicion\n\nLe quedan warniciones, ({ctx.prefix}warnlist @usuario para ver la lista)", colour=color)   
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, description="La lista de warniciones que alguien tendra", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def warnlist(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        with open('./src/json/warnings.json', 'r') as f:
            warns = json.load(f)
        if not str(member.id) in warns[str(ctx.guild.id)]:
            return await ctx.send("Este usuario no tiene warniciones")
        embed = discord.Embed(title="Lista de warniciones", description=f"{member.mention}  Tiene:", colour=color) 
        for index in range(0, warns[str(ctx.guild.id)][str(member.id)]["warns"]):
            embed.add_field(name=f"{index + 1} | {warns[str(ctx.guild.id)][str(member.id)]['razones'][index]}", value="--------------", inline=False)
        with open("./src/json/warnings.json","w") as f:
            json.dump(warns,f)    
        embed.set_footer(text=f"Si tiene 5 warniciones {member.mention} sera expulsado")
        await ctx.send(embed=embed)

    @commands.command(description="Mutea ha alguien", usage="<usuario> [razon]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        
        with open("./src/json/mute.json", "r") as f:
            user = json.load(f)


        if not str(member.id) in user:
            user[str(member.id)] = {}
            user[str(member.id)]["razon"] = reason
        else:
            await ctx.send("Ese usuario ya estra baneado")

        with open("./src/json/mute.json", "w") as f:
            json.dump(user, f)

        await ctx.send(embed=discord.Embed(title="Muteado", description=f"{ctx.author.mention}, se ha muteado a {member.mention}", color=color))

    @commands.command(description="Desmutea ha alguien", usage="<usuario>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member):
        
        with open("./src/json/mute.json", 'r') as f:
            user = json.load(f)

        if str(member.id) in user:
            del user[str(member.id)]
        else:
            await ctx.send("Ese usuario no esta muteado")

        with open("./src/json/mute.json", "w") as f:
            json.dump(user, f)

        await ctx.send(embed=discord.Embed(title="Desmuteado", description=f"{ctx.author.mention}, se ha desmuteado a {member.mention}", color=color))

    @commands.command(description="Crea una nueba categoria", usage="<nombre>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def new_category(self, ctx, *, cat):
        category = await ctx.guild.create_category(name=f'{cat}')
        embed = discord.Embed(title="Categoria echa", description=f"Hola, acabo de crear una nueva categoria --- **({category.name})**", colour=color)
        await ctx.send(embed=embed)

    @commands.command(description="Nuevo canal de texto", usage="<nombre>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def new_textchannel(self, ctx, *, cha):
        channel = await ctx.guild.create_text_channel(name=f'{cha}')
        embed = discord.Embed(title="Categoria echa", description=f"Hola, acabo de crear un nuevo canal de texto --- **({channel})**", colour=color)
        await ctx.send(embed=embed)


    @commands.command(description="Crea un canal de voz", usage="<nombre>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def new_voicechannel(self, ctx, *, vc):
        vc = await ctx.guild.create_voice_channel(name=f'{vc}')
        embed = discord.Embed(title="Categoria echa", description=f"Hola, acabo de crear un nuevo canal de voz --- **({vc})**", colour=color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))