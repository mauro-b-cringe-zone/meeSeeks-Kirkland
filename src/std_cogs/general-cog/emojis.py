import discord
import requests
import io
import re
from discord.ext import commands

from os import environ as env

color = int(env["COLOR"])

class Emoji(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def find_emoji(self, msg):
        msg = re.sub("<a?:(.+):([0-9]+)>", "\\2", msg)
        color_modifiers = ["1f3fb", "1f3fc", "1f3fd", "1f44c", "1f3fe", "1f3ff"]
        
        name = None

        for guild in self.bot.guilds:
            for emoji in guild.emojis:
                if msg.strip().lower() in emoji.name.lower():
                    name = emoji.name + (".gif" if emoji.animated else ".png")
                    url = emoji.url
                    id = emoji.id
                    guild_name = guild.name
                if msg.strip() in (str(emoji.id), emoji.name):
                    name = emoji.name + (".gif" if emoji.animated else ".png")
                    url = emoji.url
                    return name, url, emoji.id, guild.name
        if name:
            return name, url, id, guild_name

        codepoint_regex = re.compile('([\d#])?\\\\[xuU]0*([a-f\d]*)')
        unicode_raw = msg.encode('unicode-escape').decode('ascii')
        codepoints = codepoint_regex.findall(unicode_raw)
        if codepoints == []:
            return "", "", "", ""

        if len(codepoints) > 1 and codepoints[1][1] in color_modifiers:
            codepoints.pop(1)

        if codepoints[0][0] == '#':
            emoji_code = '23-20e3'
        elif codepoints[0][0] == '':
            codepoints = [x[1] for x in codepoints]
            emoji_code = '-'.join(codepoints)
        else:
            emoji_code = "3{}-{}".format(codepoints[0][0], codepoints[0][1])
        url = "https://raw.githubusercontent.com/astronautlevel2/twemoji/gh-pages/128x128/{}.png".format(emoji_code)
        name = "emoji.png"
        return name, url, "N/A", "Official"

    @commands.command(pass_context=True, aliases=['emote'], invoke_without_command=True, description="Mira un emoji como una imagen", usage="[s (Literalmente pones s)] <emoji>")
    async def emoji(self, ctx, *, msg):
        emojis = msg.split()
        if msg.startswith('s '):
            emojis = emojis[1:]
            get_guild = True
        else:
            get_guild = False

        if len(emojis) > 5:
            return await ctx.send("Maximo siete emojis.")

        images = []
        for emoji in emojis:
            name, url, id, guild = self.find_emoji(emoji)
            if url == "":
                await ctx.send("Could not find {}. Skipping.".format(emoji))
                continue
            response = requests.get(url, stream=True)
            if response.status_code == 404:
                await ctx.send("El emoji {} no lo encontre. Abre un error en <https://github.com/maubg-debug/maubot/issues> con el nombre no existente del emoji".format(emoji))
                continue

            img = io.BytesIO()
            for block in response.iter_content(1024):
                if not block:
                    break
                img.write(block)
            img.seek(0)
            images.append((guild, str(id), url, discord.File(img, name)))

        for (guild, id, url, file) in images:
            if ctx.channel.permissions_for(ctx.author).attach_files:
                if get_guild:
                    await ctx.send(content='**ID:** {}\n**Servidor:** {}'.format(id, guild), file=file)
                else:
                    await ctx.send(embed=discord.Embed(title=f"toma tu emoji", url=url, color=color, description=f"{ctx.author.mention}, se te ha creado un emoji, por si no lo ves puedes darle al titulo o **[aqui]({url})**").set_image(url=url))
            else:
                if get_guild:
                    await ctx.send('**ID:** {}\n**Servidor:** {}\n**URL: {}**'.format(id, guild, url))
                else:
                    await ctx.send(url)
            file.close()

def setup(bot):
    bot.add_cog(Emoji(bot))