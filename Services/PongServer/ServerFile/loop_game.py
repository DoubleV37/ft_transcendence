import asyncio, json, time, websockets

from pong import Pong
from db_game import save_db, get_user_info, set_ingame_status
from global_var import GAMES

# =======  game  =======

async def send_opponent_info(game_id):
	print("==Send opponent info==")
	user1 = await get_user_info(GAMES[game_id]["players"][0][0])
	user2 = await get_user_info(GAMES[game_id]["players"][1][0])
	GAMES[game_id]["player_1"] = user1
	GAMES[game_id]["player_2"] = user2
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
	GAMES[game_id]["nb_players"] = 19
	await send_opponent_info(game_id)
	pong.running = True
	loop = time.time()
	print("===Game started===")
	print(pong.powerup)
	while pong.running:
		loop += 1 / 240
		pong.ball_walk()
		pong.powerup_run()
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
	await save_db(game_id, pong)
	await send_game_finish(game_id, pong)
	print("===Game finished===")

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
	try:
		for player in GAMES[game_id]["players"]:
			await player[1].send(json.dumps(data))
	except websockets.exceptions.ConnectionClosed:
		pong.running = False

async def send_game_finish(game_id, pong):
	if len(GAMES[game_id]["players"]) == 2:
		if pong.point[0] > pong.point[1]:
			await GAMES[game_id]["players"][0][1].send(json.dumps({"message" : "lose"}))
			await GAMES[game_id]["players"][1][1].send(json.dumps({"message" : "win"}))
		else:
			await GAMES[game_id]["players"][0][1].send(json.dumps({"message" : "win"}))
			await GAMES[game_id]["players"][1][1].send(json.dumps({"message" : "lose"}))
	else :
		await GAMES[game_id]["players"][0][1].send(json.dumps({"message" : "Game stopped"}))
