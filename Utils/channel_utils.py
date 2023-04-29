import discord


class ChannelUtils:

    @staticmethod
    def is_channel_locked(interaction: discord.Interaction, voice_channel: discord.VoiceChannel) -> bool:
        is_locked: bool = voice_channel.permissions_for(
            interaction.guild.default_role).view_channel  # If true can see, False can't see
        return is_locked

    @staticmethod
    def is_custom_channel(voice_channel: discord.VoiceChannel) -> bool:
        perm_overwrites = voice_channel.overwrites
        for key, value in perm_overwrites.items():
            if value.priority_speaker:
                return True
        return False
