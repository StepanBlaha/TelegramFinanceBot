import requests

API_KEY = "4A233F809A5C784E081B4B3B55ED5F50"
STEAM_ID = "76561198990361300"  # Replace with the user's SteamID64






def get_steam_user_summary(apiKey, steamID):
    """
    Function for getting Steam user summary
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :return: User profile data or None if not found
    """
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": apiKey,
        "steamids": steamID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None

def get_user_wishlist(apiKey, steamID):
    """
    Function for getting a user's wishlist
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :return: Wishlist data or None if not found
    """
    url = f"https://api.steampowered.com/IWishlistService/GetWishlist/v1/"
    params = {
        "key": apiKey,
        "steamids": steamID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None

def get_user_bans(apiKey, steamID):
    """
    Function for getting a user's ban status
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :return: Ban status data or None if not found
    """
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/"
    params = {
        "key": apiKey,
        "steamids": steamID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None

def get_user_friendlist(apiKey, steamID):
    """
    Function for getting user's friend list
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :return: Friend list data or None if not found
    """
    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/"
    params = {
        "key": apiKey,
        "steamids": steamID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None

def get_user_steamid(apiKey, steamUrl):
    """
    Function for resolving a Steam vanity URL to Steam ID
    :param apiKey: Steam API key
    :param steam_url: Vanity URL of the Steam user
    :return: Steam ID or None if not found
    """
    url = f"https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {
        "key": apiKey,
        "vanityurl": steamUrl
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None

def get_user_games(apiKey, steamID):
    """
    Function for getting owned games of a user
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :return: List of owned games or None if not found
    """
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": apiKey,
        "steamids": steamID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None

def get_user_recent_games(apiKey, steamID):
    """
    Function for getting recently played games of a user
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :return: List of recently played games or None if not found
    """
    url = f"https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/"
    params = {
        "key": apiKey,
        "steamids": steamID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None

def get_user_level(apiKey, steamID):
    """
    Function for getting Steam level of a user
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :return: Steam level or None if not found
    """
    url = f"https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/"
    params = {
        "key": apiKey,
        "steamids": steamID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None

def get_user_badges(apiKey, steamID, favourite=False):
    """
    Function for getting user's badges
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :param favourite: Boolean flag to get the favourite badge
    :return: List of badges or None if not found
    """
    if favourite:
        url = f"https://api.steampowered.com/IPlayerService/GetFavoriteBadge/v1/"
    else:
        url = f"https://api.steampowered.com/IPlayerService/GetBadges/v1/"
    params = {
        "key": apiKey,
        "steamids": steamID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None


def get_user_game_achievements(apiKey, steamID, appID):
    """
    Function for getting game achievements of a user
    :param apiKey: Steam API key
    :param steamID: Steam user ID
    :param app_id: Steam application ID of the game
    :return: List of achievements or None if not found
    """
    url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/"
    params = {
        "key": apiKey,
        "steamids": steamID,
        "appid": appID
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "response" in data and "players" in data["response"]:
        return data["response"]["players"][0]  # Returns the user's profile data
    return None















user_data = get_steam_user_summary(API_KEY, STEAM_ID)

if user_data:
    print(f"Steam Name: {user_data['personaname']}")
    print(f"Profile URL: {user_data['profileurl']}")
    print(f"Avatar: {user_data['avatarfull']}")
    print(f"Status: {user_data['personastate']}")
else:
    print("User not found or API error")