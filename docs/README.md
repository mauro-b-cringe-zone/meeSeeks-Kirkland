# Como instalarlo

## Como empezar

#### 0. Instalar python 3.6.0 - 3.9.x
Las versiones inferiores o superiores no son compatibles oficialmente

#### 1. Crearse un enviroment
```
C\> python3 -m venv env
C\> windows (.\env\Scripts\activate) | linux (source .\env\bin\activate)
```

#### 2. Instalar dependencias de Python (Con el enviroment ya activado)
```
pip install -r requirements.txt
```

#### 3. Editar el entorno
a) Copie el archivo `.env.example` y cámbiele el nombre a `.env`
b) Completa los valores

---
#### 5. archivo.env
Todo esta en el [.example.env](https://github.com/maubg-debug/maubot/blob/main/.example.env)
```txt
# https://discord.com/developers/applications
TOKEN = 

# https://openweathermap.org/api
WEATHER_KEY =

# https://github.com/maubg-debug/maubot/blob/main/docs/README.md#4-archivoenv 
COMP_KEY =

# https://github.com/maubg-debug/maubot/blob/main/docs/README.md#instrucciones-para-el-color-del-env 
COLOR = 

# Esto ya esta rellenado
USER_STATISTICS_THROTTLE_DURATION=10
USER_STATISTICS_INCREMENT=5

# True|False
DEBUG=

# https://brainshop.ai/
CHAT_AI_BOT = 

# Las instrucciones se pueden ver aqui https://github.com/maubg-debug/maubot/tree/main/data#instalacion-de-data
JSON_DIR=Tu direccion para los json
DB_DIR=Tu direccion para la DB

# Los webhooks del servidor
# -> https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
WEBHOOK_URL_ENTRADA=
WEBHOOK_URL_SALIDA=
WEBHOOK_URL_ERRORES=
```

#### 4. Correr el bot
```shell
python ./src/main.py
```

```
#### Instrucciones para el color del .env
```shell
pip install envparse <- O -> pip install git+https://github.com/rconradharris/envparse.git
```
---
Luego en la consola de python pondreis
```python
C:\> python
>>>
>>> print(int(0xffffff)) # Enved de "0xffffff" poner buestro color
16777215
>>> # Si no cogeremos el "COLOR" del .env como un str() y lo queremos en int() para el embed
```
