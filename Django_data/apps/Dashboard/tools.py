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


def ordered_party(opponent_key: list, me: User) -> list:
    ordered = list(list())
    for opponent in opponent_key:
        id = opponent.game
        myself = UserGame.objects.get(game=id, user=me)
        ordered.append([myself, id, opponent])
    return ordered
