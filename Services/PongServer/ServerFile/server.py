import asyncio, websockets, jwt, json
from http.cookies import SimpleCookie
from decouple import config

CONNECTIONS = dict()

async def register(websocket, data):
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
	CONNECTIONS[websocket] = {"user" : dict_user["username"], "data" : data}
	print("==Client connected")
	print(CONNECTIONS)

def check_group(websocket):
	if len(CONNECTIONS) < 2:
		return False
	if CONNECTIONS[websocket]["data"]["type_game"] == "all":
		pass
	elif CONNECTIONS[websocket]["data"]["type_game"] == "custom":
		pass
	return False

async def handler(websocket):
	waiting = False
	while True:
		if not waiting:
			print("==Waiting for settings")
			try:
				message = await websocket.recv()
				data = json.loads(message)
				type_msg = data.get("message")
				if (type_msg == "settings"):
					await register(websocket, data)
					waiting = True
				print(f"==Received message: {message}")
			except websockets.exceptions.ConnectionClosedError:
				break
		if waiting:
			print("==Waiting for group")
			found = check_group(websocket)
			if found:
				await websocket.send(json.dumps({"message" : "start"}))
				break
			await asyncio.sleep(1)

async def main():
	print("Server started")
	async with websockets.serve(handler, "0.0.0.0", 8765):
		# await show_time()
		await asyncio.Future()  # run forever

if __name__ == "__main__":
	asyncio.run(main())
