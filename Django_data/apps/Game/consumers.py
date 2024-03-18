import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PongConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.roomGroupName = "pong_game"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
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

	async def sendMessage(self , paddleR , paddleL , ballX , ballY):
		await self.send(text_data = json.dumps({"paddleR" : paddleR , "paddleL" : paddleL , "ballX" : ballX , "ballY" : ballY , "type" : "sendMessage"}))
