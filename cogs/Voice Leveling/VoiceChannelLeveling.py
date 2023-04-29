import math
import time
from typing import Tuple

import discord
from discord.ext import commands

from bot import OllieV2
from config import VCLeveling

"""
  "188779992585469952": {
    "Level": 0,
    "Guild": 982514587742142545,
    "Exp": 41223214
  }

"""

users_leveling_cache = {
}


# TODO Update info via tasks
class VoiceChannelLeveling(commands.Cog):
    def __init__(self, bot):
        self.bot: OllieV2 = bot

    async def _get_accumulated_xp(self, user_id: int):
        """Calculates proper amount of xp gained from call. Accessed from dict containing single session call time"""
        try:
            user_start_time: int = users_leveling_cache[user_id]["Start"]
            time_in_minutes: int = ((int(time.time()) * 1000) - user_start_time) // 60_000  # Minutes user was in call
            xp_gained = time_in_minutes * VCLeveling.XP_RATE  # 3.3 xp per minute (200 xp per hour)
            if await self.bot.db.is_double_exp(user_id) is True:
                return xp_gained * 2, time_in_minutes
            return (xp_gained + 200) * 100, time_in_minutes

        except KeyError as e:
            print(e)
            return

    async def _get_saved_xp(self, user_id: int) -> int:
        response = await self.bot.db.fetch("select exp from public.users where discord_id = $1", user_id)
        return response[0][0]

    @staticmethod
    def _calculate_level(xp: int, level: int) -> Tuple[int, int]:
        """Calculates level based on what xp one has and the level they're at"""
        LEVELING_UP = True
        while LEVELING_UP:
            xpNeeded = int((level ** 2) // 2 + 250 + math.floor(level / 100) * 250)  # XP required for level
            print(xpNeeded)
            if xp >= xpNeeded:
                xp -= xpNeeded
                level += 1
                continue
            return level, xp

    async def _update_voice_leveling_data(self, user_id: int, xp: int, time_in_call: int, level: int) -> None:
        # ~~~~~Value Updates~~~~~
        await self.bot.db.execute(
            "update public.users set exp = exp + $1, total_time = total_time + $2, user_level = $3, total_exp = total_exp + $1 where discord_id = $4",
            xp, time_in_call, level, user_id)

    @staticmethod
    def _add_user_to_leveling_dict(member: discord.Member):
        user_id = member.id
        joinTime = int(time.time()) * 1000
        users_leveling_cache[user_id] = {"Start": joinTime, "Guild": member.guild.id}

    async def _level_up_event(self, user_id: int):
        pass

    async def _vc_leave_event(self, user_id: int):
        if (xp_and_time := await self._get_accumulated_xp(user_id=user_id)) is None:
            print("Something went wrong with getting user xp")
            return -1
        saved_xp = await self._get_saved_xp(user_id)
        xp, time_mins = xp_and_time
        xp += saved_xp
        level: int = await self.bot.db.get_user_level(user_id)
        new_level, left_over_xp = self._calculate_level(xp, level)

        await self._update_voice_leveling_data(user_id, left_over_xp, time_mins, new_level)
        if new_level > level:
            await self._level_up_event(user_id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState) -> None:
        if member.bot:
            return

        user_id = member.id
        after_voice = after
        before_voice = before

        if not before_voice.channel and after_voice.channel:  # User join
            self._add_user_to_leveling_dict(member)

        # TODO Investigate see if necessary if check
        if before_voice.channel and not after_voice.channel:  # User leave channel
            if not user_id in users_leveling_cache:  # if user has leveling data
                print("User not in user_info")
                return

            if await self._vc_leave_event(member.id) == -1:
                return

            users_leveling_cache.pop(user_id)


async def setup(bot: commands.Bot):
    await bot.add_cog(VoiceChannelLeveling(bot))
