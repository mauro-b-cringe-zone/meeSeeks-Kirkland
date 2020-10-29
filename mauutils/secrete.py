from dotenv import load_dotenv
load_dotenv(verbose=True)

from os import environ as env

TOKEN = env['TOKEN']
WEATHER_KEY = env['WEATHER_KEY']
# LINK PARA EL BOT ES: https://discord.com/oauth2/authorize?client_id=730124969132163093&permissions=8&scope=bot
# SERVIDOR https://discord.gg/4gfUZtB
color = int(env["COLOR"]) 
color_error = 0xe71818


