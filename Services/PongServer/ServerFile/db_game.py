import psycopg2, pytz
from datetime import datetime
from http.cookies import SimpleCookie
from decouple import config

from pong import Pong
from global_var import GAMES

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

async def save_game_db(game_id, pong):
	print("==Save game DB==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	dict_stats = pong.print_stats()
	dtz = datetime.now(pytz.timezone('Europe/Paris'))
	cur.execute("INSERT INTO \"Game_games\" \
		(\"idGame\", \"nb_users\", \"running\", \"date\", \"duration\", \"pwr_up\", \"nb_rounds\", \"in_tournament\", \"bounce\", \"max_exchange\") \
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
		(game_id, 19, False, dtz, pong.time / 240, pong.powerup, pong.point[0] + pong.point[1], False, dict_stats["bounce"], dict_stats["max_exchange"],))
	conn.commit()
	cur.close()
	conn.close()
	print("==Game saved==")

async def save_user_game_db(gameid, user, num, pong):
	print("==Save user game DB==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	dict_stats = pong.print_stats()
	if num == 1:
		cur.execute("INSERT INTO \"Game_usergame\" \
			(\"game_id\", \"user_id\", \"score\", \"max_speed\", \"winner\") \
			VALUES (%s, %s, %s, %s, %s)",
			(gameid, user[0], pong.point[1], dict_stats["max_speed"][1], pong.point[0] < pong.point[1],))
	else:
		cur.execute("INSERT INTO \"Game_usergame\" \
			(\"game_id\", \"user_id\", \"score\", \"max_speed\", \"winner\") \
			VALUES (%s, %s, %s, %s, %s)",
			(gameid, user[0], pong.point[0], dict_stats["max_speed"][0], pong.point[0] > pong.point[1],))
	conn.commit()
	cur.close()
	conn.close()

async def save_db(game_id, pong):
	print("==Save DB==")
	user1 = GAMES[game_id]["player_1"]
	user2 = GAMES[game_id]["player_2"]
	if len(GAMES[game_id]["players"]) == 2:
		await save_game_db(game_id, pong)
		config = await take_conf_db()
		conn = await connect_db(config)
		cur = conn.cursor()
		cur.execute("SELECT \"id\" FROM \"Game_games\" WHERE \"idGame\" = %s", (game_id,))
		gameid = cur.fetchone()[0]

		await save_user_game_db(gameid, user1, 1, pong)
		await update_global_stats(pong.point[0] < pong.point[1], user1, game_id)

		await save_user_game_db(gameid, user2, 2, pong)
		await update_global_stats(pong.point[1] < pong.point[0], user2, game_id)
		conn.commit()
		cur.close()
		conn.close()

	await set_ingame_status(user1[3], False)
	await set_ingame_status(user2[3], False)


async def update_global_stats(winner, user, game_id):
	print("==Update global stats==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	cur.execute("SELECT * FROM \"Dashboard_globalstats\" WHERE \"user_id\" = %s", (user[0],))
	row = cur.fetchone()
	if row:
		print(row)
		if winner:
			cur.execute("UPDATE \"Dashboard_globalstats\" SET \"victory\" = %s WHERE \"user_id\" = %s", (row[5] + 1, user[0],))
			cur.execute("UPDATE \"Dashboard_globalstats\" SET \"win_rate\" = %s WHERE \"user_id\" = %s", ((row[5] + 1) / (row[2] + 1), user[0],))
		else:
			cur.execute("UPDATE \"Dashboard_globalstats\" SET \"defeat\" = %s WHERE \"user_id\" = %s", (row[6] + 1, user[0],))
			cur.execute("UPDATE \"Dashboard_globalstats\" SET \"win_rate\" = %s WHERE \"user_id\" = %s", ((row[5]) / (row[2] + 1), user[0],))
		cur.execute("UPDATE \"Dashboard_globalstats\" SET \"nb_games\" = %s WHERE \"user_id\" = %s", (row[2] + 1, user[0],))
		cur.execute("UPDATE \"Dashboard_globalstats\" SET \"regular_games\" = %s WHERE \"user_id\" = %s", (row[3] + 1, user[0],))
	conn.commit()
	cur.close()
	conn.close()

async def get_user_info(username):
	print("==Get user info==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	cur.execute("SELECT * FROM \"Auth_user\" WHERE \"username\" = %s", (username,))
	row = cur.fetchone()
	cur.close()
	conn.close()
	return row

async def set_ingame_status(username, status):
	print("==Set in game status==")
	config = await take_conf_db()
	conn = await connect_db(config)
	cur = conn.cursor()
	cur.execute("UPDATE \"Auth_user\" SET \"in_game\" = %s WHERE \"username\" = %s", (status, username,))
	conn.commit()
	cur.close()
	conn.close()
