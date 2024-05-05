""" server.py """
import asyncio
import websockets
import datetime
import random

async def hello(websocket):
	print("Server connected")
	name = await websocket.recv()
	print(f"<<< {name}")

	greeting = f"Hello {name}!"

	await websocket.send(greeting)
	print(f">>> {greeting}")

async def show_time(websocket):
	print("Server connected")
	while True:
		message = datetime.datetime.utcnow().isoformat() + "Z"
		await websocket.send(message)
		message = await websocket.recv()
		print(f">>> {message}")
		await asyncio.sleep(random.random() * 2 + 1)

async def main():
	print("Server started")
	async with websockets.serve(show_time, "0.0.0.0", 8765):
		await asyncio.Future()  # run forever

if __name__ == "__main__":
	asyncio.run(main())
