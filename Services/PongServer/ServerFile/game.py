import asyncio, websockets, jwt, json
from http.cookies import SimpleCookie
from decouple import config

from pong import Pong
from db_game import *
from loop_game import game_routine
from global_var import GAMES, CONNECTIONS_GAMES


async def game_handler(websocket, game_id):
	print("==Game started==")
	try:
		state = await register_game(websocket, game_id)
		if not state:
			return
		if GAMES[game_id]["players"][0][1] == websocket:
			num = 1
		else:
			num = 2
		while True:
			message = await websocket.recv()
			message = json.loads(message)
			type_msg = message.get("message")
			if type_msg == "settings" and num == 1:
				GAMES[game_id]["settings"] = message
				GAMES[game_id]["pong"] = Pong(GAMES[game_id]["settings"]["point_limit"], GAMES[game_id]["settings"]["difficulty"], GAMES[game_id]["settings"]["powerup"])
				asyncio.create_task(game_routine(game_id, GAMES[game_id]["pong"]))
			if type_msg == "up" and num == 1 and GAMES[game_id]["pong"].player_pos[1] > 0:
				GAMES[game_id]["pong"].player_pos[1] -= GAMES[game_id]["pong"].player_speed
			if type_msg == "down" and num == 1 and GAMES[game_id]["pong"].player_pos[1] < 900:
				GAMES[game_id]["pong"].player_pos[1] += GAMES[game_id]["pong"].player_speed
			if type_msg == "up" and num == 2 and GAMES[game_id]["pong"].player_pos[0] > 0:
				GAMES[game_id]["pong"].player_pos[0] -= GAMES[game_id]["pong"].player_speed
			if type_msg == "down" and num == 2 and GAMES[game_id]["pong"].player_pos[0] < 900:
				GAMES[game_id]["pong"].player_pos[0] += GAMES[game_id]["pong"].player_speed
	except websockets.exceptions.ConnectionClosed:
		print("==Client disconnected==")
		if game_id in GAMES:
			for player in GAMES[game_id]["players"]:
				if player[1] == websocket:
					GAMES[game_id]["players"].remove(player)
					GAMES[game_id]["pong"].running = False
					break
			if len(GAMES[game_id]["players"]) == 0 and GAMES[game_id]["nb_players"] == 2:
				del GAMES[game_id]
				print("==Game deleted==")
			elif len(GAMES[game_id]["players"]) == 1 and GAMES[game_id]["nb_players"] == 2:
				await GAMES[game_id]["players"][0][1].send(json.dumps({"message" : "Game stopped"}))
		if websocket in CONNECTIONS_GAMES:
			print("++++++DELETE++++++")
			del CONNECTIONS_GAMES[websocket]

# =======  connection  =======

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
		if GAMES[game_id]["nb_players"] == 2 or GAMES[game_id]["nb_players"] == 19:
			await websocket.send(json.dumps({"message" : "Game stopped"}))
			return False
		GAMES[game_id]["players"].append((dict_user["username"], websocket))
		GAMES[game_id]["nb_players"] += 1
		print("==Player added==")
	else:
		await websocket.ping()
		GAMES[game_id] = {"players" : [(dict_user["username"], websocket)], "settings" : None, "nb_players" : 1}
		print("==Game created==" + str(game_id))
	print("==Client connected==")
	return True



