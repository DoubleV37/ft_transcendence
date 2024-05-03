import json, asyncio, time
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .pong import Pong as Pong_game
from .models import Games, UserGame
from django.utils import timezone
from channels.exceptions import StopConsumer
import logging
import websockets
import threading

logger = logging.getLogger(__name__)


class MultiPongConsumer(AsyncWebsocketConsumer):

    async def websocket_disconnect(self, message):
        try:
            logger.info(f"{self.scope['user'].username = } - websocket_disconnect - 1")
            for group in self.groups:
                await self.channel_layer.group_discard(group, self.channel_name)
        except AttributeError:
            logger.info(f"{self.scope['user'].username = } - websocket_disconnect - 2")
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        logger.info(f"{self.scope['user'].username = } - websocket_disconnect - 3")
        await self.disconnect(message["code"])
        logger.info(f"{self.scope['user'].username = } - websocket_disconnect - 4")
        raise StopConsumer()


    async def connect(self):
        logger.info(f"{self.scope['user'].username = } - connect - 1")
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"][:-1]
        self.room_group_name = f"game_{self.room_name}"
        logger.info(f"{self.scope['user'].username = } - connect - 2")
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        logger.info(f"{self.scope['user'].username = } - connect - 3")
        await self.accept()
        logger.info(f"{self.scope['user'].username = } - connect - 4")
        #self.thread = threading await self.init_db_game()
        self.thread_db = threading.Thread(target=self.init_db_game)
        self.thread_db.start()
        logger.info(f"{self.scope['user'].username = } - connect - 5")
        #await self.start_game()
        self.thread_start = threading.Thread(target=self.start_game)
        self.thread_start.start()

    async def disconnect(self, close_code):
        logger.info(f"{self.scope['user'].username = } - connect - 1")
        game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
        logger.info(f"{self.scope['user'].username = } - connect - 2")
        if game.nb_users == 2:
            logger.info(f"{self.scope['user'].username = } - connect - 3")
            game.nb_users = 19
            if game.running is True:
                logger.info(f"{self.scope['user'].username = } - connect - 4")
                game.running = False
                winner = self.opponent.username
                self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "game_finish",
                        "pong": {
                            "message": "Game finished",
                            "winner": winner,
                        },
                    },
                )
                logger.info(f"{self.scope['user'].username = } - connect - 5")
            await database_sync_to_async(game.save)()
        elif game.nb_users in (0, 1):
            logger.info(f"{self.scope['user'].username = } - connect - 6")
            user_game = await database_sync_to_async(UserGame.objects.get)(
                user=self.scope["user"], game=game
            )
            logger.info(f"{self.scope['user'].username = } - connect - 7")
            await database_sync_to_async(user_game.delete)()
            if self.user_num == 1:
                logger.info(f"{self.scope['user'].username = } - connect - 8")
                await database_sync_to_async(game.delete)()
        logger.info(f"{self.scope['user'].username = } - connect - 9")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def init_db_game(self):
        self.db_wait = True
        logger.info(f"{self.scope['user'].username = } - init_db_game - 1")
        self.pong = Pong_game(2, 10, 0)
        self.username = self.scope["user"].username
        self.game, created = await sync_to_async(Games.objects.get_or_create)(
            idGame=self.room_name
        )
        logger.info(f"{self.scope['user'].username = } - init_db_game - 2")
        if created:
            logger.info(f"{self.scope['user'].username = } - init_db_game - 3")
            self.user_num = 1
        else:
            logger.info(f"{self.scope['user'].username = } - init_db_game - 4")
            self.user_num = 2
            if self.game.nb_users == 19 or self.game.nb_users == 2:
                logger.info(f"{self.scope['user'].username = } - init_db_game - 5")
                user_game = await database_sync_to_async(UserGame.objects.get)(
                    user=self.scope["user"], game=self.game
                )
                logger.info(f"{self.scope['user'].username = } - init_db_game - 6")
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop", "error": {"message": "Game stopped"}},
                )
                logger.info(f"{self.scope['user'].username = } - init_db_game - 7")
                self.db_wait = False
                return
        logger.info(f"{self.scope['user'].username = } - init_db_game - 8")
        await sync_to_async(UserGame.objects.create)(
            user=self.scope["user"], game=self.game
        )
        self.db_wait = False


    async def receive(self, text_data):
        logger.info(f"{self.scope['user'].username = } - receive - 1")
        data = json.loads(text_data)
        message = data.get("message")
        if not message:
            logger.info(f"{self.scope['user'].username = } - receive - 2")
            return
        if self.user_num == 1:
            logger.info(f"{self.scope['user'].username = } - receive - 3")
            if message == "settings":
                self.pong.point_limit = data.get("point_limit")
                self.pong.paddle_radius = data.get("difficulty")
                self.pong.powerup = data.get("powerup")
            if message == "up":
                self.pong.player_pos[1] -= self.pong.player_speed
            elif message == "down":
                self.pong.player_pos[1] += self.pong.player_speed
            elif message == "stopGame":
                logger.info(f"{self.scope['user'].username = } - receive - 4")
                self.pong.running = False
            elif message == "stop":
                logger.info(f"{self.scope['user'].username = } - receive - 4")
                self.pong.running = False
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop", "error": {"message": "Game stopped"}},
                )
                logger.info(f"{self.scope['user'].username = } - receive - 5")
        else:
            logger.info(f"{self.scope['user'].username = } - receive - 6")
            if message == "up":
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "game_message", "message": "2up"}
                )
            elif message == "down":
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "game_message", "message": "2down"}
                )
            elif message == "stop":
                logger.info(f"{self.scope['user'].username = } - receive - 7")
                self.pong.running = False
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop", "error": {"message": "Game stopped"}},
                )
        logger.info(f"{self.scope['user'].username = } - receive - 8")


    async def game_message(self, event):
        if self.user_num == 2:
            logger.info(f"{self.scope['user'].username = } - game_message - 1")
            return
        if event["message"] == "2up":
            logger.info(f"{self.scope['user'].username = } - game_message - 2")
            self.pong.player_pos[0] -= self.pong.player_speed
        elif event["message"] == "2down":
            logger.info(f"{self.scope['user'].username = } - game_message - 3")
            self.pong.player_pos[0] += self.pong.player_speed


    async def wait_opponent(self):
        logger.info(f"{self.scope['user'].username = } - wait_opponent - 1")
        game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
        logger.info(f"{self.scope['user'].username = } - wait_opponent - 2")
        while game.nb_users != 2:
            await asyncio.sleep(1)
            game = await database_sync_to_async(Games.objects.get)(
                idGame=self.room_name
            )
            if game.nb_users == 19:
                logger.info(f"{self.scope['user'].username = } - wait_opponent - 3")
                user_game = await database_sync_to_async(UserGame.objects.get)(
                    user=self.scope["user"], game=self.game
                )
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop", "error": {"message": "Game stopped"}},
                )
                return False  # Indique que le jeu est arrêté
        logger.info(f"{self.scope['user'].username = } - wait_opponent - 4")
        return True  # Indique que le deuxième joueur a rejoint


    async def start_game(self):
        self.start_wait = True
        while self.db_wait is True:
            await asyncio.sleep(1)
        logger.info(f"{self.scope['user'].username = } - start_game - 1")
        game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
        logger.info(f"{self.scope['user'].username = } - start_game - 2")
        if game.nb_users == 19:
            logger.info(f"{self.scope['user'].username = } - start_game - 3")
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "game_stop", "error": {"message": "Game stopped"}},
            )
            logger.info(f"{self.scope['user'].username = } - start_game - 4")
        my_user = self.scope["user"]
        if self.user_num == 1:
            logger.info(f"{self.scope['user'].username = } - start_game - 5")
            enough_users = await self.wait_opponent()
            logger.info(f"{self.scope['user'].username = } - start_game - 6")
            if not enough_users:
                logger.info(f"{self.scope['user'].username = } - start_game - 7")
                self.start_wait = False
                return
            game.nb_users = 2
            self.opponent = await self.set_opponent()
            logger.info(f"{self.scope['user'].username = } - start_game - 8")
            await self.send(
                text_data=json.dumps(
                    {
                        "message": "opponent",
                        "num": 1,
                        "opponent_name": self.opponent.username,
                        "opponent_paddle": self.opponent.skin_paddle,
                        "opponent_avatar": self.opponent.avatar.url,
                        "my_name": my_user.username,
                        "my_ball": my_user.skin_ball,
                        "my_paddle": my_user.skin_paddle,
                        "my_background": my_user.skin_background,
                        "my_avatar": my_user.avatar.url,
                    }
                )
            )
            logger.info(f"{self.scope['user'].username = } - start_game - 9")
            game.running = True
            await database_sync_to_async(game.save)()
            logger.info(f"{self.scope['user'].username = } - start_game - 10")
            asyncio.create_task(self.run_game())
        else:
            logger.info(f"{self.scope['user'].username = } - start_game - 11")
            game.nb_users = 2
            self.opponent = await self.set_opponent()
            logger.info(f"{self.scope['user'].username = } - start_game - 12")
            await self.send(
                text_data=json.dumps(
                    {
                        "message": "opponent",
                        "num": 2,
                        "opponent_name": self.opponent.username,
                        "opponent_paddle": self.opponent.skin_paddle,
                        "opponent_avatar": self.opponent.avatar.url,
                        "my_name": my_user.username,
                        "my_ball": my_user.skin_ball,
                        "my_paddle": my_user.skin_paddle,
                        "my_background": my_user.skin_background,
                        "my_avatar": my_user.avatar.url,
                    }
                )
            )
            logger.info(f"{self.scope['user'].username = } - start_game - 13")
        await database_sync_to_async(game.save)()
        self.start_wait = True
        logger.info(f"{self.scope['user'].username = } - start_game - 14")


    async def set_opponent(self):
        logger.info(f"{self.scope['user'].username = } - set_opponent - 1")
        opponents = await sync_to_async(list)(UserGame.objects.filter(game=self.game))
        logger.info(f"{self.scope['user'].username = } - set_opponent - 2")
        for opponent in opponents:
            opponent_user = await sync_to_async(lambda: opponent.user)()
            if opponent_user.username != self.username:
                logger.info(f"{self.scope['user'].username = } - set_opponent - 3")
                return opponent_user
        logger.info(f"{self.scope['user'].username = } - set_opponent - 4")
        return None


    async def game_stop(self, event):
        logger.info(f"{self.scope['user'].username = } - game_stop - 1")
        await self.send(text_data=json.dumps(event["error"]))


    async def run_game(self):
        logger.info(f"{self.scope['user'].username = } - run_game - 1")
        loop = time.time()
        while self.pong.running:
            loop += 1 / 240
            self.pong.ball_walk()
            if self.pong.ball_pos[0] < 60 and self.pong.ball_speed[0] < 0:
                self.pong.paddle_bounce(0)
            elif self.pong.ball_pos[0] > 1140 and self.pong.ball_speed[0] > 0:
                self.pong.paddle_bounce(1)
            if (
                self.pong.ball_pos[1] < 5
                and self.pong.ball_speed[1] < 0
                or self.pong.ball_pos[1] > 895
                and self.pong.ball_speed[1] > 0
            ):
                self.pong.ball_speed[1] *= -1
                self.pong.ball_bonce += 1
            if self.pong.ball_pos[0] > 1200:
                self.pong.update_score(0)
            if self.pong.ball_pos[0] < 0:
                self.pong.update_score(1)
            await self.sendUpdateGame()
            await asyncio.sleep(loop - time.time())
        logger.info(f"{self.scope['user'].username = } - run_game - 2")
        await self.save_stats()
        logger.info(f"{self.scope['user'].username = } - run_game - 3")
        await self.send_game_finish()
        logger.info(f"{self.scope['user'].username = } - run_game - 4")


    async def save_stats(self):
        logger.info(f"{self.scope['user'].username = } - save_stats - 1")
        self.game = await database_sync_to_async(Games.objects.get)(
            idGame=self.room_name
        )
        logger.info(f"{self.scope['user'].username = } - save_stats - 2")
        self.user_game = await database_sync_to_async(UserGame.objects.get)(
            user=self.scope["user"], game=self.game
        )
        logger.info(f"{self.scope['user'].username = } - save_stats - 3")
        self.opponent_game = await database_sync_to_async(UserGame.objects.get)(
            user=self.opponent, game=self.game
        )
        logger.info(f"{self.scope['user'].username = } - save_stats - 4")
        dict_stats = self.pong.print_stats()
        self.game.running = False
        self.game.date = timezone.now()
        self.game.duration = self.pong.time / 240
        self.game.pwr_up = self.pong.powerup
        self.game.nb_rounds = self.pong.point[0] + self.pong.point[1]
        self.game.bounce = dict_stats["bounce"]
        self.game.max_exchange = dict_stats["max_exchange"]
        self.user_game.max_speed = dict_stats["max_speed"][1]
        self.user_game.score = dict_stats["score2"]
        self.opponent_game.max_speed = dict_stats["max_speed"][0]
        self.opponent_game.score = dict_stats["score1"]
        if dict_stats["score1"] > dict_stats["score2"]:
            logger.info(f"{self.scope['user'].username = } - save_stats - 5")
            self.opponent_game.winner = True
        else:
            logger.info(f"{self.scope['user'].username = } - save_stats - 6")
            self.user_game.winner = True
        logger.info(f"{self.scope['user'].username = } - save_stats - 7")
        await database_sync_to_async(self.game.save)()
        logger.info(f"{self.scope['user'].username = } - save_stats - 8")
        await database_sync_to_async(self.user_game.save)()
        logger.info(f"{self.scope['user'].username = } - save_stats - 9")
        await database_sync_to_async(self.opponent_game.save)()
        logger.info(f"{self.scope['user'].username = } - save_stats - 10")


    async def sendUpdateGame(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "game_state",
                "pong": {
                    "message": "game_state",
                    "paddleL": self.pong.player_pos[0] / 900,
                    "paddleR": self.pong.player_pos[1] / 900,
                    "paddle1size": self.pong.player_size[0] / 900,
                    "paddle2size": self.pong.player_size[1] / 900,
                    "ballX": self.pong.ball_pos[0] / 1200,
                    "ballY": self.pong.ball_pos[1] / 900,
                    "ballspeedX": self.pong.ball_speed[0],
                    "ballspeedY": self.pong.ball_speed[1],
                    "ballsize": self.pong.ball_size / 900,
                    "score1": self.pong.point[0],
                    "score2": self.pong.point[1],
                    "powerupY": self.pong.powerup_pos[1] / 900,
                    "powerupsize": self.pong.powerup_size / 900,
                    "time": self.pong.time,
                },
            },
        )


    async def game_state(self, event):
        logger.info(f"{self.scope['user'].username = } - game_state - 1")
        await self.send(text_data=json.dumps(event["pong"]))
        logger.info(f"{self.scope['user'].username = } - game_state - 2")


    async def send_game_finish(self):
        logger.info(f"{self.scope['user'].username = } - send_game_finish - 1")
        winner = self.username
        if self.pong.point[0] > self.pong.point[1]:
            logger.info(f"{self.scope['user'].username = } - send_game_finish - 2")
            winner = self.opponent.username
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "game_finish",
                "pong": {
                    "message": "Game finished",
                    "winner": winner,
                },
            },
        )
        logger.info(f"{self.scope['user'].username = } - send_game_finish - 3")


    async def game_finish(self, event):
        logger.info(f"{self.scope['user'].username = } - game_finish - 1")
        if event["pong"]["winner"] == self.username:
            logger.info(f"{self.scope['user'].username = } - game_finish - 2")
            await self.send(text_data=json.dumps({"message": "win"}))
        else:
            logger.info(f"{self.scope['user'].username = } - game_finish - 3")
            await self.send(text_data=json.dumps({"message": "lose"}))
