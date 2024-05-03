import random
import math

class Pong():

	def __init__(self, point_limit, difficulty, power):
		self.running = True
		self.time = 0
		self.engage_time = 1000
		self.point = [0, 0]
		self.point_limit = point_limit
		self.player_pos = [450, 450]
		self.player_size = [150, 150]
		self.player_speed = 20
		self.paddle_radius = 15 - difficulty
		self.ball_acceleration = 0.05
		if random.randint(0,1) == 0:
			self.engage = 1
			self.ball_speed = [0,0]
			self.ball_pos = [80, 450]
		else:
			self.engage = 2
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
		dic_stats = {
			"score1": self.point[0],
			"score2": self.point[1],
			"max_speed": [round(self.ball_max_speed[0] * 5, 1), round(self.ball_max_speed[1] * 5, 1)],
			"bounce": self.ball_bonce,
			"max_exchange": self.max_exchange
		}
		return dic_stats
		# if self.point[0] > self.point[1]:
		# 	print("\nPlayer 1 WINS\n")
		# else:
		# 	print("\nPlayer 2 WINS\n")
		# print("score: ", self.point[0], " - ", self.point[1])
		# print("max speed: ", round(self.ball_max_speed[0] * 10, 1), " - ", round(self.ball_max_speed[1] * 10, 1))
		# print("bounce: ", self.ball_bonce)
		# print("max exchange: ", self.max_exchange)

	def paddle_bounce(self, player):
		if player == 0:
			if 55 > self.ball_pos[0] > (55 + ( 2 * self.ball_speed[0])) and self.player_pos[0] - (self.player_size[0] / 2 + 10) < self.ball_pos[1] < self.player_pos[0] + (self.player_size[0] / 2 + 10):
				self.ball_speed[0] *= -(1 + self.ball_acceleration)
				if self.ball_speed[0] > 10:
					self.ball_speed[0] = 10
				self.ball_speed[1] = (self.ball_pos[1] - self.player_pos[0]) / self.paddle_radius
				self.stats(player)
		else:
			if 1145 < self.ball_pos[0] < (1145 + ( 2 * self.ball_speed[0])) and self.player_pos[1] - (self.player_size[1] / 2 + 10) < self.ball_pos[1] < self.player_pos[1] + (self.player_size[1] / 2 + 10):
				self.ball_speed[0] *= -(1 + self.ball_acceleration)
				if self.ball_speed[0] < -10:
					self.ball_speed[0] = -10
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
