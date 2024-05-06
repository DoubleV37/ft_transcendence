import asyncio, websockets, jwt, json
from http.cookies import SimpleCookie
from decouple import config

GAMES = dict()

async def game_handler(websocket, game_id):
	print(game_id)
	print("==Game started==")
	while True:
		try:
			message = await websocket.recv()
			print(f"==Received message==: {message}")
		except websockets.exceptions.ConnectionClosed:
			print("==Client disconnected==")
			break
