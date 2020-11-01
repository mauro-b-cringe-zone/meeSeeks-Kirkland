# Maubot

Maubot | El mejor bot de la historia. Maubot es un robot con multiples funciones de todo y con una gran variedad de comandos.
Maubot tambien tiene un [compilador](http://maubot.mooo.com/maucompilador) y aparte de eso es un bot maravilloso

![GitHub last commit](https://img.shields.io/github/last-commit/maubg-debug/maubot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues-raw/maubg-debug/maubot?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/maubg-debug/maubot?style=for-the-badge)  

# Maubot | El mejor bot de la historia

## Autor
[¡Miralo!](AUTOR.md)

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
Maubot esta bajo la licencia de [GNU](./LICENSE.md)
