import asyncio, websockets, jwt, json, psycopg2, time, pytz
from datetime import datetime
from http.cookies import SimpleCookie
from decouple import config
from configparser import ConfigParser

from pong import Pong

CONNECTIONS_GAMES = dict()
# ws : game_id (int)

GAMES = dict()
# game_id (int) : {"players" : [(username,websocket), (username, websocket)], "settings" : dict, "nb_players" : int, "pong" : Pong}

async def game_handler(websocket, game_id):
	print("==Game started==")
	try:
		await register_game(websocket, game_id)
		if GAMES[game_id]["players"][0][1] == websocket:
			num = 1
		else:
			num = 2
		while True:
			message = await websocket.recv()
			message = json.loads(message)
			type_msg = message.get("message")
			if type_msg == "settings" and GAMES[game_id]["settings"] == None:
				GAMES[game_id]["settings"] = message
				GAMES[game_id]["pong"] = Pong(GAMES[game_id]["settings"]["point_limit"], GAMES[game_id]["settings"]["difficulty"], GAMES[game_id]["settings"]["powerup"])
				asyncio.create_task(game_routine(game_id, GAMES[game_id]["pong"]))
			if type_msg == "up":
				GAMES[game_id]["pong"].player_pos[num - 1] -= GAMES[game_id]["pong"].player_speed
			if type_msg == "down":
				GAMES[game_id]["pong"].player_pos[num - 1] += GAMES[game_id]["pong"].player_speed
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

# =======  game  =======


async def send_opponent_info(game_id):
	print("==Send opponent info==")
	user1 = await get_user_info(GAMES[game_id]["players"][0][0])
	user2 = await get_user_info(GAMES[game_id]["players"][1][0])
	await set_ingame_status(user1[3], True)
	await set_ingame_status(user2[3], True)
	send1 = {
		"message": "opponent",
		"num": 1,
		"opponent_name": user2[3],
		"opponent_paddle": user2[13],
		"opponent_avatar": "/avatars/" + user2[6],
		"my_name": user1[3],
		"my_avatar": "/avatars/" + user1[6],
		"my_ball": user1[12],
		"my_paddle": user1[13],
		"my_background": user1[14],
	}
	send2 = {
		"message": "opponent",
		"num": 2,
		"opponent_name": user1[3],
		"opponent_paddle": user1[13],
		"opponent_avatar":"/avatars/" + user1[6],
		"my_name": user2[3],
		"my_avatar": "/avatars/" + user2[6],
		"my_ball": user2[12],
		"my_paddle": user2[13],
		"my_background": user2[14],
	}
	await GAMES[game_id]["players"][0][1].send(json.dumps(send1))
	await GAMES[game_id]["players"][1][1].send(json.dumps(send2))


async def game_routine(game_id, pong):
	print("===Game routine===")
	while len(GAMES[game_id]["players"]) < 2:
		print("==Waiting for player==")
		await asyncio.sleep(1)
	await send_opponent_info(game_id)
	pong.running = True
	loop = time.time()
	print("===Game started===")
	print(pong.point_limit)
	while pong.running:
		loop += 1 / 240
		pong.ball_walk()
		if pong.ball_pos[0] < 60 and pong.ball_speed[0] < 0:
			pong.paddle_bounce(0)
		elif pong.ball_pos[0] > 1140 and pong.ball_speed[0] > 0:
			pong.paddle_bounce(1)
		if (pong.ball_pos[1] < 5 and pong.ball_speed[1] < 0
			or pong.ball_pos[1] > 895 and pong.ball_speed[1] > 0):
			pong.ball_speed[1] *= -1
			pong.ball_bonce += 1
		if pong.ball_pos[0] > 1200:
			pong.update_score(0)
		if pong.ball_pos[0] < 0:
			pong.update_score(1)
		await send_update_game(game_id, pong)
		await asyncio.sleep(loop - time.time())
	print(pong.point[0], pong.point[1])
	print("===Game finished===")
	await save_db(game_id, pong)
	await send_game_finish(game_id, pong)

async def send_update_game(game_id, pong):
	data = {
				"message": "game_state",
				"paddleL": pong.player_pos[0] / 900,
				"paddleR": pong.player_pos[1] / 900,
				"paddle1size": pong.player_size[0] / 900,
				"paddle2size": pong.player_size[1] / 900,
				"ballX": pong.ball_pos[0] / 1200,
				"ballY": pong.ball_pos[1] / 900,
				"ballspeedX": pong.ball_speed[0],
				"ballspeedY": pong.ball_speed[1],
				"ballsize": pong.ball_size / 900,
				"score1": pong.point[0],
				"score2": pong.point[1],
				"powerupY": pong.powerup_pos[1] / 900,
				"powerupsize": pong.powerup_size / 900,
				"time": pong.time,
            }
	for player in GAMES[game_id]["players"]:
		await player[1].send(json.dumps(data))

