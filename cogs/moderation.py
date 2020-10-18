import discord 
from discord.ext import commands
import time
import json

color = 0x75aef5 

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        msg = await ctx.send(f'Se an borrado {amount} mensajes')
        time.sleep(1.2)
        await msg.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)    
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        
        await member.kick(reason=reason)
        embed = discord.Embed(title=f"Eliminado", description=f"Se a eliminado a {member.mention} del servidor",colour=color)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):

        
        await member.ban(reason=reason)
        embed = discord.Embed(title=f"Baneado", description=f"Se a baneado a {member.mention} del servidor",colour=color)
        await ctx.send(embed=embed)
        

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(user=member, reason="Se le a quitado el baneo")
        embed = discord.Embed(title=f"Desbaneado", description=f"Se a desbaneado a {member.mention} del servidor",colour=color)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def warn(self, ctx, member: discord.Member, *, razon="Sin especificar"):
        with open('./json/warnings.json', 'r') as f:
            warns = json.load(f)
        if str(member.id) in warns:
            warns[str(member.id)]["warns"] += 1
        else:
            warns[str(member.id)] = {}
            warns[str(member.id)]["warns"] = 1
        if warns[str(member.id)]["warns"] == 5:
            await member.kick(reason="Mas de 5 warniciones")
            embed = discord.Embed(title="Expulsado", description=f"{member.mention} ha sido expulsado  Razon: Mas de 5 warniciones", colour=color)   
            return await ctx.send(embed=embed)
        with open("./json/warnings.json","w") as f:
            json.dump(warns,f)    
        embed = discord.Embed(title="Warnicion", description=f"{member.mention}  Razon: {razon}\n\nLe quedan {5-warns[str(member.id)]['warns']} warniciones", colour=color)   
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def unwarn(self, ctx, member: discord.Member):
        with open('./json/warnings.json', 'r') as f:
            warns = json.load(f)
        if str(member.id) in warns:
            warns[str(member.id)]["warns"] -= 1
        with open("./json/warnings.json","w") as f:
            json.dump(warns,f)    
        embed = discord.Embed(title="Warnicion quitado", description=f"{member.mention}  Se le a quitado una guarnicion\n\nLe quedan {5-warns[str(member.id)]['warns']} warniciones", colour=color)   
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def warnlist(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author
        with open('./json/warnings.json', 'r') as f:
            warns = json.load(f)
        embed = discord.Embed(title="Lista de warniciones", description=f"{member.mention}  Tiene", colour=color) 
        if warns[str(member.id)]["warns"] == 0:
            return await ctx.send("Este usuario to tiene guarniciones")
        print(warns[str(member.id)]["warns"])
        embed.add_field(name="Warniciones", value=f"{warns[str(member.id)]['warns']}", inline=False)
        with open("./json/warnings.json","w") as f:
            json.dump(warns,f)    
        embed.add_field(name="\uFEFF", value="Si tiene 5 warniciones sera expulsado")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        
        await ctx.member.mute(reason=reason)
        await ctx.send("{} a sido muteado".format(member.mention,ctx.author.mention))



    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def new_category(self, ctx, *, cat):
        category = await ctx.guild.create_category(name=f'{cat}')
        embed = discord.Embed(title="Categoria echa", description=f"Hola, acabo de crear una nueva categoria --- **({category.name})**", colour=color)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def new_textchannel(self, ctx, *, cha):
        channel = await ctx.guild.create_text_channel(name=f'{cha}')
        embed = discord.Embed(title="Categoria echa", description=f"Hola, acabo de crear un nuevo canal de texto --- **({channel})**", colour=color)
        await ctx.send(embed=embed)


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    async def new_voicechannel(self, ctx, *, vc):
        vc = await ctx.guild.create_voice_channel(name=f'{vc}')
        embed = discord.Embed(title="Categoria echa", description=f"Hola, acabo de crear un nuevo canal de voz --- **({vc})**", colour=color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))