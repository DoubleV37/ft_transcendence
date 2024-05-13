import asyncio, websockets, jwt, json, hashlib, random
from http.cookies import SimpleCookie
from decouple import config

CONNECTIONS = dict()

async def matchmaking_handler(websocket, path):
	print(path)
	waiting = False
	while True:
		try:
			if not waiting:
				message = await websocket.recv()
				data = json.loads(message)
				type_msg = data.get("message")
				if (type_msg == "settings"):
					await register(websocket, data)
					waiting = True
					found, group = check_group(websocket)
					if found:
						print(group)
						room_name = generate_room_name(group)
						for ws in group:
							await ws[0].send(json.dumps(group[0][1]["data"]))
							await ws[0].send(json.dumps({"message" : "match_found", "room_name" : room_name}))
			if waiting:
				message = await websocket.recv()
		except websockets.exceptions.ConnectionClosed:
			del CONNECTIONS[websocket]
			break

def generate_room_name(group):
		user1 = group[0][1]["user"]
		user2 = group[1][1]["user"]
		game_name = "Pong"

		random_str = "".join(
			random.choices(
				"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=6)
		)

		room_name = hashlib.sha256(
			f"{user1}_{user2}_{game_name}_{random_str}".encode()
		).hexdigest()
		return room_name

def check_group(websocket):
	if len(CONNECTIONS) < 2:
		return False, None
	if CONNECTIONS[websocket]["data"]["type_game"] == "all":
		group = [(websocket, CONNECTIONS[websocket])]
		for ws in CONNECTIONS:
			if ws != websocket:
				group.insert(0, (ws, CONNECTIONS[ws]))
				break
		return True, group
	elif CONNECTIONS[websocket]["data"]["type_game"] == "custom":
		group = [(websocket, CONNECTIONS[websocket])]
		for ws in CONNECTIONS:
			if ws != websocket:
				if (CONNECTIONS[ws]["data"] == CONNECTIONS[websocket]["data"] and ws != websocket) or (CONNECTIONS[ws]["data"]["type_game"] == "all" and ws != websocket) :
					group.append((ws, CONNECTIONS[ws]))
					break
		if len(group) == 2:
			return True, group
	return False, None

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
