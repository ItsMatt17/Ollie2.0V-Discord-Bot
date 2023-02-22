import asyncio
import os

import discord
from discord import app_commands
from discord import ui
from discord.ext import commands

from config import VoiceFunny


class VoiceSelect(ui.Select):
    def __init__(self):
        self.SOURCE = None
        options_1 = []

        for asset in enumerate(os.listdir(VoiceFunny.assets)):
            options_1.append(discord.SelectOption(label=asset[:-4], description="An audio of a weirdo"))
        if len(options) >= 25:
            print(f"[WARNING] Assets are reaching limit, there are {len(options)} in ./assets")
        super().__init__(placeholder='Choose an audio clip to play', min_values=1, max_values=1, options=options)


    async def callback(self, interaction : discord.Interaction):
        sound = self.values[0]
        for asset in os.listdir(VoiceFunny.assets):
            if asset[:-4] == sound:
                print(f'[SOURCE] Picked a source {asset}')
                self.SOURCE = f'{VoiceFunny.assets}/{asset}'
                break

        print(f'[SOURCE]: {self.SOURCE}')

        channel = await interaction.user.voice.channel.connect()
        audio = discord.FFmpegPCMAudio(executable=VoiceFunny.executable, source=self.SOURCE)
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
        self.bot: commands.Bot = bot
        self.SOURCE = ''

    @staticmethod
    def _embed_builder() -> discord.Embed:
        # for asset in os.listdir(VoiceFunny.assets):

        embed = discord.Embed(title="Funny Voice Clips",
                              description=f"With over {len(VoiceSelect.options_1)} different clips, and Rey's flirting clips!",
                              color=discord.Color.red())
        return embed

    @app_commands.checks.cooldown(3, 10)
    @app_commands.command(name="voice", description="Funny haha command")
    async def voice(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message('No voice channel')
            return

        # TODO Fix for check if bot is already connected to channel

        if self.bot.voice_clients:
            await interaction.response.send_message("Already in a channel")
            print("In a channel")

        view = VoiceView()
        await interaction.response.send_message(embed=self._embed_builder(), view=view, ephemeral=True)
        await view.wait()


    @voice.error
    async def voice_error(self, interaction : discord.Interaction, error):
        print(f"[Error]: [Module Voice] {error}")

        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"You're on scooldown for {error.retry_after:.2f}s", ephemeral=True
            )
        elif isinstance(error, discord.ClientException):
            message = interaction.message
            if message:
                await message.delete()

async def setup(bot: commands.Bot):
   await bot.add_cog(Funny(bot))