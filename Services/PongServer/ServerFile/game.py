import asyncio, websockets, jwt, json, psycopg2
from http.cookies import SimpleCookie
from decouple import config
from configparser import ConfigParser

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
				# await save_game_db(game_id)
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

# =======  db  =======

async def take_conf_db():
	print("==Take config DB==")
	config_db = {}
	config_db["host"] = config("POSTGRES_HOST")
	config_db["database"] = config("POSTGRES_DB")
	config_db["user"] = config("PGUSER")
	config_db["password"] = config("POSTGRES_PASSWORD")
	config_db["port"] = config("POSTGRES_PORT")
	return config_db

async def connect_db(config_db):
	print("==Connect DB==")
	conn = None
	try:
		# connect to the PostgreSQL server
		print('Connecting to the PostgreSQL database...')
		conn = psycopg2.connect(**config_db)
		print('Connected')
		return conn
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

async def save_game_db(game_id):
	print("==Save game DB==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	cur.execute("SELECT * FROM \"Game_games\"")
	rows = cur.fetchall()
	print("The number of parts: ", cur.rowcount)
	for row in rows:
		print(row)
	cur.execute("INSERT INTO \"Game_games\" \
		(\"idGame\", \"nb_users\", \"running\", \"date\", \"duration\", \"pwr_up\", \"nb_rounds\", \"in_tournament\", \"bounce\", \"max_exchange\") \
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
		(game_id, 2, True, "2021-09-01 00:00:00", 0, False, 0, False, 0, 0))
	print("==Game saved==")
	conn.commit()
	cur.close()
	conn.close()

