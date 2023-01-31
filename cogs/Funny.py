
import asyncio
import typing
import os

import discord
from discord.ext import commands
from discord import app_commands




class Funny(commands.Cog):
    def __init__(self, bot):
        self.bot : commands.Bot = bot
        self.SOURCE = ''
        #self.SOUND_LIST = ['']
        

    #TODO Change to /voice & add numerous options for the bot.
    @app_commands.command(name="voice", description="Funny haha command")
    async def voice(self, interaction : discord.Interaction, sound: typing.Literal["hue", "knock", "me", "rey", "rey_2", "rey_3", "hue_2", "hue_3"]):  #TODO Make dynamic by searching through assets rather than hard coding
        if not interaction.user.voice:
            await interaction.response.send_message('No voice channel')
            return

        if not interaction.permissions.administrator:  #Adjust perms as needed here
            await interaction.response.send_message('No permission')
            return

        
        for asset in os.listdir("assets"):
            print(f'{asset[:-4]} ||| {sound}')
            if asset[:-4] == sound:
                print(f'[SOURCE] Picked a sourece {asset}')
                self.SOURCE = f'assets/{asset}'
                break

        
        print(f'Source: {self.SOURCE}')

        channel = await interaction.user.voice.channel.connect()
        audio = discord.FFmpegPCMAudio(executable="C:\PATH_PROGRAMS/ffmpeg.exe", source=self.SOURCE) 
        channel.play(audio)    

        await interaction.response.send_message(content=":)", ephemeral=True)

        while channel.is_playing():
            await asyncio.sleep(2)

        channel.pause()

        await channel.disconnect()
        await interaction.followup.send(content="Bye!", ephemeral=True)


async def setup(bot: commands.Bot):
   await bot.add_cog(Funny(bot))