from .models import MatchmakingUser
import json, asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .pong import Pong, ai_brain
from asgiref.sync import sync_to_async
import hashlib

class SoloPongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.roomGroupName = "pong_game"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
		self.pong = Pong(1 , 2 , 10)

		asyncio.create_task(self.runGame())

	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName ,
			self.channel_layer
		)

	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data["message"]
		username = data["username"]
		if message == "up":
			self.pong.player_pos[1] = self.pong.player_pos[1] - self.pong.player_speed
		elif message == "down":
			self.pong.player_pos[1] = self.pong.player_pos[1] + self.pong.player_speed

	async def sendMessage(self):
		await self.send(text_data = json.dumps({"paddleL" : self.pong.player_pos[0]/900 ,
												"paddleR" : self.pong.player_pos[1]/900 ,
												"ballX" : self.pong.ball_pos[0]/1200 ,
												"ballY" : self.pong.ball_pos[1]/900 ,
												"score1" : self.pong.point[0] ,
												"score2" : self.pong.point[1] ,
												"ballsize" : self.pong.ball_size/900 ,
												"paddle1size" : self.pong.player_size[0]/900 ,
												"paddle2size" : self.pong.player_size[1]/900 ,
												"type" : "sendMessage"}))

	async def runGame(self):
		while self.pong.running:
			# ia move
			self.pong.player_pos[0] = ai_brain(self.pong, 1, 20)
			# ball move
			self.pong.ball_walk()
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
			await self.sendMessage()
			await asyncio.sleep(1/240)

class MultiPongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.roomGroupName = self.scope["url_route"]["kwargs"]["room_name"]
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()


	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName,
			self.channel_name  # Corrected this line
		)


	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data["message"]
		username = data["username"]
		if message == "up":
			self.pong.player_pos[1] = self.pong.player_pos[1] - self.pong.player_speed
		elif message == "down":
			self.pong.player_pos[1] = self.pong.player_pos[1] + self.pong.player_speed
		elif message == "start":
			self.pong = Pong(1 , 2 , 10)
			asyncio.create_task(self.runGame())


	async def sendMessage(self):
		await self.channel_layer.group_send(
			self.roomGroupName , json.dumps({"paddleL" : self.pong.player_pos[0]/900 ,
												"paddleR" : self.pong.player_pos[1]/900 ,
												"ballX" : self.pong.ball_pos[0]/1200 ,
												"ballY" : self.pong.ball_pos[1]/900 ,
												"score1" : self.pong.point[0] ,
												"score2" : self.pong.point[1] ,
												"ballsize" : self.pong.ball_size/900 ,
												"paddle1size" : self.pong.player_size[0]/900 ,
												"paddle2size" : self.pong.player_size[1]/900 ,
												"type" : "sendMessage"})
		)

	async def runGame(self):
		while self.pong.running:
			# ia move
			self.pong.player_pos[0] = ai_brain(self.pong, 1, 20)
			# ball move
			self.pong.ball_walk()
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
			await self.sendMessage()
			await asyncio.sleep(1/240)

class MatchmakingPongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = "matchmaking"
		self.roomGroupName = "matchmaking"
		await self.channel_layer.group_add(
			self.roomGroupName,
			self.channel_name
		)
		await self.accept()

	async def receive(self, text_data):
		if text_data == 'search':
			await self.add_to_matchmaking_pool()
			await self.send(text_data=json.dumps({"type": "searching"}))

			# Vérifie si le pool de matchmaking contient deux utilisateurs
			num = await self.len_pool()
			await self.send(text_data=str(num))
			if await self.len_pool() >= 2:
				# Récupère les deux utilisateurs du pool
				users = await self.get_pool_members()
				# Crée une salle de jeu pour eux
				# new_room_name = hashlib.sha256(f"{users[0]}{users[1]}".encode()).hexdigest()
				new_room_name = "caca"
				await self.create_game_room(new_room_name, users)

	async def create_game_room(self, room_name, users):
		for user in users:
			await self.channel_layer.group_add(room_name, user)
			# Informez l'utilisateur de rejoindre la nouvelle salle de jeu
			await self.channel_layer.send(user, {
				"type": "matchmaking.success",
				"room_name": room_name
			})
		await self.channel_layer.group_discard(self.roomGroupName, users[0])
		await self.channel_layer.group_discard(self.roomGroupName, users[1])

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName,
			self.channel_name
		)
		await self.remove_from_matchmaking_pool()

	@sync_to_async
	def add_to_matchmaking_pool(self):
		MatchmakingUser.objects.create(channel_name=self.channel_name)

	@sync_to_async
	def remove_from_matchmaking_pool(self):
		MatchmakingUser.objects.filter(channel_name=self.channel_name).delete()

	@sync_to_async
	def len_pool(self):
		return MatchmakingUser.objects.count()

	@sync_to_async
	def get_pool_members(self):
		users = MatchmakingUser.objects.all()[:2]
		user_channel_names = []
		for user in users:
			user_channel_names.append(user.channel_name)
		users.delete()
		return user_channel_names


	async def matchmaking_success(self, event):
		# Gestionnaire de message pour le type "matchmaking.success"
		room_name = event['room_name']
		await self.send(text_data=json.dumps({
			"type": "match_found",
			"room_name": room_name
		}))

