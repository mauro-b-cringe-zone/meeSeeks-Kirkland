import discord
from discord.ext import commands
import asyncio
from os import environ as env
color = int(env["COLOR"])
import random
import time
import json
from googletrans import Translator
from json import loads as jsonify
from urllib.request import urlopen as getapi
import requests
from termcolor import cprint

class Games(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command(description="Piedra, Papel o tijera...")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rps(self, ctx, respuesta: str = ""):
        

        if respuesta == "":
            embed = discord.Embed(title="Como jugar", description=f"Para jugar tu tienes que mete una respuesta **<piedra | papel | tijera>** Solo se puede jugar contra la maquina\n\n**Ejemplo**\n{ctx.prefix}rps piedra\n",colour=color)
            await ctx.send(embed=embed)    



        eleccion = ["tijera", "papel", "piedra"]


        # 1: Ganas
        # 2: Empatas
        # 3: Pierdes

        puntuacion = {}
        # MAQUINA, HUMANO
        puntuacion[('piedra', 'piedra')] = 2
        puntuacion[('piedra', 'papel')] = 1
        puntuacion[('piedra', 'tijera')] = 3
        puntuacion[('papel', 'piedra')] = 3
        puntuacion[('papel', 'papel')] = 2
        puntuacion[('papel', 'tijera')] = 1
        puntuacion[('tijera', 'piedra')] = 1
        puntuacion[('tijera', 'papel')] = 3
        puntuacion[('tijera', 'tijera')] = 2

        eleccion_final = random.choice(eleccion)

        RESULTADO = puntuacion[eleccion_final, respuesta]

        if RESULTADO == 3:
            await ctx.send(embed=discord.Embed(title="¡Has perdido!", description=f"La eleccion de la maquina a sido **{eleccion_final}**\n Por lo que significa que has perdido 🤭",colour=color)) 

        if RESULTADO == 2:
            await ctx.send(embed=discord.Embed(title="¡Has empatado!", description=f"La eleccion de la maquina a sido **{eleccion_final}**\n Por lo que significa que has empatado 🤨",colour=color)) 

        if RESULTADO == 1:
            await ctx.send(embed=discord.Embed(title="¡Has ganado!", description=f"La eleccion de la maquina a sido **{eleccion_final}**\n Por lo que significa que has ganaado 🤬",colour=color)) 


    

    @commands.command(name='connect4', description="Juega al conecta 4")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def connect4(self,ctx, opponent="", width=7, height=6):
        #-------------- ayuda ------------------#
        if(opponent==""):
            em = discord.Embed()
            em.title = f'Como se usa: {ctx.prefix}connect4 [oponente] [largo] [alto]'
            em.description = f'Desafía al oponente a un juego de conectar 4. El oponente debe ser @mencionado para comenzar\nLa placa tiene un tamaño predeterminado de 7x6 si no se especifica, aunque normalmente no necesitará ninguna placa más grande que esa..\nEl volumen máximo de la placa es 95 debido a limitaciones de caracteres'
            em.add_field(name="Ejemplo", value=f"{ctx.prefix}connect4 **@mencionado**\n{ctx.prefix}connect4 **@mencionado 10 9**", inline=False)
            em.colour = color
            await ctx.send(embed=em)
            return
        #----------------------------------------------#
        await ctx.message.delete()
        
        zrw = ""

        resized = False
        if(width*height > 95):
            width = 7
            height = 6
            resized = True
            zrw = "grande"

        if(width*height < 42):
            width = 7
            height = 6
            resized = True
            zrw = "pequeña"
        
        player1 = ctx.message.mentions[0].name
        player2 = ctx.message.author.name
        s = ':black_circle:'
        p1 = ':blue_circle:'
        p2 = ':red_circle:'
        board = []
        for column in range(height):
            rowArr = []
            for row in range(width):
                rowArr.append(s)
            board.append(rowArr)
        def getDisplay():
            toDisplay = ""
            for y in range(height):
                for x in range(width-1):
                    toDisplay+=board[y][x]+'|'
                toDisplay+=board[y][width-1] + '\n'
            return(toDisplay)
        
        boardMessage = None
        em = discord.Embed()
        if(player1==player2):
            em.title = f"{player2} se desafiaron a un juego de Connecta 4 \n(Wow estas solo)"
        else:
            em.title = f'{player2} a desafiado {player1} a un juego de Connecta 4'
        em.description = f"{getDisplay()}"
        em.colour = color
        em.add_field(name=f"{player1}", value=f"Escriba un número del 1-{width} para aceptar y colocar su primera pieza, o escriba 'rechazar' para rechazar", inline=False)
        if resized:
            em.add_field(name="Nota", value=f"La longitud original de la placa era demasiado {zrw}, por defecto era 7x6", inline=False)
        await ctx.send(embed=em)
        async for x in ctx.channel.history(limit = 1):
            boardMessage = x
        badInput = 0
        turns = 1
        currentPlayer = player1
        otherPlayer = player2
        currentPlayerId=1
        while True:
            try:
                msg = await self.bot.wait_for("message", check=lambda message: message.author.name == player1, timeout=30)
                if(msg.content=='rechazar'):
                    em = discord.Embed()
                    if(player1==player2):
                        em.title = f"{player2} se desafiaron a un juego de Connecta 4 (Wow estas solo)"
                    else:
                        em.title = f'{player2} a desafiado {player1} a un juego de Connecta 4'
                    em.description = f"{getDisplay()}"
                    em.colour = color
                    em.add_field(name=f"{player1}", value="Desafío rechazado", inline=False)
                    await boardMessage.edit(embed=em)
                    return
                
                slot = int(msg.content)
                if(slot<1 or slot>width):
                    raise ValueError
                await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                board[height-1][slot-1] = p1
                gameLoop = True
                currentPlayer = player2
                otherPlayer = player1
                turns +=1
                currentPlayerId=2
                break;
            except asyncio.TimeoutError:
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} se desafiaron a un juego de Connecta 4 (Wow estas solo)"
                else:
                    em.title = f'{player2} a desafiado {player1} a un juego de Connecta 4'
                em.description = f"{getDisplay()}"
                em.colour = color
                em.add_field(name=f"{player1}", value="Tiempo de juego agotado", inline=False)
                await boardMessage.edit(embed=em)
                return
            except ValueError:
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} se desafiaron a un juego de Connecta 4 (Wow estas solo)"
                else:
                    em.title = f'{player2} a desafiado {player1}  a un juego de Connecta 4'
                em.description = f"{getDisplay()}"
                em.colour = color
                em.add_field(name=f"{player1}", value=f"Ingrese un número válido entre 1-{width}", inline=False)
                await boardMessage.edit(embed=em)
                badInput+=1
            if(badInput==3):
                em = discord.Embed()
                if(player1==player2):
                    em.title = f"{player2} se desafiaron a un juego de Connecta 4 (Wow estas solo)"
                else:
                    em.title = f'{player2} a desafiado {player1} a un juego de Connecta 4'
                em.description = f"{getDisplay()}"
                em.colour = color
                em.add_field(name=f"{player1}", value="No ingresó un número válido en 3 intentos. El juego terminó.", inline=False)
                await boardMessage.edit(embed=em)
                return
        winningComment=""
        winner=""
        while gameLoop:
            if(turns==width*height):
                winner=None
                break;
            ################################
            #Combinaciones#
            ################################
            # Horizontal
            for y in range(height):
                for x in range(width-3):
                    if(board[y][x]==board[y][x+1] and board[y][x]==board[y][x+2] and board[y][x]==board[y][x+3] and board[y][x]!=s):
                        if(board[y][x]==p1):
                            board[y][x] = ':large_blue_diamond:'
                            board[y][x+1] = ':large_blue_diamond:'
                            board[y][x+2] = ':large_blue_diamond:'
                            board[y][x+3] = ':large_blue_diamond:'
                        elif(board[y][x]==p2):
                            board[y][x]=":diamonds:"
                            board[y][x+1]=":diamonds:"
                            board[y][x+2]=":diamonds:"
                            board[y][x+3]=":diamonds:"
                        cprint("[Log] ganador", 'yellow')
                        winner=otherPlayer
                        winningComment = f"{otherPlayer} conectado 4 en una fila horizontal"
                        break
                if(winner!=""):
                    break
            #Vertical
            for y in range(height-3):
                for x in range(width):
                    if(board[y][x]==board[y+1][x] and board[y][x]==board[y+2][x] and board[y][x]==board[y+3][x] and board[y][x]!=s):
                        if(board[y][x]==p1):
                            board[y][x] = ':large_blue_diamond:'
                            board[y+1][x] = ':large_blue_diamond:'
                            board[y+2][x] = ':large_blue_diamond:'
                            board[y+3][x] = ':large_blue_diamond:'
                        elif(board[y][x]==p2):
                            board[y][x]=":diamonds:"
                            board[y+1][x]=":diamonds:"
                            board[y+2][x]=":diamonds:"
                            board[y+3][x]=":diamonds:"
                        winner = otherPlayer
                        winningComment = f"{otherPlayer} conectado 4 en una fila vertical"
                        break
                if(winner!=""):
                    break      
            # diagonal \
            for y in range(height-3):
                for x in range(width-3):
                    if(board[y][x]==board[y+1][x+1] and board[y][x]==board[y+2][x+2] and board[y][x]==board[y+3][x+3] and board[y][x]!=s):
                        if(board[y][x]==p1):
                            board[y][x] = ':large_blue_diamond:'
                            board[y+1][x+1] = ':large_blue_diamond:'
                            board[y+2][x+2] = ':large_blue_diamond:'
                            board[y+3][x+3] = ':large_blue_diamond:'
                        elif(board[y][x]==p2):
                            board[y][x]=":diamonds:"
                            board[y+1][x+1]=":diamonds:"
                            board[y+2][x+2]=":diamonds:"
                            board[y+3][x+3]=":diamonds:"
                        winner = otherPlayer
                        winningComment = f"{otherPlayer} conectado 4 en una \ diagonal"
                        break
                if(winner!=""):
                    break    
            # diagonal /
            for y in range(height-3):
                for x in range(3,width):
                    if(board[y][x]==board[y+1][x-1] and board[y][x]==board[y+2][x-2] and board[y][x]==board[y+3][x-3] and board[y][x]!=s):
                        if(board[y][x]==p1):
                            board[y][x] = ':large_blue_diamond:'
                            board[y+1][x-1] = ':large_blue_diamond:'
                            board[y+2][x-2] = ':large_blue_diamond:'
                            board[y+3][x-3] = ':large_blue_diamond:'
                        elif(board[y][x]==p2):
                            board[y][x]=":diamonds:"
                            board[y+1][x-1]=":diamonds:"
                            board[y+2][x-2]=":diamonds:"
                            board[y+3][x-3]=":diamonds:"
                        winner = otherPlayer
                        winningComment = f"{otherPlayer} conectado 4 en una / diagonal"
                        break
                if(winner!=""):
                    break    
            if(winner!=""):
                break
            ################################
            em = discord.Embed()
            em.title = f'Conecta 4'
            em.description = f"{getDisplay()}"
            em.colour = color
            em.add_field(name=f"Turno {turns}: Turno de {currentPlayer}", value=f"Ingrese un valor de 1-{width}. Tienes 30 segundos para hacer una elección", inline=True)
            await boardMessage.edit(embed=em)
            gotValidInput = False
            badInput = 0
            while not gotValidInput:
                try:
                    msg = await self.bot.wait_for('message',check=lambda message: message.author.name == currentPlayer, timeout=30)
                    await ctx.channel.delete_messages(await self.getMessages(ctx,1))
                    slot = int(msg.content)

                    if(msg.content=='rechazar'):
                        em = discord.Embed()
                        if(player1==player2):
                            em.title = f"{player2} se desafiaron a un juego de Connecta 4 (Wow estas solo)"
                        else:
                            em.title = f'{player2} a desafiado {player1} a un juego de Connecta 4'
                        em.description = f"{getDisplay()}"
                        em.colour = color
                        em.add_field(name=f"{player1}", value="Desafío rechazado", inline=False)
                        await boardMessage.edit(embed=em)
                        return

                    if(slot<1 or slot>width):
                        raise ValueError
                    for y in range(height-1,-1,-1):
                        if(board[y][slot-1]==s):
                            if(currentPlayerId == 1):
                                board[y][slot-1] = p1
                                break;
                            else:
                                board[y][slot-1] = p2
                                break;
                        elif(y==0): # Si la columna esta llena
                            raise ValueError
                    # Cambiar de personaje
                    if(currentPlayerId == 1):
                        currentPlayer = player2
                        otherPlayer = player1
                        currentPlayerId = 2
                    elif(currentPlayerId == 2):
                        currentPlayer = player1
                        otherPlayer = player2
                        currentPlayerId = 1
                    gotValidInput=True
                    turns+=1
                    break
                except asyncio.exceptions.TimeoutError:
                    winner=otherPlayer
                    winningComment=f"{currentPlayer} tomó demasiado tiempo"
                    gameLoop = False
                    break
                except ValueError:
                    em = discord.Embed()
                    em.title = f'Connecta 4'
                    em.description = f"{getDisplay()}"
                    em.colour = color
                    em.add_field(name=f"Turno {turns}: {currentPlayer}", value=f"Ingrese un número válido entre 1-{width}", inline=False)
                    await boardMessage.edit(embed=em)
                    badInput+=1
                if(badInput==3):
                    winner=otherPlayer
                    winningComment=f"{currentPlayer} tenía demasiadas entradas incorrectas"
                    gameLoop = False
                    break
        if(winner==None):
            em = discord.Embed()
            em.title = f'Conecta 4 - Empate, sin ganadores'
            em.description = f"{getDisplay()}"
            em.colour = color
            await boardMessage.edit(embed=em)
        elif(winner==player1):
            em = discord.Embed()
            em.title = f'Conecta 4 - {player1} gana!'
            em.description = f"{getDisplay()}"
            em.add_field(name="Razon:", value=f"{winningComment}", inline=False)
            if(player1==player2):
                em.add_field(name="Tambien:", value=f"A ganado contra si mismo", inline=False)
            em.colour = color
            await boardMessage.edit(embed=em)
        elif(winner==player2):
            em = discord.Embed()
            em.title = f'Conecta 4 - {player2} gana!'
            em.description = f"{getDisplay()}"
            em.add_field(name="Reason:", value=f"{winningComment}", inline=False)
            if(player1==player2):
                em.add_field(name="Tambien:", value=f"A ganado contra si mismo", inline=False)
            em.colour = color
            await boardMessage.edit(embed=em)




    async def getMessages(self, ctx: commands.Context,number: int=1):
        if(number==0):
            return([])
        toDelete = []
        async for x in ctx.channel.history(limit = number):
            toDelete.append(x)
        return(toDelete)


    @commands.command(description="Es como una ruleta Russa (SI TE TOCA PISTOLA SERAS EXPULSADO)")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roulette(self, ctx):
        responses = [
            ':gun:', ':safety_vest:', ':safety_vest:',
            ':safety_vest:', ':safety_vest:', ':safety_vest:'
        ]
        response = random.choice(responses)
        if response == ':gun:':
            try:
                await ctx.author.kick(reason='Ruleta')
            except Exception as e:
                await ctx.send(f'**`ERROR:`** { type(e).__name__ } - { e }')
            else:
                await ctx.send(f'{response}! {ctx.author.display_name} Tiene mala suerte')
        else:
            await ctx.send(f'{response}! {ctx.author.display_name} Esta bien... por ahora')


    @commands.command(description="Questionario de matematicas")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def mathquiz(self, ctx):
        arrayId, num1, num2, symArray = random.randint(0, 4), random.randint(1, 100), random.randint(1, 100), ['+', '-', 'x', ':', '^']
        ansArray = [num1+num2, num1-num2, num1*num2, num1/num2, num1**num2]
        sym = symArray[arrayId]
        msg = await ctx.send(embed=discord.Embed(title="Pregunta de mates (15 segundos)", description=f"{str(num1)} {str(sym)} {str(num2)} = ???", colour=color))
        def is_correct(m):
            return m.author == ctx.message.author
        answer = round(ansArray[arrayId])
        try:
            trying = await self.bot.wait_for("message", check=is_correct, timeout=15.0)
        except asyncio.TimeoutError:
            return await msg.edit(embed=discord.Embed(title="Se acavo el tiempo", desciprion="Has tardado mas de `15 segundos` a la proxima intenta responder mas rapido\n\nLa respuesta era {}".format(answer),colour=color))
        if str(trying.content)==str(answer):
            await msg.edit(embed=discord.Embed(title="¡Muy bien!", description=f"Esta correcto.\n Si quieres jugar a otra cosa como un trivia no ter olvides de poner `{ctx.prefix}help fun`", colour=color))
            user = ctx.author
            diamantes_dados = random.randint(10, 30)
            with open("mainbank.json", "r") as f:
                users = json.load(f)
            users[str(user.id)]["wallet"] += diamantes_dados
            with open("mainbank.json", "w") as f:
                json.dump(users, f)            
            await ctx.send(f"Y se te ha {diamantes_dados} diamantes dinero a tu cuenta")
        else:
            await msg.edit(embed=discord.Embed(title="¡Mal!", desciprion=f"La respuesta era {answer}\n\nSi quieres jugar a otra cosa como un trivia no ter olvides de poner `{ctx.prefix}help fun`",colour=color))

    def api(self, url):
        return jsonify(getapi(url).read())

    @commands.command(description="Te preguntare una pregunta que hara que te preguntes la pregunta :v")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def trivia(self, ctx):
        al = None
        try:
            wait = await ctx.send( ' | Porfavor espera... generando pregunta...')
            auth = ctx.message.author
            data = self.api('https://wiki-quiz.herokuapp.com/v1/quiz?topics=Science')
            q = random.choice(data['quiz'])
            choices = ''
            for i in range(0, len(q['options'])):
                al = list('🇦🇧🇨🇩')
                if q['answer']==q['options'][i]:
                    corr = al[i]
                choices = choices + al[i] +' '+ q['options'][i]+'\n'

            trans = Translator()
            translated_question = trans.translate(q['question'], src='en', dest='es')
            translated_choices = trans.translate(choices, src='en', dest='es')

            embed = discord.Embed(title='Trivia!', description='**'+translated_question.text+'**\n'+translated_choices.text, colour=color)
            embed.set_footer(text='Responde poniendo una reaccion! Tienes 60 segundos.')
            await wait.edit(content='', embed=embed)
            for i in range(0, len(al)):
                await wait.add_reaction(al[i])
        except Exception as e:
            await wait.edit(content="", embed=discord.Embed(title="Ups..", description=f' | Upss..!\nun error intenta usar {ctx.prefix}rate_bot <descripcion>.\n```{e}```', colour=color))
        guy = ctx.message.author
        def check(reaction, user):
            return user == guy
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await wait.add_reaction('😔')
        if str(reaction.emoji)==str(corr):
            await wait.edit(embed=discord.Embed(title="Bien hecho", description=' | <@'+str(guy.id)+'>, Felicidades! Estas correcto. :partying_face:', colour=color))
        
            user = ctx.author
            diamantes_dados = random.randint(10, 30)
            with open("mainbank.json", "r") as f:
                users = json.load(f)
            users[str(user.id)]["wallet"] += diamantes_dados
            with open("mainbank.json", "w") as f:
                json.dump(users, f)            
            await ctx.send(f"Y se te ha {diamantes_dados} diamantes dinero a tu cuenta")
     
        else:
            translated_corr = trans.translate(corr, src="en", dest='es')
            # await wait.clear_reaction()
            await wait.edit(content="", embed=discord.Embed(title="Incorrecto", description=' | <@'+str(guy.id)+'>, Estas incorrecto. La respuesta es   |   '+str(translated_corr.text)+'.', colour=color))


    @commands.command(description="Adivina el numero")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def guessnum(self, ctx):
        num = random.randint(5, 100)
        username = ctx.message.author.display_name
        user_class = ctx.message.author
        embed = discord.Embed(title='Empezando el juego!', description=f'¡ {ctx.author.mention} Tienes que adivinar un número **secreto** entre 5 y 100! \n\n¡Tienes 20 intentos y un temporizador de 20 segundos en cada intento! \n\n **B U E N A   S U E R T E**', colour=color)
        await ctx.send(embed=embed)
        gameplay = True
        attempts = 20
        while gameplay==True:
            if attempts<1:
                await ctx.send('¡El tiempo ha terminado! La respuesta es **'+str(num)+'.**')
                gameplay = False
                break
            def check_not_stranger(m):
                return m.author == user_class
            try:
                trying = await self.bot.wait_for('message', check=check_not_stranger, timeout=20.0)
            except asyncio.TimeoutError:
                await ctx.send(' | ¡No respondiste durante los siguientes 20 segundos! \nEl juego terminó.')
                gameplay = False
                break
            if trying.content.isnumeric()==False:
                await ctx.send('¡Eso no es un número!')
                attempts = int(attempts) - 1
            else:
                if int(trying.content)<num:
                    await ctx.send('Mas alto')
                    attempts = int(attempts) - 1
                if int(trying.content)>num:
                    await ctx.send('Menos')
                    attempts = int(attempts) - 1
                if int(trying.content)==num:
                    await ctx.send(embed=discord.Embed(title=' | Estas corecto!', description=f' {ctx.author.mention} **La respuesta es '+str(num)+'!**', colour=color))
            
                    user = ctx.author
                    diamantes_dados = random.randint(10, 30)
                    with open("mainbank.json", "r") as f:
                        users = json.load(f)
                    users[str(user.id)]["wallet"] += diamantes_dados
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)            
                    await ctx.send(f"Y se te ha **{diamantes_dados}** diamantes dinero a tu cuenta")
        
                    gameplay = False
                    break

    @commands.command(aliases=['guessav','avatarguess','avguess','avatargame','avgame'], description="Advivina el avatar (DEVE HAVER ALMENOS 5 MIEMBRO EN EL SERVIDOR)")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def guessavatar(self, ctx):
        if len(ctx.message.guild.members)>500:
            await ctx.send('Lo sentimos, para proteger la privacidad de algunas personas, este comando no está disponible para servidores grandes. (más de 500 miembros)')
        else:
            wait = await ctx.send(' | Espere... generando una pregunta... \nEste proceso puede tardar más si su servidor tiene más miembros.')
            avatarAll, nameAll = [], []
            for ppl in ctx.guild.members:
                if ctx.guild.get_member(int(ppl.id)).status.name!='offline':
                    avatarAll.append(str(ppl.avatar_url).replace('webp', 'png'))
                    nameAll.append(ppl.display_name)
            if len(avatarAll)<=4:
                await ctx.send(' | ¡Necesitas mas miembros online! :x:')
            else:
                numCorrect = random.randint(0, len(avatarAll)-1)
                corr_avatar, corr_name = avatarAll[numCorrect], nameAll[numCorrect]
                nameAll.remove(corr_name)
                wrongArr = []
                for i in range(0, 3):
                    wrongArr.append(random.choice(nameAll))
                abcs, emots = list('🇦🇧🇨🇩'), list('🇦🇧🇨🇩')
                randomInt = random.randint(0, 3)
                corr_order = random.choice(abcs[randomInt])
                abcs[randomInt] = '0'
                question, chooseCount = '', 0
                for assign in abcs:
                    if assign!='0':
                        question += '**'+ str(assign) + '.** '+str(wrongArr[chooseCount])+ '\n'
                        chooseCount += 1
                    else:
                        question += '**'+ str(corr_order) + '.** '+str(corr_name)+ '\n'
                embed = discord.Embed(title='¿A qué pertenece el avatar de abajo?', description=':eyes: ¡Haz clic en las reacciones! **Tienes 20 segundos.**\n\n'+str(question), colour=color)
                embed.set_footer(text='Por razones de privacidad, las personas que se muestran arriba son usuarios en línea..')
                embed.set_image(url=corr_avatar)
                main = await ctx.send(embed=embed)
                await wait.delete()
                for i in emots: await main.add_reaction(i)
                def is_correct(reaction, user):
                    return user == ctx.message.author
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', check=is_correct, timeout=20.0)
                except asyncio.TimeoutError:
                    return await main.edit(content=':pensive: ¿Ninguno? Bien entonces, la respuesta es: '+str(corr_order)+'. '+str(corr_name), embed=None)
                if str(reaction.emoji)==str(corr_order):
                    diamantes_dados = random.randint(10, 30)
                    await main.edit(content="", embed=discord.Embed(title="¡Correcto!", description=' | <@'+str(ctx.message.author.id)+f'>, Estas correcto! :tada:\n\nY se te ha añadido **{diamantes_dados}** diamantes a tu cuenta', colour=color))
                    user = ctx.author
                    with open("mainbank.json", "r") as f:
                        users = json.load(f)
                    users[str(user.id)]["wallet"] += diamantes_dados
                    with open("mainbank.json", "w") as f:
                        json.dump(users, f)     
                else:
                    await main.edit(content="", embed=discord.Embed(title="¡Incorrecto!", description=' | <@'+str(ctx.message.author.id)+'>, Incorrecto. La respuesta era '+str(corr_order)+'. '+str(corr_name), colour=color))




    def jsonisp(self, url):
        return requests.get(url).json()

    @commands.command(description="¿Saves sobre geografia?")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def geoquiz(self, ctx):
        wait = await ctx.send(' | Porfavor espera... se te esta generando el test...')
        data, topic = self.jsonisp("https://restcountries.eu/rest/v2/"), random.choice(['capital', 'region', 'subregion', 'population', 'demonym', 'nativeName'])
        chosen_nation_num = random.randint(0, len(data))
        chosen_nation, wrongs = data[chosen_nation_num], []
        data.remove(data[chosen_nation_num])
        correct = str(chosen_nation[topic])
        for i in range(0, 4):
            integer = random.randint(0, len(data))
            wrongs.append(str(data[integer][str(topic)]))
            data.remove(data[integer])
        emot, static_emot, corr_order_num = list('🇦🇧🇨🇩'), list('🇦🇧🇨🇩'), random.randint(0, 3)
        corr_order = emot[corr_order_num]
        emot[corr_order_num], question, guy = '0', '', ctx.author
        for emote in emot:
            if emote!='0':
                added = random.choice(wrongs)
                question += emote + ' ' + added + '\n'
                wrongs.remove(added)
            else:
                question += corr_order + ' ' + correct + '\n'
        trans = Translator()
        translated_topic = trans.translate(topic, src='en', dest='es')
        translated_nation = trans.translate(chosen_nation['name'], src='en', dest='es')
        translated_question = trans.translate(question, src='en', dest='es')
        translated_corr_order = trans.translate(corr_order, src='en', dest='es')

        embed = discord.Embed(title='Test de geografia: '+str(translated_topic.text), description=':nerd: Haz click en la reaccion! **Tienes 20 segundos.**\n\nQue '+str(translated_topic.text)+' pertenece a '+str(translated_nation.text)+'?\n\n'+str(translated_question.text), colour=color)
        await wait.edit(content='', embed=embed)
        for i in range(0, len(static_emot)):
            await wait.add_reaction(static_emot[i])
        def check(reaction, user):
            return user == guy
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await wait.add_reaction('😔')
        if str(reaction.emoji)==str(corr_order):
            await wait.edit(content='', embed=discord.Embed(title="¡Correcto!", description=' | <@'+str(guy.id)+'>, felizidades! Estas correcto. :partying_face:\n\nY se te han añadido diamantes a tu cuenta', colour=color))
            diamantes_dados = random.randint(10, 30)
            user = ctx.author
            with open("mainbank.json", "r") as f:
                users = json.load(f)
            users[str(user.id)]["wallet"] += diamantes_dados
            with open("mainbank.json", "w") as f:
                json.dump(users, f)             
        else:
            await wait.edit(content='', embed=discord.Embed(title="¡Incorrecto!", description=' | <@'+str(guy.id)+f'>, Estas **incorrecto**. La respuesta era {translated_corr_order.text}', colour=color))



    @commands.command(description="DESACTIVA LA BOMBA CORRE")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bomb(self, ctx):
        def embedType(a):
            if a==1: 
                return discord.Embed(title='¡La bomba ha explotadao!', description='Has perdido!', colour=color)
            elif a==2: 
                return discord.Embed(title='¡La bomba ha sido desarmada!', description=f'¡Felicidades {ctx.author.mention} has desactivado la bomba! :grinning:', colour=color)
        embed = discord.Embed(title='¡DESACTIVA LA BOMBA!', description='**¡Corta el cable correcto! \n¡La bomba explotará en 15 segundos!**', colour=color)
        main = await ctx.send(embed=embed)
        buttons = ['🔴', '🟡', '🔵', '🟢']
        for i in range(0, len(buttons)):
            await main.add_reaction(buttons[i])
        correct = random.choice(buttons)
        def check(reaction, user):
            return user == ctx.author
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await main.edit(content='', embed=embedType(1))
        if str(reaction.emoji)!=correct:
            await main.edit(content='', embed=embedType(1))
        else:
            await main.edit(content='', embed=embedType(2))
            diamantes_dados = random.randint(10, 30)
            user = ctx.author
            with open("mainbank.json", "r") as f:
                users = json.load(f)
            users[str(user.id)]["wallet"] += diamantes_dados
            with open("mainbank.json", "w") as f:
                json.dump(users, f)    
            await ctx.send(f"Se te an añadido **{diamantes_dados}** diamantes")





    @commands.command(description="Un busca minas (NO VALE HACER TRAMPAS)")
    async def minesweeper(self, ctx, columns = None, rows = None, bombs = None):
        if columns is None or rows is None and bombs is None:
            if columns is not None or rows is not None or bombs is not None:
                await ctx.send('That is nQue no está formateado correctamente o no se usaron enteros positivos válidosot formatted properly or valid positive integers weren\'t used, ',
                                f'el formato correcto es: \n` {ctx.prefix}buscaminas <columnas> <fileras> <bombas>`\n\n',
                                'No puedes darme nada por columnas, filas y bombas aleatorias.')
                return
            else:
                # Da un rango aleatorio de columnas y filas de 4 a 13 si no se dan argumentos
                # La cantidad de bombas depende de un rango aleatorio de 5 a esta fórmula:
                # ((columnas * filas) - 1) / 2.5
                # Esto es para asegurarse de que los porcentajes de bombas en un tablero aleatorio dado no sean demasiado altos
                columns = random.randint(4,13)
                rows = random.randint(4,13)
                bombs = columns * rows - 1
                bombs = bombs / 2.5
                bombs = round(random.randint(5, round(bombs)))
        try:
            columns = int(columns)
            rows = int(rows)
            bombs = int(bombs)
        except ValueError:
            await ctx.send('That is nQue no está formateado correctamente o no se usaron enteros positivos válidosot formatted properly or valid positive integers weren\'t used, ',
                            f'el formato correcto es: \n` {ctx.prefix}buscaminas <columnas> <fileras> <bombas>`\n\n',
                            'No puedes darme nada por columnas, filas y bombas aleatorias.')
            return
        if columns > 13 or rows > 13:
            await ctx.send('El límite para las columnas y filas es 13 debido a los límites de la discord...')
            return
        if columns < 1 or rows < 1 or bombs < 1:
            await ctx.send('Los números proporcionados no pueden ser cero o negativos...')
            return
        if bombs + 1 > columns * rows:
            await ctx.send(':boom:  **BOOM**, tienes más bombas que espacios en la cuadrícula o intentaste hacer que todos los espacios fueran bombas!')
            return
        
        
        grid = [[0 for num in range (columns)] for num in range(rows)]


        loop_count = 0
        while loop_count < bombs:
            x = random.randint(0, columns - 1)
            y = random.randint(0, rows - 1)

            if grid[y][x] == 0:
                grid[y][x] = 'B'
                loop_count = loop_count + 1

            if grid[y][x] == 'B':
                pass


        pos_x = 0
        pos_y = 0
        while pos_x * pos_y < columns * rows and pos_y < rows:

            adj_sum = 0

            for (adj_y, adj_x) in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]:
               
                try:
                    if grid[adj_y + pos_y][adj_x + pos_x] == 'B' and adj_y + pos_y > -1 and adj_x + pos_x > -1:

                        adj_sum = adj_sum + 1
                except Exception as error:
                    pass


            if grid[pos_y][pos_x] != 'B':
                grid[pos_y][pos_x] = adj_sum


            if pos_x == columns - 1:
                pos_x = 0
                pos_y = pos_y + 1
            else:
                pos_x = pos_x + 1


        string_builder = []
        for the_rows in grid:
            string_builder.append(''.join(map(str, the_rows)))
        string_builder = '\n'.join(string_builder)

        string_builder = string_builder.replace('0', '||:zero:||')
        string_builder = string_builder.replace('1', '||:one:||')
        string_builder = string_builder.replace('2', '||:two:||')
        string_builder = string_builder.replace('3', '||:three:||')
        string_builder = string_builder.replace('4', '||:four:||')
        string_builder = string_builder.replace('5', '||:five:||')
        string_builder = string_builder.replace('6', '||:six:||')
        string_builder = string_builder.replace('7', '||:seven:||')
        string_builder = string_builder.replace('8', '||:eight:||')
        final = string_builder.replace('B', '||:bomb:||')

        percentage = columns * rows
        percentage = bombs / percentage
        percentage = 100 * percentage
        percentage = round(percentage, 2)

        embed = discord.Embed(title='\U0001F642 Buscaminas \U0001F635', colour=color)
        embed.add_field(name="Tablero", value=f"\U0000FEFF\n{final}", inline=False)
        embed.add_field(name='Columnas:', value=columns, inline=True)
        embed.add_field(name='Filas:', value=rows, inline=True)
        embed.add_field(name='\U0001F4A3 Cuentas:', value=bombs, inline=True)
        embed.add_field(name='\U0001F4A3 Porciento:', value=f'{percentage}%', inline=True)
        embed.add_field(name='Espacios totales:', value=columns * rows, inline=True)
        embed.add_field(name='Propuesto por:', value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Games(bot))