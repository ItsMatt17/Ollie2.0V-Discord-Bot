
import asyncio
import typing
import os

import discord
from discord.ext import commands
from discord import app_commands
from discord import ui

class VoiceSelect(ui.Select):
    def __init__(self):
        
        options = []
        for asset in os.listdir("assets"):
            options.append(discord.SelectOption(label=asset[:-4], description="An audio of a weirdo"))
        
        super().__init__(placeholder='Choose an audio clip to play', min_values=1, max_values=1, options=options)

    
    async def callback(self, interaction : discord.Interaction):  
        sound =  self.values[0]
        for asset in os.listdir("assets"):
            if asset[:-4] == sound:
                print(f'[SOURCE] Picked a source {asset}')
                self.SOURCE = f'assets/{asset}'
                break

        
        print(f'[SOURCE]: {self.SOURCE}')

        channel = await interaction.user.voice.channel.connect()
        audio = discord.FFmpegPCMAudio(executable="C:\PATH_PROGRAMS/ffmpeg.exe", source=self.SOURCE) 
        channel.play(audio)    

        await interaction.response.send_message(content=":)", ephemeral=True)

        while channel.is_playing():
            await asyncio.sleep(2)

        channel.pause()

        await channel.disconnect()
        await interaction.followup.send(content="Bye!", ephemeral=True)
    

class VoiceView(ui.View):
    def __init__(self):
        super().__init__(timeout=15.0)

        self.add_item(VoiceSelect())

  
class Funny(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        self.SOURCE = ''        

    @app_commands.command(name="voice", description="Funny haha command")
    async def voice(self, interaction : discord.Interaction): 
        if not interaction.user.voice:
            await interaction.response.send_message('No voice channel')
            return

        if not interaction.permissions.administrator:  #Adjust perms as needed here
            await interaction.response.send_message('No permission')
            return

        view = VoiceView()
        msg = await interaction.response.send_message(view=view, ephemeral=True)  # Most dynamic way of coding this seems to be using views
        print(type(msg))
        await view.wait()
        print(type(msg))



async def setup(bot: commands.Bot):
   await bot.add_cog(Funny(bot))