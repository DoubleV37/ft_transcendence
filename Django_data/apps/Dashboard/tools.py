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


def dict_constructor(data: dict) -> dict:
    logger.debug(f"{' dict_constructor ':~^30}")
    token = dict()
    index: int = 0
    for item, value in data.items():
        logger.debug(f"{item = } | {value =}")
        key = 'match ' + str(index)
        token[key] = value
        index = index + 1
    return token