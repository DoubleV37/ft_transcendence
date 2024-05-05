""" server.py """
import asyncio, websockets, jwt, json
from http.cookies import SimpleCookie
from decouple import config

CONNECTIONS = dict()

async def register(websocket):
	header_cookie = websocket.request_headers.get("Cookie")
	cookie = SimpleCookie(header_cookie)
	jwtt = cookie.get("jwt_token").value
	dict_user = jwt.decode(
		jwtt,
		config("DJANGO_SECRET_KEY"),
		algorithms=config("HASH"),
		issuer=config("NAME"),
		options={"verify_signature": False}
	)
	CONNECTIONS[websocket] = dict_user["username"]
	print("==Client connected")
	print(CONNECTIONS)
	try:
		await websocket.wait_closed()
	finally:
		print("CLient disconnected")
		del CONNECTIONS[websocket]

async def handler(websocket):
	while True:
		try:
			message = await websocket.recv()
			if (message == "coucou"): # message settings
				await register(websocket)
				await websocket.send("coucou")
			print(f"==Received message: {message}")
		except websockets.exceptions.ConnectionClosedError:
			break

async def main():
	print("Server started")
	async with websockets.serve(handler, "0.0.0.0", 8765):
		# await show_time()
		await asyncio.Future()  # run forever

if __name__ == "__main__":
	asyncio.run(main())
