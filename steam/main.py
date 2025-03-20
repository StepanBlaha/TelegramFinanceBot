API_KEY = "4A233F809A5C784E081B4B3B55ED5F50"
steam_id = "76561198990361300"
import os
from steam_web_api import Steam
import json

KEY = "4A233F809A5C784E081B4B3B55ED5F50"
steam = Steam(KEY)

user = steam.users.get_profile_wishlist(steam_id=steam_id, page=1)


def get_friends(userId, expanded=False):
    """
    Function for getting users friend list
    :param userId: user id
    :param expanded: boolean to get friend list with more data
    :return: friend list
    """
    friends = steam.users.get_user_friends_list(userId, enriched=expanded)
    return friends

def get_acc_info(userId):
    """
    Function for getting users account info
    :param userId: user id
    :return: account info
    """
    user = steam.users.get_user_details(userId)
    return user

def get_recent_games(userId):
    """
    Function for getting users recent games
    :param userId: User id
    :return: list of recent games
    """
    recentGames = steam.users.get_user_recently_played_games(userId)
    return recentGames

def get_games(userId):
    """
    Function for getting users games
    :param userId: user id
    :return: list of games
    """
    games = steam.users.get_owned_games(userId)
    return games

def get_level(userId):
    """
    Function for getting users level
    :param userId: user id
    :return: user level
    """
    level = steam.users.get_user_steam_level(userId)
    return level

def get_badges(userId):
    """
    Function for getting users badges
    :param userId: user id
    :return: list of badges
    """
    badges = steam.users.get_user_badges(userId)
    return badges

def search_games(search):
    """
    Function for searching for games on steam
    :param search: word for search
    :return: list of games
    """
    games = steam.apps.search_games(search)
    return games

def get_game_details(gameId):
    """
    Function for getting game details
    :param gameId: game id
    :return: list of game details
    """
    details = steam.apps.get_app_details(gameId)
    return details

user = steam.users.get_profile_wishlist("76561198990361300")


