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

logger = logging.getLogger(__name__)


class MultiPongConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"][:-1]
        self.room_group_name = f"game_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.init_db_game()
        await self.start_game()

    async def disconnect(self, close_code):
        logger.debug(f"{self.scope['user'].username = }")
        game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
        logger.debug("Hello 0 ?")
        logger.debug(f"{game.running = }")
        logger.debug(f"{game.nb_users = }")
        if game.nb_users == 2:
            game.nb_users = 19
            logger.debug("Hello 1 ?")
            if game.running == True:
                logger.debug("Hello 2 ?")
                game.running = False
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop",
                     "error": {"message": "Game stopped",
                               "name": self.scope['user'].username}}
                )
            await database_sync_to_async(game.save)()
        elif game.nb_users == 0 or game.nb_users == 1:
            user_game = await database_sync_to_async(UserGame.objects.get)(
                user=self.scope["user"], game=game
            )
            await database_sync_to_async(user_game.delete)()
            if self.user_num == 1:
                await database_sync_to_async(game.delete)()

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def init_db_game(self):
        self.pong = Pong_game(2, 10, 0)
        self.username = self.scope["user"].username
        self.game, created = await sync_to_async(Games.objects.get_or_create)(
            idGame=self.room_name
        )
        if created:
            self.user_num = 1
            logger.debug(f"{ self.username = } - init_db - 1")

        else:
            logger.debug(f"{ self.username = } - init_db - 2")
            self.user_num = 2
            if self.game.nb_users == 19 or self.game.nb_users == 2:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop", "error": {"message": "Game stopped"}},
                )
        await sync_to_async(UserGame.objects.create)(
            user=self.scope["user"], game=self.game
        )
        logger.debug(f"{ self.username = } - init_db_game OK")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        if not message:
            return
        if self.user_num == 1:
            if message == "settings":
                self.pong.point_limit = data.get("point_limit")
                self.pong.paddle_radius = data.get("difficulty")
                self.pong.powerup = data.get("powerup")
            if message == "up":
                self.pong.player_pos[1] -= self.pong.player_speed
            elif message == "down":
                self.pong.player_pos[1] += self.pong.player_speed
            elif message == "space" and self.pong.engage > 0:
                self.pong.engage = 0
            elif message == "stopGame":
                self.pong.running = False
            elif message == "stop":
                self.pong.running = False
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop", "error": {"message": "Game stopped"}},
                )
        else:
            if message == "up":
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "game_message", "message": "2up"}
                )
            elif message == "down":
                await self.channel_layer.group_send(
                    self.room_group_name, {"type": "game_message", "message": "2down"}
                )
            elif message == "stop":
                self.pong.running = False
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop", "error": {"message": "Game stopped"}},
                )

    async def game_message(self, event):
        if self.user_num == 2:
            return
        if event["message"] == "2up":
            self.pong.player_pos[0] -= self.pong.player_speed
        elif event["message"] == "2down":
            self.pong.player_pos[0] += self.pong.player_speed

    async def wait_opponent(self):
        game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
        while game.nb_users != 2:
            await asyncio.sleep(1)
            game = await database_sync_to_async(Games.objects.get)(
                idGame=self.room_name
            )
            if game.nb_users == 19:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "game_stop", "error": {"message": "Game stopped"}},
                )
                return False  # Indique que le jeu est arrêté
        return True  # Indique que le deuxième joueur a rejoint

    async def start_game(self):
        game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
        if game.nb_users == 19:
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "game_stop", "error": {"message": "Game stopped"}},
            )
        my_user = self.scope["user"]
        if self.user_num == 1:
            logger.info(f"{my_user.username = } - start_game - 1")
            enough_users = await self.wait_opponent()
            if not enough_users:
                logger.info(f"{my_user.username = } - not enough user - 1")
                return
            game.nb_users = 2
            self.opponent = await self.set_opponent()
            logger.info(f"{self.opponent.username = } - opponenent name - 1")
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
            game.running = True
            await database_sync_to_async(game.save)()
            asyncio.create_task(self.run_game())
        else:
            logger.info(f"{my_user.username = } - start_game - 2")
            game.nb_users = 2
            self.opponent = await self.set_opponent()
            logger.info(f"{self.opponent.username = } - opponenent name - 2")

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
        await database_sync_to_async(game.save)()
        logger.info(f"{game.nb_users = } - start_game over - nb_users")
        logger.info(f"{self.opponent.username = } - start_game over")

    async def set_opponent(self):
        opponents = await sync_to_async(list)(UserGame.objects.filter(game=self.game))
        for opponent in opponents:
            opponent_user = await sync_to_async(lambda: opponent.user)()
            if opponent_user.username != self.username:
                return opponent_user
        return None

    async def game_stop(self, event):
        await self.send(text_data=json.dumps(event["error"]))

    async def run_game(self):
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
        await self.save_stats()
        await self.send_game_finish()

    async def save_stats(self):
        self.game = await database_sync_to_async(Games.objects.get)(
            idGame=self.room_name
        )
        self.user_game = await database_sync_to_async(UserGame.objects.get)(
            user=self.scope["user"], game=self.game
        )
        self.opponent_game = await database_sync_to_async(UserGame.objects.get)(
            user=self.opponent, game=self.game
        )
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
            self.opponent_game.winner = True
        else:
            self.user_game.winner = True
        await database_sync_to_async(self.game.save)()
        await database_sync_to_async(self.user_game.save)()
        await database_sync_to_async(self.opponent_game.save)()

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
        await self.send(text_data=json.dumps(event["pong"]))

    async def send_game_finish(self):
        winner = self.username
        if self.pong.point[0] > self.pong.point[1]:
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

    async def game_finish(self, event):
        if event["pong"]["winner"] == self.username:
            await self.send(text_data=json.dumps({"message": "win"}))
        else:
            await self.send(text_data=json.dumps({"message": "lose"}))
