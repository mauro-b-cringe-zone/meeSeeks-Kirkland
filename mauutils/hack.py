import random

def history(a):
    arr = [
        'Cómo crear un bot como Username601 sin codificación gratis',
        'Cómo evitar un bloqueo por parte del gobierno',
        'Cómo borrar el historial de navegación de mis padres',
        'Cómo conseguir más personas en mi servidor',
        'cómo hacer que mi servidor obtenga 1000 miembros en 1 minuto',
        'Cómo obtener el icono del servidor animado GRATIS SIN NITRO',
        'VPN GRATIS SIN HACK VIRUS',
        'www.'+a+'. com',
        'Cómo eludir una prohibición en discordia',
        '¿Por qué la gente me prohíbe? Solo tengo 12 años',
        'Cómo acceder a la discordia cuando tienes menos de 13 años',
        'discord.gg/'+a,
        'MINECRAFT ÚLTIMA VERSIÓN DESCARGA GRATUITA CRACK NO HACK NO ROOT',
        'Cómo hackear la discordia',
        'Xxx_EpicGamer_xxX vamos a jugar',
        'Cómo respirar',
        'Cuál es el significado de la vida',
        'Cuál es el resultado de 1/0'
        'Tutorial de trampas de bot OwO',
        'Cómo hacer trampa en Pokecord. CRÉDITOS GRATIS SIN HACK ',
        'FREE NITRO NO HACK LEGIT 2020',
        'Cómo impulsar mi servidor de forma gratuita sin hackear crack legítimo',
        'CÓMO CONSEGUIR MÁS MIEMBROS EN MI SERVIDOR PLSS ESTOY DESESPERADO',
        '¿Por qué la gente sigue saliendo de mi servidor de discordia?'
        'Cómo convertirse en un bot en discordia',
        'Vbucks gratis sin hacks'
    ]
    return random.choice(arr)

def password(a):
    arr = [
        a+'esguayy',
        a+'123456',
        'Xx _'+a+'_ xX',
        'fornitegamer123',
        'real'+a,
        'theultimate'+a,
        'último'+a,
        'mega'+a,
        '123'+a+'123',
        'CONTRASEÑA',
        'QWERTY',
        '000000',
        '111111',
        'uwuyoucanthackme',
        'Edmund1978',
        '12345',
        'PASS123',
        'DÉJAME ENTRAR',
        'XXXcoolpasswordXXX',
        'XXX'+a +'XXX',
        'DankMemerFan42069',
        'Swag69',
        'UWU69',
        '601SUCKS',
        'epicgamer123'
    ]
    return random.choice(arr)

def randomhash():
    hashh = ''
    for i in range(0, random.randint(13, 21)):
        hashh = hashh + random.choice(list('ABCDEFHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'))
    return hashh

def lastmsg(a):
    arr = [
        'únete a plspls discord.gg/'+a,
        'Amo mi vida',
        'bruh',
        'mama Mia',
        'Username601 apesta',
        'OwO',
        '¿Cuál es el apellido de obama por favor?'
        'Oye, soy gay',
        'yee',
        '¿Puedes enviarme ese clip nsfw gracias?',
        'eewww: o',
        'suscríbete a pewdiepie'
    ]
    return random.choice(arr)
def email(a):
    arr = [
        a+'esgenial',
        a+'juegaminecraft',
        'elúnico'+a,
        'nohackablegmailaccount',
        'epicgmaillink',
        a+'eslamejor',
        a+'OwO',
        'señor'+a,
        a+'juegafortnite',
        a+'votóelnombredeusuario601',
        a+'601'
    ]
    return random.choice(arr)

def hackflow(tohack):
    flow = [
        '0hack.exe -u '+str(tohack.name)+' -a',
        '0\n[hack.exe] Abriendo mensaje de hack...',
        '0\n[hack.exe] Apertura http://discord.com/hack/'+randomhash(),
        '1\n[hack.exe] USUARIO DETECTADO: '+tohack.name+'. HACKEANDO USUARIO... ',
        '1"hecho"',
        '1\n[hack.exe] RECUPERACIÓN DE LA DIRECCIÓN IP... ',
        '1"hecho". IP: 99.238.'+str(tohack.discriminator)+'.1729.10',
        '1\n[hack.exe] ACCEDER AL DISPOSITIVO DESDE DISCORD... ',
        '1"hecho".',
        '1\n[DEVICE ID:'+str(tohack.discriminator)+'] ACCESO PERMITIDO',
        '1\n[hack.exe] OPTENIENDO CAMARA... ',
        '2succeso.',
        '2\n[hack.exe] DIFUSIÓN DE CAMARA A LA WEB OSCURA... ',
        '2"hecho".',
        '1\n[hack.exe] OBTENER INFORMACIÓN DE CORREO ELECTRÓNICO... ',
        '1"hecho".',
        '4\nEMAIL: '+email(tohack.name)+'@hackeado.com\nCONTRASEÑA: "'+password(tohack.name)+'"',
        '1\n[hack.exe] DIVULGANDO INFORMACIÓN A '+randomhash()+'.onion... ',
        '1"hecho".',
        '1\n[hack.exe] GETTING SENSITIVE PERSONAL INFORMATION...',
        '4"hecho".\nULTIMO MENSAJE: "'+lastmsg(tohack.name)+'"\nÚLTIMA HISTORIA DE NAVEGACIÓN: "'+history(tohack.name)+'"\n[hack.exe] DISTRIBUCIÓN DE INFORMACIÓN AL FBI Y NSA... ',
        '3"hecho".',
        '0\n[hack.exe] HACK COMPLETADO.',
        '0\n\nC:\\Users\\Anonymous601>'
    ]
    return flow

def bin(text):
    result = " ".join(f"{ord(i):08b}" for i in text)
    return result.replace(' ', '')