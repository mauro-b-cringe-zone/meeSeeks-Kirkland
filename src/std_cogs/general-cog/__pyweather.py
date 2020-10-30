from discord import Embed, Color
from discord.ext import commands
from discord.utils import get

from requests import get as rget
from datetime import datetime, timedelta

from utils.Environment import env

color = int(env.get["COLOR"])
WEATHER_KEY = env.get("WEATHER_KEY")

from googletrans import Translator

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_cast(city, forecast=False):
        if forecast:
            return rget(f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&APPID={WEATHER_KEY}").json()
        data  = rget(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={WEATHER_KEY}").json()
        cleared_data = {
            'City': data['name'],
            'Time': (datetime.utcfromtimestamp(data['dt']) + timedelta(hours=2)).strftime('%H:%M:%S'),
            'Weather': f"{data['weather'][0]['main']} - {data['weather'][0]['description']}",
            'Temperature': f"{data['main']['temp']}°C",
            'Feels like': f"{data['main']['feels_like']}°C",
            'Min temperature': f"{data['main']['temp_min']}°C",
            'Max temperature': f"{data['main']['temp_max']}°C",
            'Humidity': f"{data['main']['humidity']}%",
            'Pressure': f"{data['main']['pressure']} Pa",
            'Clouds': f"{data['clouds']['all']}%",
            'Wind': f"{data['wind']['speed']} km/h",
            'Sunset': (datetime.utcfromtimestamp(data['sys']['sunset']) + timedelta(hours=2)).strftime('%H:%M:%S'),
            'Sunrise': (datetime.utcfromtimestamp(data['sys']['sunrise']) + timedelta(hours=2)).strftime('%H:%M:%S'),
        }
        return cleared_data

    @commands.command(description="Busca el tiempo en tu cioudad", usage="<ciudad>")
    async def weather(self, ctx,  *, city):
        data = Weather.get_cast(city)
        embed = Embed(title=f":white_sun_small_cloud: Clima en {data['City']}:", colour=color)
        for key, value in data.items():
            translated_key = Translator().translate(key, src='en', dest='es')
            embed.add_field(name=translated_key.text, value=value)

        data = Weather.get_cast(city, True)
        days = {entry['dt_txt'][:10]: [] for entry in data['list']}
        for index, entry in enumerate(data['list']):
            days[entry['dt_txt'][:10]].append(f"{entry['dt_txt'][11:-3]} → {entry['weather'][0]['main']} - {entry['main']['temp']}°C\n")

        msg = await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Weather(bot))
