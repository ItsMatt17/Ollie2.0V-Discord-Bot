import asyncio
import os

import discord
from discord import app_commands
from discord import ui
from discord.ext import commands

from config import VoiceFunny

OPTIONS = []
test = [discord.SelectOption(label=asset[:-4], description="An audio of a weirdo") for asset in
        os.listdir(VoiceFunny.assets)]
amount_of_clips = []


class VoiceSelect(ui.Select):
    def __init__(self):
        self.SOURCE = None

        for asset in os.listdir(VoiceFunny.assets):
            # amount_of_clips.append(asset.split())
            OPTIONS.append(discord.SelectOption(label=asset[:-4], description="An audio of a weirdo"))
        if len(OPTIONS) >= 25:
            print(f"[WARNING] Assets are reaching limit, there are {len(OPTIONS)} in ./assets")
        super().__init__(placeholder='Choose an audio clip to play', min_values=1, max_values=1, options=OPTIONS)

    async def callback(self, interaction: discord.Interaction):
        VALUE_SELECTED = 0
        sound = self.values[VALUE_SELECTED]
        for asset in os.listdir(VoiceFunny.assets):
            if asset[:-4] == sound:
                print(f'[SOURCE] Picked a source {asset}')
                self.SOURCE = f'{VoiceFunny.assets}/{asset}'
                break

        print(f'[SOURCE]: {self.SOURCE}')

        channel = await interaction.user.voice.channel.connect()
        audio = discord.FFmpegPCMAudio(executable=VoiceFunny.executable, source=self.SOURCE)
        channel.play(audio)

        while channel.is_playing():
            await asyncio.sleep(2)

        channel.pause()

        await channel.disconnect()


class VoiceView(ui.View):
    def __init__(self):
        super().__init__(timeout=15.0)
        self.add_item(VoiceSelect())


class Funny(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.SOURCE = ''

    def _embed_builder(self) -> discord.Embed:
        # for asset in os.listdir(VoiceFunny.assets):

        embed = discord.Embed(title="Funny Voice Clips",
                              description=f"With over {len(OPTIONS)} different clips, and Rey's flirting clips!",
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