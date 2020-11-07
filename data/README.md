# Instalacion de data

## Como empezar

### Cambiar la direccion

* Create una carpeta donde tu quieras
* Mete todos los json y bases de datos que tu quieras en esa carpeta
* Ve al archivo `.env` y pon rellena el `JSON_DIR` y el `DB_DIR`

Tendria que qudar algo asi
```env
JSON_DIR=c:\maubot\jsons\
DB_DIR=c:\maubot\DB\
```

> Tiene que terminar con un `\`

Por ejemplo seria

```python
from os import environ as env

with open(env["JSON_DIR"] + "tujson.json", "r") as f:
	json = json.load(f)
    
print(json)
```

* Por eso tendria que terminar con un `\`

## Dudas
* Si tienes dudas no olvides en [contactarme](http://github.com/maubg-debug)
