from apps.Auth.models import User
from apps.Game.models import Games, UserGame


import logging
logger = logging.getLogger(__name__)


def party_played_by(me: User) -> list:
    return [mygame for mygame in UserGame.objects.filter(user=me)]


def find_opponent(key: list, me: User) -> list:
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
        myself = UserGame.objects.get_object_or_404(game=id, user=me)
        ordered[str(index)] = {'me': myself, 'id': id, 'opponent': opponent}
        index = index + 1
    return ordered


def populate_context(data: dict) -> dict:
    token = dict()
    index: int = len(data) - 1
    ref: int = 0
    while index >= 0:
        key = 'match ' + str(ref)
        token[key] = data.get_object_or_404(str(index))
        ref += 1
        index -= 1
    return token


def not_his_dashboard(key: int) -> dict:
    index: bool = True
    opponent = None
    myself = None
    game = Games.objects.get_object_or_404(id=key)
    tmp = list(UserGame.objects.filter(game=key))
    for player in tmp:
        if index:
            opponent = player
        else:
            myself = player
        index = False
    return {'me': myself, 'game': game, 'opponent': opponent}


def populate_dashboard(key: int, me: User) -> dict:
    try:
        # try to get a valid game id
        game = Games.objects.get(id=key)
        try:
            # try to get UserGame linked to id game sent. (Owner Games)
            myself = UserGame.objects.get(game=key, user=me)
        except:
            # throwing means populate other user's dashboard
            return not_his_dashboard(key=key)
        tmp = list(UserGame.objects.filter(game=key).exclude(user=me))
    except:
        # Bad id_game sent
        raise
    # way of function which User sent want to populate his own dashboard
    opponent = None
    for player in tmp:
        if player.user != me:
            opponent = player
    return {'me': myself, 'game': game, 'opponent': opponent}
