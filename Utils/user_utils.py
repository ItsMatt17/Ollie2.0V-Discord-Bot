import discord
from discord import PublicUserFlags

from bot import OllieV2
from config import MY_ID


class UserUtils:
    @staticmethod
    def is_user_in_dict(user_id: int, data: dict) -> bool:
        if str(user_id) in data["User"]:
            return True
        return False

    @staticmethod
    def is_channel_owner(interaction: discord.Interaction, voice_channel: discord.VoiceChannel):
        if not voice_channel.overwrites_for(
                obj=interaction.user).priority_speaker and interaction.user.id != MY_ID:  # Not the one who created channel or not me
            return False
        return True

    @staticmethod
    async def get_user_badges(user: int) -> PublicUserFlags | None:
        if isinstance(user, int):
            try:
                user = await OllieV2.get_bot().fetch_user(user)
                print(user.public_flags.value)

                return tuple(user.public_flags)
            except discord.NotFound or discord.HTTPException as e:
                return

    @staticmethod
    async def get_user_avatar(user: discord.Member | discord.User):
        try:
            return user.avatar.url
        except AttributeError:
            return user.default_avatar.url
