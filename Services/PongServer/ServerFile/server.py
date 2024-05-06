import asyncio, websockets

from matchmaking import matchmaking_handler
from game import game_handler

async def handler(websocket, path):
	if path == "/ws/multi/matchmaking/":
		await matchmaking_handler(websocket, path)
	elif path.startswith("/ws/multi/game/"):
		print(path)
		game_id = path.split("/")[-2]
		await game_handler(websocket, game_id)
	else:
		await websocket.send("Invalid path")

async def main():
	print("Server started")
	async with websockets.serve(handler, "0.0.0.0", 8765):
		await asyncio.Future()  # run forever

if __name__ == "__main__":
	asyncio.run(main())
