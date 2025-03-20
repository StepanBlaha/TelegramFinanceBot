import requests

API_KEY = "4A233F809A5C784E081B4B3B55ED5F50"
STEAM_ID = "76561198990361300"  # Replace with the user's SteamID64






def get_steam_user_summary(api_key, steam_id):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        "key": api_key,
        "steamids": steam_id
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