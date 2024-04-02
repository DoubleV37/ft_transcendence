import json , asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .pong import Pong
from channels.auth import login

class MultiPongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'game_%s' % self.room_name
		login(self.scope , self.scope["user"])

		try:
			game = Games.objects.get(idGame=self.room_name)
			self.user_num = 2
		except Games.DoesNotExist:
			game = Games.objects.create(idGame=self.room_name)
			self.user_num = 1
			self.pong = Pong(1 , 2 , 10)

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		await self.accept()

		UserGame.objects.get_or_create(user=self.scope['user'], game=game)


	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName,
			self.channel_name
		)


	async def receive(self, text_data):
		data = json.loads(text_data)
		message = data["message"]
		username = data["username"]
		if username != self.scope["user"].username:
			return
		if self.user_num == 1:
			if message == "up":
				self.pong.player_pos[1] = self.pong.player_pos[1] - self.pong.player_speed
			elif message == "down":
				self.pong.player_pos[1] = self.pong.player_pos[1] + self.pong.player_speed
			elif message == "start":
				start_num = Games.objects.get(idGame=self.room_name).start_num
				Games.objects.filter(idGame=self.room_name).update(start_num=start_num+1)
				if Games.objects.get(idGame=self.room_name).start_num == 2:
					asyncio.create_task(self.runGame())
		else:
			if message == "up":
				self.pong.player_pos[0] = self.pong.player_pos[0] - self.pong.player_speed
			elif message == "down":
				self.pong.player_pos[0] = self.pong.player_pos[0] + self.pong.player_speed
			elif message == "start":
				start_num = Games.objects.get(idGame=self.room_name).start_num
				Games.objects.filter(idGame=self.room_name).update(start_num=start_num+1)

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



