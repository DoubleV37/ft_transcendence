from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from apps.Auth.models import User
from apps.Game.models import Games, UserGame


import logging
logger = logging.getLogger(__name__)


def party_played(me: User) -> list:
    return [mygame for mygame in UserGame.objects.filter(user=me)]


def find_my_opponent(key: list, me: User) -> list:
    key_game_id = [item.game.idGame for item in key]
    all_opponent = UserGame.objects.all()
    opponent = [
        item for item in all_opponent if item.game.idGame in key_game_id
        and item.user != me
    ]
    return opponent


def ordered_party(opponent_key: list, me: User) -> dict:
    ordered = dict(dict())
    index: int = 0
    for opponent in opponent_key:
        id = opponent.game
        myself = UserGame.objects.get(game=id, user=me)
        ordered[str(index)] = {'me': myself, 'id': id, 'opponent': opponent}
        index = index + 1
    return ordered


def data_constructor(data: dict) -> dict:
    token = dict()
    index: int = len(data) - 1
    ref: int = 0
    while index >= 0:
        key = 'match ' + str(ref)
        token[key] = data.get(str(index))
        ref += 1
        index -= 1
    return token


def party_sender(key: int, me: User) -> dict:
    try:
        game = Games.objects.get(id=key)
        myself = UserGame.objects.get(game=key, user=me)
        tmp = list(UserGame.objects.filter(game=key).exclude(user=me))
    except:
        raise
    opponent = None
    for player in tmp:
        if player.user != me:
            opponent = player
    return {'me': myself, 'game': game, 'opponent': opponent}
