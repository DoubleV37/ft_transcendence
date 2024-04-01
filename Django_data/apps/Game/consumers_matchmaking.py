from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from .models import MatchmakingUser

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

	@database_sync_to_async
	def add_to_matchmaking_pool(self):
		MatchmakingUser.objects.create(channel_name=self.channel_name)

	@database_sync_to_async
	def remove_from_matchmaking_pool(self):
		MatchmakingUser.objects.filter(channel_name=self.channel_name).delete()

	@database_sync_to_async
	def len_pool(self):
		return MatchmakingUser.objects.count()

	@database_sync_to_async
	def get_pool_members(self):
		users = MatchmakingUser.objects.all()
		user_channel_names = []
		while len(user_channel_names) < 2:
			user = users.first()
			user_channel_names.append(users[0].channel_name)
			user.delete()
		return user_channel_names


	async def matchmaking_success(self, event):
		# Gestionnaire de message pour le type "matchmaking.success"
		room_name = event['room_name']
		await self.send(text_data=json.dumps({
			"type": "match_found",
			"room_name": room_name
		}))
