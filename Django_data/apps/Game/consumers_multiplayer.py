import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from .pong import Pong as Pong_game
from .models import Games, UserGame

class MultiPongConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name'][:-1]
		self.room_group_name = f'game_{self.room_name}'
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()
		await self.init_db_game()
		await self.start_game()

	async def disconnect(self, close_code):
		try:
			game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
			if game.nb_users == 2:
				game.nb_users = 19
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
			elif game.nb_users == 0 or game.nb_users == 1:
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
		self.pong = Pong_game(2 , 10, 0)
		self.username = self.scope["user"].username
		self.game, created = await sync_to_async(Games.objects.get_or_create)(idGame=self.room_name)
		if created:
			self.user_num = 1
		else:
			self.user_num = 2
			if self.game.nb_users == 19 or self.game.nb_users == 2:
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
			if message == "up":
				await self.channel_layer.group_send(
					self.room_group_name,
					{
						'type': 'game_message',
						'message': "2up"
					}
				)
			elif message == "down":
				await self.channel_layer.group_send(
					self.room_group_name,
					{
						'type': 'game_message',
						'message': "2down"
					}
				)

	async def game_message(self, event):
		if self.user_num == 2:
			return
		if event['message'] == "2up":
			self.pong.player_pos[0] -= self.pong.player_speed
		elif event['message'] == "2down":
			self.pong.player_pos[0] += self.pong.player_speed

	async def start_game(self):
		game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
		if game.nb_users == 19:
			await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'game_stop',
					'error': {
						"message": "Game stopped"
					}
				}
			)
		if self.user_num == 1 :
			game.nb_users = 2
			await database_sync_to_async(game.save)()
			self.opponent = await self.set_opponent()
			await self.send(text_data=json.dumps({"message": "opponent", "opponent": self.opponent.username, "num": 1}))
			asyncio.create_task(self.run_game())
		else:
			self.opponent = await self.set_opponent()
			await self.send(text_data=json.dumps({"message": "opponent", "opponent": self.opponent.username, "num": 2}))

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
		await self.save_score()
		await self.send_game_finish()

	async def save_score(self):
		game = await database_sync_to_async(Games.objects.get)(idGame=self.room_name)
		user_game = await database_sync_to_async(UserGame.objects.get)(user=self.scope["user"], game=game)
		user_game_opp = await database_sync_to_async(UserGame.objects.get)(user=self.opponent, game=game)
		user_game.score = self.pong.point[1]
		user_game_opp.score = self.pong.point[0]
		if self.pong.point[0] > self.pong.point[1]:
			user_game_opp.winner = True
		else:
			user_game.winner = True
		await database_sync_to_async(user_game.save)()
		await database_sync_to_async(user_game_opp.save)()

	async def send_game_state(self):
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'game_state',
				'pong': {
					"message": "game_state",
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

	async def send_game_finish(self):
		winner = self.username
		if self.pong.point[0] > self.pong.point[1]:
			winner = self.opponent.username
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'game_finish',
				'pong':
				{
					"message": "Game finished",
					"winner": winner,
				}
			}
		)

	async def game_finish(self, event):
		if event['pong']['winner'] == self.username:
			await self.send(text_data=json.dumps({"message": "win"}))
		else:
			await self.send(text_data=json.dumps({"message": "lose"}))
