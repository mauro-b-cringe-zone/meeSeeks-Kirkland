import discord
from discord.ext import commands
import json

color = 0x75aef5 

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        
def setup(bot):
    bot.add_cog(Tags(bot))