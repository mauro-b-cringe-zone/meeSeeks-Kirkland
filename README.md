# Maubot

Maubot | El mejor bot de la historia. Maubot es un robot con multiples funciones de todo y con una gran variedad de comandos.
Maubot tambien tiene un [compilador](http://maubot.mooo.com/maucompilador) y aparte de eso es un bot maravilloso

![GitHub last commit](https://img.shields.io/github/last-commit/maubg-debug/maubot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues-raw/maubg-debug/maubot?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/maubg-debug/maubot?style=for-the-badge)  

# Maubot | El mejor bot de la historia

![img](https://raw.githubusercontent.com/maubg-debug/maubot/main/docs/Maubot-banner.jpg)

## Autor
[¡Miralo!](https://github.com/maubg-debug/maubot/blob/main/AUTOR.md)

# ¿Qué puede hacer Maubot?
Como se muestra en la descripcion <strong>Maubot</strong> tiene una gran variedad de comandos y secciones

# Caracteristicas

## Ayuda

* El bot viene con una función `$help` que muestra la lista de todos los comandos disponibles.
* Puede escribir `!help [Cog]` para ver más información sobre cada comando.


## Set Language

* The key feature is to let individual servers to use a specific language in which the bot will respond in. This makes it that all communities get the full experience by letting everyone to understand what each response means.

* If you do not see your language in our list of available languages, this means that we do not yet have translators to support that language. Believe it or not, but we do not know every single language for you to deliver, so instead we are recruiting a team of translators to help us with this mission! If you are interested, [join our support server](https://discord.gg/sbySHxA) for more information.


## Prefijos
* Los prefijos de Maubot son (!, ?, m.) y uno personalizado que es $ y puedes cambiarlo poniendo `$prefix <tu prefijo>` 

## Moderacion basica

* maubot tiene uno de los sistemas de moderación más simples, sin necesidad de configurar nada. Depende completamente del sistema de permisos de Discord para garantizar si el usuario tiene permiso para castigar a alguien o no.

  * **Expulsion y Baneos(suaves)** comprueba el rol más alto del usuario que tiene un permiso requerido específico para ejecutar el comando.

  * **Mutear y Desmutear** Maubot al igual que con los comandos de expulsion y etc, Checkea si el usuario tiene permisos y el que este muteado no podra hablar en le chat

  * **Warniciones** Maubot detecta si un usuario tiene mas de 5 warniviones `$warnlist [@usuario]` para ver las warniciones

  * **Cambios en el servidor** Maubot tambien puede hacer cambios en el servidor, como eliminar mensages, crear canales, etc.

## Invite Lookup

* Have an invite URL and want to see what the server is about but don't want to be caught joining? You can now look up the general information about the invite and the server that it leads to.


## Useful & Fun

* Display general information about a chosen user or a current server.

* Randomize a member from the server, or within a role.


# Anti-Bot Farm

* Quote will leave any server with more than 20 members that has more than 70% of the population composed of Bots.


# Suggestions

* Have a suggestion? Join our [**Support Server**](https://discord.gg/sbySHxA) and head over to #suggestions. Follow the template to submit your own suggestion.



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
Maubot esta bajo la licencia de [GNU](https://github.com/maubg-debug/maubot/blob/main/README.md)
