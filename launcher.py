from maubot import bot, main
from mauutils.secrete import TOKEN
import traceback, sys
from termcolor import cprint
import os       
from tqdm import tqdm
from time import sleep

"""Para actualizar los requirements `pip freeze > requirements.txt`"""

if __name__ == "__main__":
    try:
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/economy'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.economy.{filename[:-3]}')
                    cprint(str("[Cog] " + 'cogs.economy.'+filename[:-3]+' ...Hecho'), 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/eventos'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.eventos.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.eventos.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/fun'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.fun.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.fun.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/fun/social'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.fun.social.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.fun.social.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/fun/http_cmds'):
            if filename.endswith('.py') and filename.startswith("cmd_"):
                    bot.load_extension(f'cogs.fun.http_cmds.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.fun.http_cmds.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/imgs'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.imgs.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.imgs.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/general'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.general.{filename[:-3]}')
                cprint("[Cog] " + 'cogs.general.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/lang'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.lang.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.lang.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/moderacion'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.moderacion.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.moderacion.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/musica'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.musica.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.musica.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/spotify'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.spotify.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.spotify.'+filename[:-3]+' ...Hecho', 'green')
        for filename in os.listdir('D:/work/DISCORD-BOT/maubot/cogs/tags'):
            if filename.endswith('.py'):
                    bot.load_extension(f'cogs.tags.{filename[:-3]}')
                    cprint("[Cog] " + 'cogs.tags.'+filename[:-3]+' ...Hecho', 'green')
        bot.load_extension(f'help.help')
        cprint("[Help] " + 'help.help ...Hecho', 'yellow')
    except Exception as e:
        cprint(str(f'[Log] Se a fallado al cargar todas las extensiones cogs.+{filename[:-3]}.', file=sys.stderr), 'red')
        traceback.print_exc()

try:
    cprint(f"\n\nTOKEN:  {TOKEN}", 'yellow')
    bot.run(TOKEN)
except Exception as e:
    cprint(f"[Log] Error en el login: {e}", 'red')