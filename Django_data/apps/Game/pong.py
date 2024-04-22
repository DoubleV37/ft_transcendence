import random
import math


def ai_brain( Pong, player, lvl ):

	if Pong.time % 240 != 0:
		return Pong.player_pos[player - 1]
	lvl = random.randint( -lvl, lvl )
	speedx = Pong.ball_speed[0]
	speedy = Pong.ball_speed[1]
	if speedx == 0:
		if player != Pong.engage:
			return 450
		else:
			Pong.engage = 0
			return 300
	ballx = Pong.ball_pos[0]
	bally = Pong.ball_pos[1]
	if player == 1:
		if speedx > 0:
			return 450
		while ballx > 60:
			ballx += speedx
			bally += speedy
			if 5 > bally or bally > 895:
				speedy *= -1
		return bally + lvl

	if speedx < 0:
		return 450
	while ballx < 1150:
		ballx += speedx
		bally += speedy
		if 5 > bally or bally > 895:
			speedy *= -1
	return bally + lvl


class Pong():

	def __init__(self, point_limit, difficulty, power):
		self.running = True
		self.time = 0
		self.engage = start
		self.engage_time = 1000
		self.point = [0, 0]
		self.point_limit = point_limit
		self.player_pos = [450, 450]
		self.player_size = [150, 150]
		self.player_speed = 20
		self.paddle_radius = difficulty
		self.ball_acceleration = 0.05
		if random.randint(0,1) == 0:
			self.ball_speed = [0,0]
			self.ball_pos = [80, 450]
		else:
			self.ball_speed = [0,0]
			self.ball_pos = [1120, 450]
		# powerup
		self.powerup = power
		self.powerup_size = 0
		self.powerup_time = 3*240
		self.powerup_pos = [600, 38]
		self.powerup_speed = 0
		#stats
		self.ball_max_speed = [0, 0]
		self.powerup_count = [0, 0]
		self.ball_bonce = 0
		self.max_exchange = 0
		self.exchange = 0
		self.ball_size = 10


	def powerup_run(self):
		if self.powerup == False:
			return
		self.powerup_pos[1] += self.powerup_speed
		if self.powerup_time == 0:
			if self.powerup_speed == 0:
				self.powerup_speed = 0.5
			self.powerup_size = 75

		if self.ball_speed[0] > 0 and self.powerup_time > 0:
			self.powerup_time -= 1

		if self.powerup_time == 2*240:
			self.powerup_count = [0, 0]

		if self.powerup_count == [0, 0]:
			if self.player_size[0] > 150:
				self.player_size[0] -= .5
			if self.player_size[1] > 150:
				self.player_size[1] -= .5
		else :
			if self.player_size[0] < 300 and self.powerup_count[0] == 1:
				self.player_size[0] += 1
			elif self.player_size[1] < 300 and self.powerup_count[1] == 1:
				self.player_size[1] += 1

		if self.powerup_pos[1] > (900 - (self.powerup_size / 2)) or self.powerup_pos[1] < (self.powerup_size / 2):
			self.powerup_speed *= -1
		elif (self.powerup_pos[0] - (self.powerup_size / 2)) < self.ball_pos[0] and self.ball_pos[0] < (self.powerup_pos[0] + (self.powerup_size / 2)) and (self.powerup_pos[1] - (self.powerup_size / 2)) < self.ball_pos[1] and self.ball_pos[1] < (self.powerup_pos[1] + (self.powerup_size / 2)):
			self.powerup_pos[1] = self.powerup_size / 2
			self.powerup_speed = 0
			self.powerup_time = 5 * 240
			self.powerup_size = 0
			if self.ball_speed[0] > 0:
				self.powerup_count[0] = 1
			else:
				self.powerup_count[1] = 1


	def stats(self, player):
		self.exchange += 1
		self.ball_bonce += 1
		speed = math.sqrt( self.ball_speed[0] ** 2 + self.ball_speed[1] ** 2 )
		if speed > self.ball_max_speed[player]:
			self.ball_max_speed[player] = speed


	def update_score(self, player):
		self.point[player] += 1
		if self.point[player] == self.point_limit:
			self.running = False
			# self.print_stats()
		self.player_pos[0] = 450
		self.player_pos[1] = 450
		self.engage_time = self.time + 1000
		if player == 1:
			self.ball_pos = [80, 450]
			self.ball_speed = [0,0]
			self.engage = 1
		else:
			self.ball_pos = [1120, 450]
			self.ball_speed = [0,0]
			self.engage = 2
		if self.exchange > self.max_exchange:
			self.max_exchange = self.exchange
		self.exchange = 0

	def print_stats(self):
		if self.point[0] > self.point[1]:
			print("\nPlayer 1 WINS\n")
		else:
			print("\nPlayer 2 WINS\n")
		print("score: ", self.point[0], " - ", self.point[1])
		print("max speed: ", round(self.ball_max_speed[0] * 10, 1), " - ", round(self.ball_max_speed[1] * 10, 1))
		print("bounce: ", self.ball_bonce)
		print("max exchange: ", self.max_exchange)


	def paddle_bounce(self, player):
		if player == 0:
			if 55 > self.ball_pos[0] > (55 + ( 2 * self.ball_speed[0])) and self.player_pos[0] - (self.player_size[0] / 2 + 5) < self.ball_pos[1] < self.player_pos[0] + (self.player_size[0] / 2 + 5):
				self.ball_speed[0] *= -(1 + self.ball_acceleration)
				if self.ball_speed[0] > 30:
					self.ball_speed[0] = 30
				self.ball_speed[1] = (self.ball_pos[1] - self.player_pos[0]) / self.paddle_radius
		else:
			if 1145 < self.ball_pos[0] < (1145 + ( 2 * self.ball_speed[0])) and self.player_pos[1] - (self.player_size[1] / 2 + 5) < self.ball_pos[1] < self.player_pos[1] + (self.player_size[1] / 2 + 5):
				self.ball_speed[0] *= -(1 + self.ball_acceleration)
				if self.ball_speed[0] < -30:
					self.ball_speed[0] = -30
				self.ball_speed[1] = (self.ball_pos[1] - self.player_pos[1]) / self.paddle_radius
		self.stats(player)

	def ball_walk(self):
		self.time += 1
		if self.ball_speed == [0,0] and self.engage_time < self.time:
			self.engage = 0
		if self.engage == 1:
			self.ball_pos[1] = self.player_pos[0]
		elif self.engage == 2:
			self.ball_pos[1] = self.player_pos[1]
		elif self.engage == 0 and self.ball_speed == [0,0]:
			if self.ball_pos[0] < 600:
				self.ball_speed = [ 3, ((self.player_pos[0] - 450) / 100)* -1 ]
			else:
				self.ball_speed = [ -3, ((self.player_pos[1] - 450) / 100* -1) ]
		self.ball_pos[0] += self.ball_speed[0]
		self.ball_pos[1] += self.ball_speed[1]
