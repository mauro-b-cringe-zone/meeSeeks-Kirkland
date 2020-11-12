# Como instalarlo

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
Todo esta en el [.example.env](https://github.com/maubg-debug/maubot/blob/main/.example.env)
```txt
# https://discord.com/developers/applications
TOKEN = 

# https://openweathermap.org/api
WEATHER_KEY =

# https://github.com/maubg-debug/maubot#4-archivoenv 
COMP_KEY = Visitar (https://rapidapi.com/hermanzdosilovic/api/judge0)

# https://github.com/maubg-debug/maubot#instrucciones-para-el-color-del-env 
COLOR = 

# Esto ya esta rellenado
USER_STATISTICS_THROTTLE_DURATION=10
USER_STATISTICS_INCREMENT=5

# True|False
DEBUG=

# https://www.screenshotmachine.com/
WEB_KEY =

# Las instrucciones se pueden ver aqui https://github.com/maubg-debug/maubot/tree/main/data#instalacion-de-data
JSON_DIR=Tu direccion para los json
DB_DIR=Tu direccion para la DB

# Los webhooks del servidor
# -> https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
WEBHOOK_URL_ENTRADA=
WEBHOOK_URL_SALIDA=
WEBHOOK_URL_ERRORES=
```
#### Instrucciones para el color del .env
```shell
pip install envparse <- O -> pip install git+https://github.com/rconradharris/envparse.git
```
Luego en la consola de python pondreis
```python
C:\> python
>>>
>>> print(int(0xffffff)) # Enved de "0xffffff" poner buestro color
16777215
>>> # Si no cogeremos el "COLOR" del .env como un str() y lo queremos en int() para el embed
```
