import discord


# TODO Refactor all back into desired class
def no_vc() -> discord.Embed:
    embed = (discord.Embed(
        color=discord.Color.green(),
        title="No Voice Channel...",
        description="You are sadly, not in a voice channel 🤔."
    ))
    return embed


def no_user_found(user) -> discord.Embed:
    embed = (
        discord.Embed(
            color=discord.Color.red(),
            title="User not found...",
            description=f"User <@{user}> not found :("
        )
    )
    return embed


def successful_invite(channel_link, user : discord.Member) -> discord.Embed:
    user_id = user.mention
    embed = (discord.Embed(
            color=discord.Color.green(),
            title=f"Channel Invite",
            description=f"{user_id} invited you to a voice channel!"

    ).add_field(name=f"", value=f"[Click Here to Join!]({channel_link})"
    ).set_thumbnail(url=user.display_avatar.url
    )
)
    return embed

