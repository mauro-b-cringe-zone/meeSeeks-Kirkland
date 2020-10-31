# Maubot

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
``` apt-get install libav-tools ffmpeg ```

- [arch (manjaro,...)](https://www.archlinux.org/packages/extra/x86_64/ffmpeg/)  
``` pacman -S ffmpeg ```

- [centOS (yum)](https://linuxize.com/post/how-to-install-ffmpeg-on-centos-8/)  
(haga clic en el enlace para ver la documentación)

- [rpm (everything else)](https://rpmfind.net/linux/rpm2html/search.php?query=ffmpeg)  
(haga clic en el enlace para ver la página de descarga)

#### 3. Editar el entorno
a) Copie el archivo `.env.example` y cámbiele el nombre a `.env`
b) Completa los valores

#### 3. Correr el bot
```
python ./src/main.py
```
