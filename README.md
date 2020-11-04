# Maubot

Maubot | El mejor bot de la historia. Maubot es un robot con multiples funciones de todo y con una gran variedad de comandos.
Maubot tambien tiene un [compilador](http://maubot.mooo.com/maucompilador) y aparte de eso es un bot maravilloso

![GitHub last commit](https://img.shields.io/github/last-commit/maubg-debug/maubot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues-raw/maubg-debug/maubot?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/maubg-debug/maubot?style=for-the-badge)  

# Maubot | El mejor bot de la historia

<!-- ![img](https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/Maubot-banner.jpg) -->

## Autor
[¡Miralo!](https://github.com/maubg-debug/maubot/blob/main/AUTOR.md)

# ¿Qué puede hacer Maubot?
Como se muestra en la descripcion <strong>Maubot</strong> tiene una gran variedad de comandos y secciones

# Caracteristicas

## Ayuda

* El bot viene con una función `$help` que muestra la lista de todos los comandos disponibles.
* Puede escribir `!help [Cog]` para ver más información sobre cada comando.

## Prefijos
* Los prefijos de Maubot son (!, ?, m.) y uno personalizado que es $ y puedes cambiarlo poniendo `$prefix <tu prefijo>` 

## Moderacion basica

* maubot tiene uno de los sistemas de moderación más simples, sin necesidad de configurar nada. Depende completamente del sistema de permisos de Discord para garantizar si el usuario tiene permiso para castigar a alguien o no.

  * **Expulsion y Baneos(suaves)** comprueba el rol más alto del usuario que tiene un permiso requerido específico para ejecutar el comando.

  * **Mutear y Desmutear** Maubot al igual que con los comandos de expulsion y etc, Checkea si el usuario tiene permisos y el que este muteado no podra hablar en le chat

  * **Warniciones** Maubot detecta si un usuario tiene mas de 5 warniviones `$warnlist [@usuario]` para ver las warniciones

  * **Cambios en el servidor** Maubot tambien puede hacer cambios en el servidor, como eliminar mensages, crear canales, etc.


## Util y divertido

* Maubot tiene funciones de economia y de musica

* Al igual que tiene comandos de juegos, manipulacion de imagenes, etc.

# Seguro

> Maubot no podra ser hackeado ni nada por el estilo porque las llaves y todo estan super seguras
> Ademas de eso, Maubot mantendra toda tu informacion guardada o nisiquiera coger informacion

# No esta loco

* Maubot no ara nada de lo que tu no le ordenes

# Anti-Bots

* Maubot dejara el servidor si el 70% de el servidor son robots

# Extras
* Musica
  * Maubot esta implementado con un equipo de musica para que tu fiesta siga marchosa 🎉
* Niveles
  * Maubot tiene un gran sistema de niveles que te havisa cuando ayas suvido de nivel
  * Tambien tiene un comando que lo puedes usar al poner `$rank` Y te dara la info de tu nivel
* Economia
  * Maubot esta disponible con un sistema de economia con comandos como:
    * `$balance [@usuario]`, `$rob <@usuario>`, `$slots`, `$shop [pagina]`, `$buy <objeto>`, `$sell <objeto>`, ...
* Maubot tiene tambien un compilador lo podeis usar poniendo `$[lenguage]` <- O -> `$run --list` para ver los idiomas
  * Si quereis podeis usarlo desde la [web](http://maubot.mooo.com/maucompilador)
* Y MUCO MASSSSS......

# Sugerencias

* Si tienes alguna sugerencia puedes unirte a [nuestro server](https://discord.gg/4gfUZtB) <- O -> Si tienes que contarnos un bug ve a [su github](https://github.com/maubg-debug/maubot/issues/new?assignees=&labels=bug&template=reporte-de-bugs.md&title=BUG)

* Tambien puedes poner `$rate_bot <descripcion>` para darle nua reseña, `$request <descripcion>` Para alguna idea y `$report` Para reportar algun bug que tenga maubot.

# Ayuda
[![Image from Gyazo](https://i.gyazo.com/a6b79abe4009be0c06ff0c5717882f1b.gif)](https://gyazo.com/a6b79abe4009be0c06ff0c5717882f1b)

# Chats
Maubot esta equipado con unos chats integrados que se podran activar poniendo `$startchat <@usuario>` y ya estaria

# Web
* Aqui esta la [web](http://maubot.mooo.com)

# Por si quieres instalarlo

## Como empezar

#### 0. Instalar python 3.6.0 - 3.9.x
Las versiones inferiores o superiores no son compatibles oficialmente

#### 1. Instalar dependencias de Python
```
pip install -r requirements.txt
```

#### 2. Instalar dependencias adicionales
- [ffmpeg binary (windows)](https://ffmpeg.org/download.html) (para charlas de voz)  
(haga clic en el enlace para ver la página de descarga)

- [macOS (homebrew)](https://formulae.brew.sh/formula/ffmpeg#default)  
```brew install wget```

- [debian (ubuntu, mint, deepin, zorin, pop!_os,...)](https://wiki.debian.org/ffmpeg)  
```apt-get install libav-tools ffmpeg```

- [arch (manjaro,...)](https://www.archlinux.org/packages/extra/x86_64/ffmpeg/)  
```pacman -S ffmpeg```

- [centOS (yum)](https://linuxize.com/post/how-to-install-ffmpeg-on-centos-8/)  
(haga clic en el enlace para ver la documentación)

- [rpm (Todo lo demas)](https://rpmfind.net/linux/rpm2html/search.php?query=ffmpeg)  
(haga clic en el enlace para ver la página de descarga)

#### 3. Editar el entorno
a) Copie el archivo `.env.example` y cámbiele el nombre a `.env`
b) Completa los valores

#### 3. Correr el bot
```shell
python ./src/main.py
```

#### 4. archivo.env
```txt
TOKEN = El token del robot
WEATHER_KEY = https://openweathermap.org/api (LLave de la api para este bot)
COMP_KEY = Visitar (https://rapidapi.com/hermanzdosilovic/api/judge0)
COLOR = Ver Las instrucciones (https://github.com/maubg-debug/maubot#instrucciones-para-el-color-del-env)
USER_STATISTICS_THROTTLE_DURATION = 5 - Esto da igual
USER_STATISTICS_INCREMENT = 10 - Esto da igual
DEBUG = True|False
```
#### Instrucciones para el color del .env
```shell
pip install envparse <- O -> pip install git+https://github.com/rconradharris/envparse.git
```
Luego en la consola de python pondreis
```python
C:\> python
Python 3.8.1 (tags/v3.8.1:1b293b6, Dec 18 2019, 23:11:46) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> print(int(0xffffff)) # Enved de "0xffffff" poner buestro color
16777215
>>> # Si no cogeremos el "COLOR" del .env como un str() y lo queremos en int() para el embed
```

# Licencia 
Maubot esta bajo la licencia de [GNU](https://github.com/maubg-debug/maubot/blob/main/LICENSE.md)
