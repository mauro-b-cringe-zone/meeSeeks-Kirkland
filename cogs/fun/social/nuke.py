import discord
from discord.ext import commands
from os import environ as env
color = int(env["COLOR"])

class Nuke(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="TE ODIOO @usuario")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nuke(self, ctx, target: discord.Member):
        await ctx.send(embed=discord.Embed(description=f"**{ctx.author.name}** a lanzado una bomba nuclear contra **{target.name}**  💔",
                                    colour=color)
                        .set_image(url="https://db.manx7.net/assets/m7/nukes/2.gif"))



def setup(bot):
    bot.add_cog(Nuke(bot))