from typing import Final, Optional

import discord
import easy_pil
from discord import File, app_commands
from discord.ext import commands
from discord.flags import PublicUserFlags
from easy_pil import Canvas, Editor, Font

from Utils.file_utils import FileUtils
from config import VCLeveling

USER_BADGES: Final[dict] = {
    PublicUserFlags.bug_hunter: 'bug_hunter_badge',
    PublicUserFlags.bug_hunter_level_2: 'bug_buster_badge',
    PublicUserFlags.staff: 'staff_badge',
    PublicUserFlags.partner: 'partner_badge',
    PublicUserFlags.early_supporter: 'early_support_badge',
    PublicUserFlags.hypesquad: 'hypesquad_events_badge',
    PublicUserFlags.verified_bot_developer: 'verified_developer_badge',
    # Figure out nitro

}


class LevelCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def get_voice_photo(user_obj: discord.Member, user_info: tuple) -> File:
        if user_obj is None or user_info is None:
            raise Exception("A param is none in get_voice_photo")

        user_level, total_time, exp = user_info
        canvas: Canvas = Canvas((814, 197), color="#23272A")
        editor = Editor(canvas)
        # easy_pil
        # user_resources = {xp_bar : editor.}

        profile_pic = await easy_pil.load_image_async(user_obj.avatar.url)

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        file = File(fp=editor.image_bytes, filename="voice_rank_level.png")
        return file

    @staticmethod
    def get_user_level(user_id: int):
        data = FileUtils.json_file_open(VCLeveling.VC_FILE_PATH)
        users = data["users"]
        if (selected_user := users.get(str(user_id))) is None:
            return None

        user_level, total_time, exp = selected_user["Level"], selected_user["Total Time"], selected_user["Exp"]
        print(f"User Level: {user_level} | Total Time {total_time} | EXP : {exp}")

        return user_level, total_time, exp

    @app_commands.command(name="level", description="Get voice channel level")
    async def level(self, interaction: discord.Interaction, user: Optional[discord.Member]) -> None:
        if not user:
            user_id: int = interaction.user.id
            user_obj: discord.Member = interaction.user
        else:
            user_id: int = user.id
            user_obj: discord.Member = user

        if (response := self.get_user_level(user_id)) is None:
            await interaction.response.send_message(f"User <@{user_id}> has no voice leveling data...")
            return

        level_photo = await self.get_voice_photo(user_obj=user_obj, user_info=response)
        await interaction.response.send_message(file=level_photo)


async def setup(bot):
    await bot.add_cog(LevelCommand(bot))
