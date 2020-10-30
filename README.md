![hellocoding bot img](docs/images/logo-bold-discord-bot.svg)

![GitHub last commit](https://img.shields.io/github/last-commit/hellocodingDE/hellocoding-bot?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues-raw/hellocodingDE/hellocoding-bot?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/hellocodingDE/hellocoding-bot?style=for-the-badge)  

# HelloCoding Discord Bot - Community Edition

## Maintainers
[Have a look!](MAINTAINERS.md)

## Getting started

#### 0. Install Python 3.6.0 - 3.9.x
Versions below or above are not official supported

#### 1. Install python dependencies
```
pip install -r requirements.txt
```

#### 2. Install additional dependencies
- [ffmpeg binary (windows)](https://ffmpeg.org/download.html) (for voicechats)  
(click on link to see download page)

- [macOS (homebrew)](https://formulae.brew.sh/formula/ffmpeg#default)  
```brew install wget```

- [debian (ubuntu, mint, deepin, zorin, pop!_os,...)](https://wiki.debian.org/ffmpeg)  
``` apt-get install libav-tools ffmpeg ```

- [arch (manjaro,...)](https://www.archlinux.org/packages/extra/x86_64/ffmpeg/)  
``` pacman -S ffmpeg ```

- [centOS (yum)](https://linuxize.com/post/how-to-install-ffmpeg-on-centos-8/)  
(click on link to see documentation)

- [rpm (everything else)](https://rpmfind.net/linux/rpm2html/search.php?query=ffmpeg)  
(click on link to see download page)

#### 3. Edit environment
a) Copy the `.env.example` file and rename it to `.env`
b) Fill in the values

#### 3. Run Bot
```
python ./src/main.py
```
