import json, asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .pong import Pong, ai_brain

class PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.roomGroupName = "pong_game"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
		self.pong = Pong(1 , 2 , 10)
		await self.runGame()
		self.paddleL = 0.5
		self.paddleR = 0.5
		self.ballX = 0.5
		self.ballY = 0.5

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
			self.paddleL = self.paddleL - 0.1
		elif message == "down":
			self.paddleL = self.paddleL + 0.1
		await self.sendMessage(self.paddleR , self.paddleL , self.ballX , self.ballY)

	async def sendMessage(self , paddleL , paddleR , ballX , ballY):
		await self.send(text_data = json.dumps({"paddleL" : paddleL , "paddleR" : paddleR , "ballX" : ballX , "ballY" : ballY , "type" : "sendMessage"}))

	async def runGame(self):
		while self.pong.running:
			# ia move
			self.pong.player_pos[0] = ai_brain(self.pong, 1, 20)
			self.pong.player_pos[1] = ai_brain(self.pong, 2, 20)
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
			await self.sendMessage(self.pong.player_pos[0]/900 , self.pong.player_pos[1]/900 , self.pong.ball_pos[0]/1200 , self.pong.ball_pos[1]/900)
			await asyncio.sleep(1/240)
			# pygame display #
			# display_game(self, screen)
			# clock.tick(240)
