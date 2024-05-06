import asyncio, websockets, jwt, json
from http.cookies import SimpleCookie
from decouple import config

CONNECTIONS_GAMES = dict()
# ws : game_id (int)

GAMES = dict()
# game_id (int) : {"players" : [(username,websocket), (username, websocket)], "settings" : dict, "nb_players" : int}

async def game_handler(websocket, game_id):
	print("==Game started==")
	try:
		await register_game(websocket, game_id)
		while True:
			message = await websocket.recv()
			message = json.loads(message)
			type_msg = message.get("message")
			if type_msg == "settings" and GAMES[game_id]["settings"] == None:
				GAMES[game_id]["settings"] = message
				print("==Settings received==")
			elif type_msg == "game":
				for player in GAMES[game_id]["players"]:
					if player[1] != websocket:
						await player[1].send(json.dumps(message))
			print(f"==Received message==: {message}")
			await websocket.ping()
	except websockets.exceptions.ConnectionClosed:
		print("==Client disconnected==")
		if game_id in GAMES:
			for player in GAMES[game_id]["players"]:
				if player[1] == websocket:
					GAMES[game_id]["players"].remove(player)
					break
			if len(GAMES[game_id]["players"]) == 0 and GAMES[game_id]["nb_players"] == 2:
				del GAMES[game_id]
				print("==Game deleted==")
			elif len(GAMES[game_id]["players"]) == 1 and GAMES[game_id]["nb_players"] == 2:
				await GAMES[game_id]["players"][0][1].send(json.dumps({"message" : "Game stopped"}))
		if websocket in CONNECTIONS_GAMES:
			print("++++++DELETE++++++")
			del CONNECTIONS_GAMES[websocket]

async def register_game(websocket, game_id):
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
	CONNECTIONS_GAMES[websocket] = game_id
	if game_id in GAMES:
		await websocket.ping()
		if GAMES[game_id]["nb_players"] == 1 and len(GAMES[game_id]["players"]) == 0:
			await websocket.send(json.dumps({"message" : "Game stopped"}))
			return
		if GAMES[game_id]["nb_players"] == 2:
			await websocket.send(json.dumps({"message" : "Game full"}))
			return
		GAMES[game_id]["players"].append((dict_user["username"], websocket))
		GAMES[game_id]["nb_players"] += 1
		print("==Player added==")
	else:
		await websocket.ping()
		GAMES[game_id] = {"players" : [(dict_user["username"], websocket)], "settings" : None, "nb_players" : 1}
		print("==Game created==" + str(game_id))
	print("==Client connected==")
