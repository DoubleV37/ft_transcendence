import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
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
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
		try:
			game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
			if game.start_num == 2:
				game.start_num = 19
				await database_sync_to_async(game.save)()
		except Games.DoesNotExist:
			pass

	async def init_db_game(self):
		self.pong = Pong_game(1 , 2 , 10)
		self.username = self.scope["user"].username
		try:
			self.game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
			await database_sync_to_async(UserGame.objects.create)(user=self.scope["user"], game=self.game)
			self.game_settings = await database_sync_to_async(Pong.objects.get)(idGame=self.game)
			self.user_num = 2
		except Games.DoesNotExist:
			# await self.send(text_data=json.dumps({"message": "start"}))
			self.game = await database_sync_to_async(Games.objects.create)(idGame=self.room_name)
			await database_sync_to_async(UserGame.objects.create)(user=self.scope["user"], game=self.game)
			self.game_settings = await database_sync_to_async(Pong.objects.create)(idGame=self.game)
			self.user_num = 1
			# self.opponent = await database_sync_to_async(
			# 	lambda: UserGame.objects.filter(game=self.game)
			# 							.exclude(user=self.scope["user"])
			# 							.first().user.username)()



	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data.get("message")
		if not message:
			return
		self.game_settings = await database_sync_to_async(Pong.objects.get)(idGame=self.game)
		if self.user_num == 1:
			if data.get("username") == self.username :
				if message == "up":
					self.pong.player_pos[1] -= self.pong.player_speed
					self.game_settings.paddleR = self.pong.player_pos[1]
				elif message == "down":
					self.pong.player_pos[1] += self.pong.player_speed
					self.game_settings.paddleR = self.pong.player_pos[1]
				elif message == "start":
					await self.start_game()
		else:
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
			asyncio.create_task(self.run_game())

	async def game_stop(self, event):
		await self.send(text_data=json.dumps(event['error']))


	async def run_game(self):
		if self.user_num == 2:
			return
		await self.update_game_settings()
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
			await self.update_game_settings()
			await asyncio.sleep(1 / 240)

	async def update_pong(self):
		self.game_settings = await database_sync_to_async(Pong.objects.get)(idGame=self.game)
		self.pong.player_pos[0] = self.game_settings.paddleL
		self.pong.player_pos[1] = self.game_settings.paddleR
		self.pong.ball_pos[0] = self.game_settings.ballX
		self.pong.ball_pos[1] = self.game_settings.ballY
		self.pong.point[0] = self.game_settings.score1
		self.pong.point[1] = self.game_settings.score2
		self.pong.ball_size = self.game_settings.ballsize
		self.pong.player_size[0] = self.game_settings.paddle1size
		self.pong.player_size[1] = self.game_settings.paddle2size

	async def update_game_settings(self):
		self.game_settings = await database_sync_to_async(Pong.objects.get)(idGame=self.game)
		self.game_settings.paddleL = self.pong.player_pos[0]
		self.game_settings.paddleR = self.pong.player_pos[1]
		self.game_settings.ballX = self.pong.ball_pos[0]
		self.game_settings.ballY = self.pong.ball_pos[1]
		self.game_settings.score1 = self.pong.point[0]
		self.game_settings.score2 = self.pong.point[1]
		self.game_settings.ballsize = self.pong.ball_size
		self.game_settings.paddle1size = self.pong.player_size[0]
		self.game_settings.paddle2size = self.pong.player_size[1]
		await database_sync_to_async(self.game_settings.save)()
		await self.send_game_state()

	async def send_game_state(self):
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'game_state',
				'pong': {
					"paddleL": self.game_settings.paddleL / 900,
					"paddleR": self.game_settings.paddleR / 900,
					"ballX": self.game_settings.ballX / 1200,
					"ballY": self.game_settings.ballY / 900,
					"score1": self.game_settings.score1,
					"score2": self.game_settings.score2,
					"ballsize": self.game_settings.ballsize / 900,
					"paddle1size": self.game_settings.paddle1size / 900,
					"paddle2size": self.game_settings.paddle2size / 900,
				}
			}
		)

	async def game_state(self, event):
		await self.send(text_data=json.dumps(event['pong']))
