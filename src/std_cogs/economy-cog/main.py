import discord 
from discord.ext import commands
import json
from os import environ as env
import random

from utils.Logger.Logger import Logger
from termcolor import cprint

color = int(env["COLOR"])
C_NAMES = "🪙"


mainshop = []
with open("./src/utils/shop.json") as f:
    mainshop = json.load(f)

mainshop = mainshop["shop"]

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open(env["JSON_DIR"] + "mainbank.json","w") as f:
        json.dump(users,f, indent=4)

    await update_bank(user, cost*-1, "wallet")

    return [True,"Worked"]

async def sell_this(user,item_name,amount,price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]   

    if users[str(user.id)]["bag"][index]["amount"] == 0:
        del users[str(user.id)]["bag"][index]

    with open(env["JSON_DIR"] + "mainbank.json","w") as f:
        json.dump(users,f, indent=4)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]


async def get_bank_data():
    with open(env["JSON_DIR"] + "mainbank.json", "r") as f:
        users = json.load(f)

    return users

async def open_acount(user):

    users = await get_bank_data()

    with open(env["JSON_DIR"] + "mainbank.json","r") as f:
        users = json.load(f)

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open(env["JSON_DIR"] + "mainbank.json","w") as f:
        json.dump(users, f, indent=4) 
    return True

async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open(env["JSON_DIR"] + "mainbank.json", "w") as f:
        json.dump(users, f, indent=4)        
    
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal




# COMANDOS



