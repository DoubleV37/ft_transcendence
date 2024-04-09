import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .pong import Pong as Pong_game
from .models import Games, UserGame , Pong

class MultiPongConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = f'game_{self.room_name}'
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()
		await self.init_db_game()

	async def disconnect(self, close_code):
		try:
			game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
			if game.start_num == 2:
				game.start_num = 19
				await database_sync_to_async(game.save)()
				if self.user_num == 1:
					self.pong.running = False
					await self.channel_layer.group_send(
						self.room_group_name,
						{
							'type': 'game_stop',
							'error': {
								"message": "Game stopped"
							}
						}
					)
				else:
					await self.channel_layer.group_send(
						self.room_group_name,
						{
							'type': 'game_stop',
							'error': {
								"message": "User exited"
							}
						}
					)
			elif game.start_num == 0 or game.start_num == 1:
				user_game = await database_sync_to_async(UserGame.objects.get)(user=self.scope["user"], game=game)
				await database_sync_to_async(user_game.delete)()
				if self.user_num == 1:
					await database_sync_to_async(game.delete)()
		except Games.DoesNotExist:
			pass
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def init_db_game(self):
		self.pong = Pong_game(1 , 2 , 10, 0)
		self.username = self.scope["user"].username
		self.game, created = await sync_to_async(Games.objects.get_or_create)(idGame=self.room_name)
		if created:
			self.user_num = 1
			self.game_settings = await sync_to_async(Pong.objects.create)(idGame=self.game)
		else:
			self.user_num = 2
			self.game_settings = await sync_to_async(Pong.objects.get)(idGame=self.game)
			if self.game.start_num == 19 or self.game.start_num == 2:
				await self.channel_layer.group_send(
					self.room_group_name,
					{
						'type': 'game_stop',
						'error': {
							"message": "Game stopped"
						}
					}
				)
		await sync_to_async(UserGame.objects.create)(user=self.scope["user"], game=self.game)


	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data.get("message")
		if not message:
			return
		if self.user_num == 1:
			if data.get("username") == self.username :
				if message == "up":
					self.pong.player_pos[1] -= self.pong.player_speed
				elif message == "down":
					self.pong.player_pos[1] += self.pong.player_speed
				elif message == "start":
					await self.start_game()
				elif message == "stop":
					self.pong.running = False
					await self.channel_layer.group_send(
						self.room_group_name,
						{
							'type': 'game_stop',
							'error': {
								"message": "Game stopped"
							}
						}
					)
		else:
			self.game_settings = await database_sync_to_async(Pong.objects.get)(idGame=self.game)
			if message == "start":
				await self.start_game()
			elif message == "up":
				self.pong.player_pos[0] -= self.pong.player_speed
				self.game_settings.paddleL = self.pong.player_pos[0]
			elif message == "down":
				self.pong.player_pos[0] += self.pong.player_speed
				self.game_settings.paddleL = self.pong.player_pos[0]
			await database_sync_to_async(self.game_settings.save)()

	async def start_game(self):
		game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
		if game.start_num == 19:
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'game_stop',
					'error': {
						"message": "Game stopped"
					}
				}
			)
		start_num = game.start_num
		game.start_num = start_num + 1
		await database_sync_to_async(game.save)()
		game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
		if self.user_num == 1 :
			while (game.start_num != 2):
				await asyncio.sleep(1)
				game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
			self.opponent = await self.set_opponent()
			await self.send(text_data=json.dumps({"message": "opponent", "opponent": self.opponent.username}))
			asyncio.create_task(self.run_game())
		else:
			self.opponent = await self.set_opponent()
			await self.send(text_data=json.dumps({"message": "opponent", "opponent": self.opponent.username}))

	async def set_opponent(self):
		opponents = await sync_to_async(list)(UserGame.objects.filter(game=self.game))
		for opponent in opponents:
			opponent_user = await sync_to_async(lambda: opponent.user)()
			if opponent_user.username != self.username:
				return opponent_user
		return None

	async def game_stop(self, event):
		await self.send(text_data=json.dumps(event['error']))

	async def run_game(self):
		if self.user_num == 2:
			return
		while self.pong.running:
			await self.update_pong()
			self.pong.ball_walk()
			if self.pong.ball_pos[0] < 60 and self.pong.ball_speed[0] < 0:
				self.pong.paddle_bounce(0)
			elif self.pong.ball_pos[0] > 1140 and self.pong.ball_speed[0] > 0:
				self.pong.paddle_bounce(1)
			if self.pong.ball_pos[1] < 5 and self.pong.ball_speed[1] < 0 or self.pong.ball_pos[1] > 895 and self.pong.ball_speed[1] > 0:
				self.pong.ball_speed[1] *= -1
				self.pong.ball_bonce += 1
			if self.pong.ball_pos[0] > 1200:
				self.pong.update_score(0)
			if self.pong.ball_pos[0] < 0:
				self.pong.update_score(1)
			await self.send_game_state()
			await asyncio.sleep(1 / 240)

	async def update_pong(self):
		self.game_settings = await database_sync_to_async(Pong.objects.get)(idGame=self.game)
		self.pong.player_pos[0] = self.game_settings.paddleL

	async def send_game_state(self):
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'game_state',
				'pong': {
					"paddleL": self.pong.player_pos[0] / 900,
					"paddleR": self.pong.player_pos[1] / 900,
					"ballX": self.pong.ball_pos[0] / 1200,
					"ballY": self.pong.ball_pos[1] / 900,
					"score1": self.pong.point[0],
					"score2": self.pong.point[1],
					"ballsize": self.pong.ball_size / 900,
					"paddle1size": self.pong.player_size[0] / 900,
					"paddle2size": self.pong.player_size[1] / 900,
					"opponent": self.opponent.username,
				}
			}
		)

	async def game_state(self, event):
		await self.send(text_data=json.dumps(event['pong']))