async def send_game_finish(game_id, pong):
	if pong.point[0] > pong.point[1]:
		await GAMES[game_id]["players"][0][1].send(json.dumps({"message" : "lose"}))
		await GAMES[game_id]["players"][1][1].send(json.dumps({"message" : "win"}))
	else:
		await GAMES[game_id]["players"][0][1].send(json.dumps({"message" : "win"}))
		await GAMES[game_id]["players"][1][1].send(json.dumps({"message" : "lose"}))

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

async def save_db(game_id, pong):
	print("==Save game DB==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	dict_stats = pong.print_stats()
	dtz = datetime.now(pytz.timezone('Europe/Paris'))
	cur.execute("INSERT INTO \"Game_games\" \
		(\"idGame\", \"nb_users\", \"running\", \"date\", \"duration\", \"pwr_up\", \"nb_rounds\", \"in_tournament\", \"bounce\", \"max_exchange\") \
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
		(game_id, 19, False, dtz, pong.time / 240, pong.powerup, pong.point[0] + pong.point[1], False, dict_stats["bounce"], dict_stats["max_exchange"]))
	print("==Game saved==")
	conn.commit()
	cur.execute("SELECT \"id\" FROM \"Game_games\" WHERE \"idGame\" = %s", (game_id,))
	gameid = cur.fetchone()[0]
	user1 = await get_user_info(GAMES[game_id]["players"][0][0])
	user2 = await get_user_info(GAMES[game_id]["players"][1][0])
	cur.execute("INSERT INTO \"Game_usergame\" \
		(\"game_id\", \"user_id\", \"score\", \"max_speed\", \"winner\") \
		VALUES (%s, %s, %s, %s, %s)",
		(gameid, user1[0], pong.point[1], dict_stats["max_speed"][1], pong.point[0] < pong.point[1]))
	cur.execute("INSERT INTO \"Game_usergame\" \
		(\"game_id\", \"user_id\", \"score\", \"max_speed\", \"winner\") \
		VALUES (%s, %s, %s, %s, %s)",
		(gameid, user2[0], pong.point[0], dict_stats["max_speed"][0], pong.point[0] > pong.point[1]))
	await update_global_stats(pong.point[0] > pong.point[1], user1, game_id)
	await update_global_stats(pong.point[1] > pong.point[0], user2, game_id)
	await set_ingame_status(user1[3], False)
	await set_ingame_status(user2[3], False)
	conn.commit()
	cur.close()
	conn.close()

async def update_global_stats(winner, user, game_id):
	print("==Update global stats==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	cur.execute("SELECT * FROM \"Dashboard_globalstats\" WHERE \"user_id\" = %s", (user[0],))
	row = cur.fetchone()
	if row:
		if winner:
			cur.execute("UPDATE \"Dashboard_globalstats\" SET \"victory\" = %s WHERE \"user_id\" = %s", (row[1] + 1, user[0]))
		else:
			cur.execute("UPDATE \"Dashboard_globalstats\" SET \"defeat\" = %s WHERE \"user_id\" = %s", (row[2] + 1, user[0]))
		cur.execute("UPDATE \"Dashboard_globalstats\" SET \"nb_games\" = %s WHERE \"user_id\" = %s", (row[3] + 1, user[0]))
		# if GAMES[game_id]["settings"]["in_tournament"]:
		# 	cur.execute("UPDATE \"Dashboard_globalstats\" SET \"tournaments_winned\" = %s WHERE \"user_id\" = %s", (row[4] + 1, user[0]))
		# else:
		cur.execute("UPDATE \"Dashboard_globalstats\" SET \"regular_games\" = %s WHERE \"user_id\" = %s", (row[5] + 1, user[0]))
		cur.execute("UPDATE \"Dashboard_globalstats\" SET \"win_rate\" = %s WHERE \"user_id\" = %s", ((row[1] + 1) / (row[3] + 1), user[0]))

async def get_user_info(username):
	print("==Get user info==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	cur.execute("SELECT * FROM \"Auth_user\" WHERE \"username\" = %s", (username))
	row = cur.fetchone()
	cur.close()
	conn.close()
	return row

async def set_ingame_status(username, status):
	print("==Set in game status==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	cur.execute("UPDATE \"Auth_user\" SET \"in_game\" = %s WHERE \"username\" = %s", (status, username))
	conn.commit()
	cur.close()
	conn.close()