class Economia(commands.Cog):
    
    def __init__(self, app):
        self.bot = app

    @commands.command(aliases=["bal"], description="Enseña el dinero de tu cuenta", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx, member: discord.Member=None):
        if member is None:
            member = ctx.author

        await open_acount(member)
        user = member
        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"] 
        bank_amt = users[str(user.id)]["bank"] 

        embed = discord.Embed(title=f"Cuenta bankaria de {member.name}", description=f"La cuenta de dinero de {member.mention}",colour=color)
        embed.add_field(name="Cartera", value=f"{wallet_amt} {C_NAMES}", inline=True)
        embed.add_field(name="Banco", value=f"{bank_amt} {C_NAMES}", inline=True)
        try:
            embed.add_field(name="Objetos", value=f"{len(users[str(user.id)]['bag'])}", inline=True)
        except:
            Logger.info(f"El usuario {member} no tiene bolsa asique se la pasa el \"field\"")
        embed.set_footer(text=f"Puedes escribir {ctx.prefix}bag para ver tu inventario", icon_url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description="Pide dinero a la gente")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        await open_acount(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        earnings = random.randrange(1001)

        await ctx.send(f"¡Felicidades! Alguien te a dado **{earnings}** {C_NAMES}")

        users[str(user.id)]["wallet"] += earnings

        with open(env["JSON_DIR"] + "mainbank.json", "w") as f:
            json.dump(users, f, indent=4)         

    @commands.command(description="Deposita tu dinero al banko (Tienes que tener dinero en la cartera)", usage="[cantidad]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def deposit(self, ctx, amount: int=None):
        await open_acount(ctx.author)

        if amount is None:
            await ctx.send(f"Porfavor pon cuantos {C_NAMES} quieres mete en el banko")
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send(f"¡Tu no tienes tantos {C_NAMES}!")
            return  
        if amount<0:
            await ctx.send(f"¿Que tal si pones mas de 0 {C_NAMES}?")
            return  

        await update_bank(ctx.author,-1*amount)
        await update_bank(ctx.author,amount, "bank")

        await ctx.send(embed=discord.Embed(title="Conseguido", description=f"Se han metido {amount} {C_NAMES} en tu cuenta bancaria", colour=color))

    @commands.command(description="Poner dinero en la cartera (Tienes que tener dinero en el banko)", usage="[cantidad]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def withdraw(self, ctx, amount=None):
        await open_acount(ctx.author)

        if amount is None:
            await ctx.send(f"Porfavor pon cuantos {C_NAMES} quieres mete en el banko")
            return



        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[1]

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send(f"¡Tu no tienes tantos {C_NAMES}!")
            return  
        if amount<0:
            await ctx.send(f"¿Que tal si pones mas de 0 {C_NAMES}?")
            return  

        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount, "bank")

        await ctx.send(embed=discord.Embed(title="Conseguido", description=f"Se han metido {amount} {C_NAMES} en tu cartera", colour=color))

    @commands.command(aliases=["give"], description="Transfiere dinero a un @usuario", usage="<usuario> [cantidad]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def transfere(self, ctx, member: discord.Member,amount=None):
        await open_acount(ctx.author)
        await open_acount(member)

        if amount is None:
            await ctx.send(f"Porfavor pon cuantos {C_NAMES} quieres transferir")
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            amount = bal[0]

        amount = int(amount)
        if amount>bal[1]:
            await ctx.send(f"¡Tu no tienes tantos {C_NAMES}!")
            return  
        if amount<0:
            await ctx.send(f"¿Que tal si pones mas de 0 {C_NAMES}?")
            return  

        await update_bank(ctx.author,-1*amount, "bank")
        await update_bank(member,amount, "bank")

        await ctx.send(embed=discord.Embed(title="Conseguido", description=f"Se han metido {amount} {C_NAMES} en su cuenta bancaria", colour=color))

    @commands.command(aliases=["slot"], description="Haver si ganas un premio", usage="[cantidad]")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def slots(self, ctx, amount=None):
        await open_acount(ctx.author)

        if amount is None:
            await ctx.send(f"Porfavor pon cuantos {C_NAMES} quieres mete en el banko")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount>bal[0]:
            await ctx.send(f"¡Tu no tienes tantos {C_NAMES}!")
            return  
        if amount<0:
            await ctx.send(f"¿Que tal si pones mas de 0 {C_NAMES}?")
            return  

        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a}, {b}, {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} Todo coincide, ¡Has ganado! 🎉")
            await update_bank(ctx.author,3*amount)
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 en una linea, ¡Has ganado! 🎉")
            await update_bank(ctx.author,2*amount)
        else:
            await ctx.send(f"{slotmachine} Nada, has perdido 😢")
            await update_bank(ctx.author,-1*amount)

    @commands.command(aliases=["rob"], description="Roba ha alguien", usage="[usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def steal(self, ctx, member: discord.Member):
        await open_acount(ctx.author)
        await open_acount(member)

        bal = await update_bank(member)

        if bal[0]<100:
            await ctx.send(f"Este usuario tiene **menos** de 100 {C_NAMES} ¡No vale la pena!")
            return 

        earnings = random.randrange(0, bal[0])

        await update_bank(ctx.author,earnings)
        await update_bank(member,-1*earnings)

        await ctx.send(embed=discord.Embed(title="GG", description=f"Has conseguido robar {earnings} {C_NAMES} a {member.mention}", colour=color))

    @commands.command(description="Mira la compra")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shop(self, ctx):
        embed = discord.Embed(colour=color)
        embed.set_author(name="Tienda", icon_url="https://img.icons8.com/ultraviolet/48/000000/amazon.png")
        for item in mainshop:
            name=item["name"]
            price=item["price"]
            description=item["description"]
            embed.add_field(name=f"{name} | __{price}__  {C_NAMES}", value=f"{description}", inline=False)

        embed.set_footer(text=f"Puedes poner {ctx.prefix}buy para comprar algo", icon_url="https://img.icons8.com/ultraviolet/48/000000/amazon.png")
        await ctx.send(embed=embed)

    @commands.command(description="Compra algo en la tienda", usage="<objeto> [cantidad]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy(self, ctx, item, amount = 1):
        await open_acount(ctx.author)

        res = await buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send(embed=discord.Embed(title="¡Ese objeto no esta hay!", colour=color))
                return
            if res[1]==2:
                await ctx.send(embed=discord.Embed(title=f"Tu **no** tienes suficiente {C_NAMES} para comprar {amount} {item}/s", colour=color))
                return


        await ctx.send(embed=discord.Embed(title=f"Te acavas de comprar {amount} {item}", colour=color))


    @commands.command(description="Mira tu inventario")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bag(self, ctx):

        await open_acount(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            cprint(f"[Log] Un error en \"economy-cog.main\": {e}", "red")
            bag = []


        em = discord.Embed(colour=color)
        em.set_author(name="Inventario", icon_url="https://img.icons8.com/color/48/000000/chalk-bag.png")
        inv = ""
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            inv += f"{name}: {amount}\n"    
        
        em.add_field(name="Objetos:", value=inv)

        await ctx.send(embed=em)   

    def GetUse(self, item):
        for i in mainshop:
            if i["name"].lower() == item:
                return i["uso"]
        return "*No se encontro uso*"

    @commands.command(description="Vende un objeto de tu inventario", usage="<objeto> [@usuario]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def use(self, ctx, obj: str = None, usr: discord.Member = None):

        if obj is None: return await ctx.send("Porfavor incluye un objeto")

        usr = ctx.author if usr is None else usr
        await open_acount(ctx.author)

        users = await get_bank_data()
        
        if not str(ctx.author.id) in users: return await ctx.send("Tu no tuenes una cuenta. `m.balance` para crearse una")

        try:
            users[str(ctx.author.id)]["bag"]
        except:
            return await ctx.send("No tienes una bolsa pon `m.balance` para crearte una")

        for thing in users[str(ctx.author.id)]["bag"]:
            item = obj.lower()
            if thing["item"].lower() == item:
                try:
                    for ind, it in enumerate(users[str(ctx.author.id)]["bag"]):
                        if it["item"] == item:
                            num = ind
                    users[str(ctx.author.id)]["bag"][num]["amount"] -= 1
                    if users[str(ctx.author.id)]["bag"][num]["amount"] == 0:
                        del users[str(ctx.author.id)]["bag"][num]
                    with open(env["JSON_DIR"] + "mainbank.json","w") as f:
                        json.dump(users, f, indent=4)
                    desc = self.GetUse(item)
                    embed = discord.Embed(color=color, title=random.choice(["¡Saves usar algo!", f"{ctx.author.name} ha usado un objeto"]))
                    embed.description = f"{ctx.author.mention} as usado un/a {item} para {usr.mention if usr.id != ctx.author.id else 'si mismo'}"
                    embed.add_field(name="Uso:", value=desc)
                    return await ctx.send(embed=embed)
                except Exception as e: 
                    return await ctx.send(f"Un pequeño error ha ocurrido\n``` {e} ```")
        await ctx.send("Tu no tienes ese objeto")


    @commands.command(description="Vende un objeto de tu inventario", usage="<objeto> [cantidad]")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def sell(self, ctx, item, amount=1):
        await open_acount(ctx.author)

        res = await sell_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                return await ctx.send("¡Ese objeto no existe!")
            if res[1]==2:
                return await ctx.send(f"¡Tu no tienes {amount} {item}s en tu inventario!")
            if res[1]==3:
                return await ctx.send(f"No tienes {item} en tu inventario")

        await ctx.send(embed=discord.Embed(title="Conseguido", description=f"Se a conseguido vender {amount} {item}/s", colour=color))

    @commands.command(aliases=["top"], description="Mira las personas mas ricas")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leaderboard(self, ctx, x=3):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        embed = discord.Embed(title=f"Top {x} personas mas ricas", description=f"Esto esta decidido a el dinero de el banco y la cartera puedes poner `{ctx.prefix}balance` para ver tus {C_NAMES}", colour=color)
        embed.add_field(name=f"#1 | Maubot (yo)", value=f"**∞** {C_NAMES}", inline=False)
        index = 2
        for amt in total:
            try:
                id_ = leader_board[amt]
                member = self.bot.get_user(int(id_))
                name = member.name
                if not member.id == ctx.author.id:
                    embed.add_field(name=f"#{index} | {name}", value=f"{amt} {C_NAMES}", inline=False)
                else:
                    embed.add_field(name=f"#{index} | {name} (Tu)", value=f"{amt} {C_NAMES}", inline=False)

                if index == x:
                    break
                else:
                    index += 1
            except: continue
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Economia(bot))
