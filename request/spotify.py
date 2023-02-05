import base64
from typing import Union

import aiohttp

from config import SPOTIFY_API, SPOTIFY_CLIENT_ID


async def get_token():
    """Gets token from Spotify API & returns it
    :parameter: `None`
    :return `str` of token
    """
    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_API
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    header = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    async with aiohttp.ClientSession(headers=header) as session:
        # print("getting token")
        result = await session.post(url, data=data, ssl=False)
        if result.status != 200:
            print(f"[API ERROR] {result.status}")

        json_info = await result.json()

    token = json_info["access_token"]
    return token


def get_auth_header(token):
    """Makes a header for the Spotify API

    :param: `str` of token
    """
    return {"Authorization": "Bearer " + token}


async def get_popularity(token, spotify_id):
    """Gets popularity of a song from Spotify API

    :param: `str` of token, `str` of spotify_id
    :return: `int` of popularity
    """
    url = f"https://api.spotify.com/v1/tracks/{spotify_id}"
    headers = get_auth_header(token)
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await session.get(url, ssl=False)
        json_info = await result.json()

    return json_info["popularity"]


async def popularity_rating(spotify_id) -> Union[int, None]:
    """Calls request functions to get popularity of a song
    :param: `str` of spotify track id
    :return: `int` of popularity

    """
    try:
        token = await get_token()
        pop = await get_popularity(token, spotify_id)
        return pop
    except Exception as e:
        print(e)
        return None
