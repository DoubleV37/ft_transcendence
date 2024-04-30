import json, asyncio, time, hashlib, random
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .pong import Pong#, ai_brain
from .models import Games, UserGame
from django.contrib.auth import get_user_model
from django.utils import timezone

class SoloPongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.roomGroupName = self.generate_room_name()
		self.room_group_name = f'game_{self.roomGroupName}'
		await self.channel_layer.group_add(
			self.room_group_name ,
			self.channel_name
		)
		await self.accept()

	async def disconnect(self , close_code):
		self.pong.running = False
		#save game
		await self.channel_layer.group_discard(
			self.room_group_name ,
			self.channel_name
		)

	def generate_room_name(self):
		user_id = self.scope["user"].id
		username = self.scope["user"].username
		game_name = "Pong"

		random_str = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))

		room_group_name = hashlib.sha256(f"{user_id}_{username}_{game_name}_{random_str}".encode()).hexdigest()
		return room_group_name

	async def init_db_game(self):
		self.game = await database_sync_to_async(Games.objects.create)(idGame=self.roomGroupName)
		self.user_game = await database_sync_to_async(UserGame.objects.create)(user=self.scope["user"], game=self.game)
		if self.ia:
			self.opponent = await database_sync_to_async(get_user_model().objects.get)(username="IA-Ochen")
		else:
			self.opponent = await database_sync_to_async(get_user_model().objects.get)(username="Guest")
		self.opponent_game = await database_sync_to_async(UserGame.objects.create)(user=self.opponent, game=self.game)
		await self.send(text_data=json.dumps({"message": "opponent", "opponent": self.opponent.username, "num": 1, "avatar": self.opponent.avatar.url}))

	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data["message"]
		if message == "up" and self.pong.player_pos[1] > 0:
			self.pong.player_pos[1] -= self.pong.player_speed
		elif message == "down" and self.pong.player_pos[1] < 900:
			self.pong.player_pos[1] += self.pong.player_speed
		if message == "w" and self.pong.player_pos[0] > 0:
			self.pong.player_pos[0] -= self.pong.player_speed
		elif message == "s" and self.pong.player_pos[0] < 900:
			self.pong.player_pos[0] += self.pong.player_speed
		if message == "space" and self.pong.engage > 0:
			self.pong.engage = 0
		if message == "settings":
			self.ia = True
			if data["opponent"] == "player":
				self.ia = False
			self.pong = Pong(data["point_limit"], data["difficulty"], data["powerup"])
			await self.init_db_game()
			asyncio.create_task(self.runGame())

	async def sendUpdateGame(self):
		try :
			await self.send(text_data = json.dumps({
						"paddleL" : self.pong.player_pos[0]/900 ,
						"paddleR" : self.pong.player_pos[1]/900 ,
						"ballX" : self.pong.ball_pos[0]/1200 ,
						"ballY" : self.pong.ball_pos[1]/900 ,
						"ballspeedX" : self.pong.ball_speed[0] ,
						"ballspeedY" : self.pong.ball_speed[1] ,
						"score1" : self.pong.point[0] ,
						"score2" : self.pong.point[1] ,
						"ballsize" : self.pong.ball_size/900 ,
						"paddle1size" : self.pong.player_size[0]/900 ,
						"paddle2size" : self.pong.player_size[1]/900 ,
						"powerupY" : self.pong.powerup_pos[1]/900 ,
						"powerupsize" : self.pong.powerup_size/900 ,
						"time" : self.pong.time ,
						"message" : "game_state"}))
		except Exception as e:
			print(e)

	async def runGame(self):
		loop = time.time()
		while self.pong.running:
			loop += 1/240
			# ball move
			self.pong.ball_walk()
			self.pong.powerup_run()
			# paddle bounce
			if self.pong.ball_pos[0] < 60 and self.pong.ball_speed[0] < 0:
				self.pong.paddle_bounce(0)
			elif self.pong.ball_pos[0] > 1140 and self.pong.ball_speed[0] > 0:
				self.pong.paddle_bounce(1)
			# wall bounce
			if self.pong.ball_pos[1] < 5 and self.pong.ball_speed[1] < 0 or self.pong.ball_pos[1] > 895 and self.pong.ball_speed[1] > 0:
				self.pong.ball_speed[1] *= -1
				self.pong.ball_bonce += 1
			# point
			if self.pong.ball_pos[0] > 1200:
				self.pong.update_score(0)
			if self.pong.ball_pos[0] < 0:
				self.pong.update_score(1)
			await self.sendUpdateGame()
			await asyncio.sleep(loop - time.time())
		await self.save_stats()
		if self.pong.point_limit == self.pong.point[0] or self.pong.point_limit == self.pong.point[1]:
			await self.send_game_finish()

	async def save_stats(self):
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

	async def send_game_finish(self):
		if self.pong.point[0] > self.pong.point[1] and self.ia:
			winner = "IA-Ochen"
		elif self.pong.point[0] > self.pong.point[1] and not self.ia:
			winner = "guest"
		else:
			winner = self.scope["user"].username
		await self.send(text_data = json.dumps({
						"message" : "game_finish" ,
						"winner" : winner}))
