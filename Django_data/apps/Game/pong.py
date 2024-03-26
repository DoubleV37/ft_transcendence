# import pygame
import random
import math

# def display_game(Pong, screen):
#     screen.fill("black")
#     pygame.draw.rect(screen, "white", (598, 0, 4, 900))
#     pygame.draw.rect(screen, "white", (40, Pong.player_pos[0] - (Pong.player_size[0] / 2), 10, Pong.player_size[0]))
#     pygame.draw.rect(screen, "white", (1150, Pong.player_pos[1] - (Pong.player_size[1] / 2), 10, Pong.player_size[1]))
#     pygame.draw.circle(screen, "white", (Pong.ball_pos[0], Pong.ball_pos[1]), 12)
#     pygame.display.flip()


def ai_brain( Pong, player, lvl ):

	lvl = random.randint( -lvl, lvl )
	speedx = Pong.ball_speed[0]
	speedy = Pong.ball_speed[1]
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

	def __init__(self, start, point_limit, difficulty):
		self.running = True
		self.point = [0, 0]
		self.point_limit = point_limit
		self.player_pos = [450, 450]
		self.player_size = [100, 450]
		self.player_speed = 30
		self.paddle_radius = difficulty
		self.ball_acceleration = 0.05
		if start == 1:
			self.ball_speed = [3, random.uniform(-1, 1)]
			self.ball_pos = [100, 450]
		else:
			self.ball_speed = [-3, random.uniform(-1, 1)]
			self.ball_pos = [1100, 450]
		# powerup
		self.powerup = True
		self.powerup_size = 50
		self.powerup_time = 5 * 240
		self.powerup_pos = [575, -50]
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
		if self.powerup_time > 0:
			self.powerup_time -= 1
			if self.powerup_time == 10 * 240:
				self.player_size[0] = 100
				self.player_size[1] = 100
		else:
			seld.powerup_speed = 2
			if self.powerup_pos[1] > 950:
				self.powerup_pos[1] = -50
				self.powerup_time = 15 * 240
				self.powerup_speed = 0
			elif self.powerup_pos[0] < self.ball_pos[0] < self.powerup_pos[0] + self.powerup_size and self.powerup_pos[1] < self.ball_pos[1] < self.powerup_pos[1] + self.powerup_size:
				self.powerup_pos[1] = -50
				self.powerup_time = 15 * 240
				self.powerup_speed = 0
				if self.ball_speed[0] > 0:
					self.powerup_count[0] += 1
					self.player_size[0] = 150
					self.player_size[1] = 80
				else:
					self.powerup_count[1] += 1
					self.player_size[0] = 80
					self.player_size[1] = 150

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
		if player == 1:
			self.ball_pos = [100, 450]
			self.ball_speed = [3, random.uniform(-1, 1)]
		else:
			self.ball_pos = [1100, 450]
			self.ball_speed = [-3, random.uniform(-1, 1)]
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
				self.ball_speed[1] = (self.ball_pos[1] - self.player_pos[0]) / self.paddle_radius
		else:
			if 1145 < self.ball_pos[0] < (1145 + ( 2 * self.ball_speed[0])) and self.player_pos[1] - (self.player_size[1] / 2 + 5) < self.ball_pos[1] < self.player_pos[1] + (self.player_size[1] / 2 + 5):
				self.ball_speed[0] *= -(1 + self.ball_acceleration)
				self.ball_speed[1] = (self.ball_pos[1] - self.player_pos[1]) / self.paddle_radius
		self.stats(player)

	def ball_walk(self):
		self.ball_pos[0] += self.ball_speed[0]
		self.ball_pos[1] += self.ball_speed[1]

#     def run(self):
#         # pygame.init()
#         # screen = pygame.display.set_mode((1200, 900))
#         # clock = pygame.time.Clock()
#         # pygame.display.set_caption("PONG")
#         while self.running:
#             # pygame move #
#             keys = pygame.key.get_pressed()
#             if self.point[0] == self.point_limit or self.point[1] == self.point_limit or keys[pygame.K_ESCAPE]:
#                 self.running = False
#                 self.print_stats()
#             if keys[pygame.K_UP] and self.player_pos[1] > 0:
#                 self.player_pos[1] -= self.player_speed
#             elif keys[pygame.K_DOWN] and self.player_pos[1] < 900:
#                 self.player_pos[1] += self.player_speed

#             # ia move
#             self.player_pos[0] = ai_brain(self, 1, 20)
#             self.player_pos[1] = ai_brain(self, 2, 20)
#             # ball move
#             self.ball_walk()
#             # paddle bounce
#             if self.ball_pos[0] < 60 and self.ball_speed[0] < 0:
#                 self.paddle_bounce(0)
#             elif self.ball_pos[0] > 1140 and self.ball_speed[0] > 0:
#                 self.paddle_bounce(1)
#             # wall bounce
#             if self.ball_pos[1] < 5 and self.ball_speed[1] < 0 or self.ball_pos[1] > 895 and self.ball_speed[1] > 0:
#                 self.ball_speed[1] *= -1
#                 self.ball_bonce += 1
#             # point
#             if self.ball_pos[0] > 1200:
#                 self.update_score(0)
#             if self.ball_pos[0] < 0:
#                 self.update_score(1)
#             # pygame display #
#             display_game(self, screen)
#             clock.tick(240)
#         pygame.quit()


# def main():
#     game = Pong(1, 2, 10)
#     game.run()


# if __name__ == "__main__":
#     main()
