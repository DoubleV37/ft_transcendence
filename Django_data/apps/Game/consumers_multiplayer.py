import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .pong import Pong
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
		await self.join_game()

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

	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data.get("message")
		if not message:
			return
		username = self.scope["user"].username
		if self.user_num == 1:
			if data.get("username") == username :
				if message == "up":
					self.pong.player_pos[1] -= self.pong.player_speed
				elif message == "down":
					self.pong.player_pos[1] += self.pong.player_speed
				elif message == "start":
					await self.start_game()
		else:
			if message == "start":
				await self.start_game()
			elif message == "up":
				await database_sync_to_async(Pong.objects.filter)(idGame=self.room_name).update(paddleL=self.pong.player_pos[0] / 900)
			elif message == "down":
				self.game_settings.paddleL = 
				await database_sync_to_async(Pong.objects.filter)(idGame=self.room_name).update(paddleL=self.)

		# await self.send_game_state()

	async def join_game(self):
		self.pong = Pong(1 , 2 , 10)
		try:
			self.game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
			self.game_settings = await database_sync_to_async(Pong.objects.get)(idGame=game)
			self.user_num = 2
			await self.send(text_data=json.dumps({"message": "start"}))
		except Games.DoesNotExist:
			self.game = await database_sync_to_async(Games.objects.create)(idGame=self.room_name)
			self.game_settings = await database_sync_to_async(Pong.objects.create)(idGame=game)
			self.user_num = 1
		await database_sync_to_async(UserGame.objects.create)(user=self.scope["user"], game=game)

	async def start_game(self):
		game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
		start_num = game.start_num
		game.start_num = start_num + 1
		await database_sync_to_async(game.save)()
		game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
		await self.send(text_data=json.dumps({"message": game.start_num}))
		if self.user_num == 1 :
			while (game.start_num != 2):
				await asyncio.sleep(1)
				game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
			asyncio.create_task(self.run_game())


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
				}
			}
		)

	async def game_state(self, event):
		await self.send(text_data=json.dumps(event['pong']))

	async def run_game(self):
		if self.user_num == 2:
			return
		while self.pong.running:
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
