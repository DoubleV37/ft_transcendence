from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import render
from apps.Auth.models import User
import logging, json


logger = logging.getLogger(__name__)


def settings(request):
    return render(request, "Profile/Settings.html")


def profile_infos(request, _id=None):
    item = {}
    if _id is None:
        _user = request.user
        item['type'] = 'himself'
    else:
        _user = User.objects.get(id=_id)
        item['type'] = 'foreign'
        item['status'] = calculate_deltatime(_user)
    item['username'] = _user.username
    item['avatar'] = _user.avatar.url
    return render(request, 'Profile/Profile.html', item)


def avatar(request):
    return render(request, "Profile/Avatar.html")

def skin(request):
    list_paddle = ["/static/images/skins/paddle/Paddle_Grass.png", "/static/images/skins/paddle/Paddle_Amethyst.png", "/static/images/skins/paddle/Paddle_Snow.png"]
    list_ball = ["/static/images/skins/ball/Ball_Cat.png", "/static/images/skins/ball/Ball_Blackhole.png", "/static/images/skins/ball/Ball_Sushi.png"]
    list_back = ["/static/images/skins/background/BG_Forest.png", "/static/images/skins/background/BG_Space.png", "/static/images/skins/background/BG_LoFi.png"]
    _user = request.user
    if request.method == 'GET':
        context = {}
        context['paddle'] = list_paddle.index(_user.skin_paddle)
        context['ball'] = list_ball.index(_user.skin_ball)
        context['background'] = list_back.index(_user.skin_background)
        return render(request, "Profile/Skins.html", context)
    if request.method == 'POST':
        skins = json.loads(request.body)
        logger.info(skins)
        if check_skins_request(skins, list_paddle,
                               list_ball, list_back) is False:
            response = JsonResponse({"success": False, "error": "Wrong informations!"})
        else:
            response = JsonResponse({"success": True})
            _user.skin_ball = skins['ball']
            _user.skin_paddle = skins['paddle']
            _user.skin_background = skins['background']
            _user.save()
        return response


def calculate_deltatime(_user):
    if _user.in_game is True:
        return 'ingame'
    current_time = timezone.now()
    last_time_ping = _user.online_data
    delta_time = current_time - last_time_ping
    if delta_time > timedelta(seconds=3):
        return 'offline'
    return 'online'

def check_skins_request(skins, paddles, balls, backgrounds):
    keys = ['paddle', 'ball', 'background']
    if all(key in skins for key in keys) is False:
        return False
    if skins['paddle'] not in paddles:
        return False
    if skins['ball'] not in balls:
        return False
    if skins['background'] not in backgrounds:
        return False
    return True
