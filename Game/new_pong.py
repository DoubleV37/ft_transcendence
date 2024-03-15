import pygame
import random
import math
import json
import time

def widow(Pong, screen, clock):
    screen.fill("black")
    pygame.draw.rect(screen, "white", (598, 0, 4, 900))
    pygame.draw.rect(screen, "white", (40, Pong.player_pos[0] - (Pong.player_size[0] / 2), 10, Pong.player_size[0]))
    pygame.draw.rect(screen, "white", (1150, Pong.player_pos[1] - (Pong.player_size[1] / 2), 10, Pong.player_size[1]))
    pygame.draw.circle(screen, "white", (Pong.ball_pos[0], Pong.ball_pos[1]), 12)
    pygame.display.flip()
    clock.tick(240) / 1000


def path_estimation( player, pos , speed, lvl ):

    lvl = random.randint( -lvl, lvl )
    if player == 1:
        if speed.x > 0:
            return 450
        while pos.x > 60:
            pos += speed
            if 5 > pos.y or pos.y > 895:
                speed.y *= -1
        return pos.y + lvl

    if speed.x < 0:
        return 450
    while pos.x < 1150:
        pos += speed
        if 5 > pos.y or pos.y > 895:
            speed.y *= -1
    return pos.y + lvl


def paddle_move( pos, target, speed ):
    if 0 < pos > target + speed:
        pos -= speed
    elif 900 > pos < target - speed:
        pos += speed
    return pos


class Pong():

    def __init__(self, start, point_limit, difficulty):
        self.running = True
        self.point = [0, 0]
        self.point_limit = point_limit
        self.player_pos = [450, 450]
        self.player_size = [100, 100]
        self.player_speed = 3
        self.paddle_radius = difficulty
        self.ball_acceleration = 0.05
        if start == 1:
            self.ball_speed = [3, random.uniform(-1, 1)]
            self.ball_pos = [100, 450]
        else:
            self.ball_speed = [-3, random.uniform(-1, 1)]
            self.ball_pos = [1100, 450]
        #stats
        self.ball_max_speed = [0, 0]
        self.ball_bonce = 0
        self.max_exchange = 0
        self.exchange = 0


    def stats(self, player):
        self.exchange += 1
        self.ball_bonce += 1
        speed = math.sqrt( self.ball_speed[0] ** 2 + self.ball_speed[1] ** 2 )
        if speed > self.ball_max_speed[player]:
            self.ball_max_speed[player] = speed


    def point(self, player):
        self.point[player] += 1
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


    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1200, 900))
        clock = pygame.time.Clock()
        pygame.display.set_caption("PONG")
        while self.running:
            # pygame move #
            keys = pygame.key.get_pressed()
            if self.point[0] == self.point_limit or self.point[1] == self.point_limit or keys[pygame.K_ESCAPE]:
                self.running = False
                self.print_stats()
            if keys[pygame.K_UP] and self.rplayer_pos > 0:
                self.player_pos[1] -= self.player_speed
            elif keys[pygame.K_DOWN] and self.rplayer_pos < 900:
                self.player_pos[1] += self.player_speed
            # ia move
            self.player_pos[0] = paddle_move( self.player_pos[0], path_estimation( 1, self.ball_pos.copy(), self.ball_speed.copy(), 20 ), self.player_speed )
            # ball move
            self.ball_pos[0] += self.ball_speed[0]
            self.ball_pos[1] += self.ball_speed[1]
            # paddle bounce
            if self.ball_pos[0] < 60 and self.ball_speed[0] < 0:
                self.paddle_bounce(0)
            elif self.ball_pos[0] > 1140 and self.ball_speed[0] > 0:
                self.paddle_bounce(1)
            # wall bounce
            if self.ball_pos[1] < 5 and self.ball_speed[1] < 0 or self.ball_pos[1] > 895 and self.ball_speed[1] > 0:
                self.ball_speed[1] *= -1
                self.ball_bonce += 1
            # point
            if self.ball_pos[0] > 1200:
                self.point(0)
            if self.ball_pos[0] < 0:
                self.point(1)
            # pygame display #
            widow(self, screen, clock)
        pygame.quit()
            

def main():

    game = Pong(1, 5, 10)
    game.run()

# # Global settings
#     point_limit = 10            #
#     paddle_height = 100         #
#     paddle_speed = 3            #
#     ball_acceleration = 0.05    #
#     paddle_radius = 10          #

#     running = True
#     lplayer_pos = 450 #
#     point = [0, 0] #
#     ball_max_speed = [0, 0] #
#     ball_bonce = 0     #
#     max_exchange = 0       #
#     exchange = 0        #
#     rplayer_pos = 450 #
#     IA_target = 450
#     IA_counter = 0
#     ball_speed = pygame.Vector2( [3, random.uniform(-1, 1)] ) #
#     ball_pos = pygame.Vector2( 50, 450) #

#     pygame.init()
#     screen = pygame.display.set_mode((1200, 900))
#     clock = pygame.time.Clock()
#     pygame.display.set_caption("PONG")

#     for_json = {}
#     for_json["running"] = True
#     for_json["point"] = [0, 0]
#     for_json["lplayer_pos"] = lplayer_pos
#     for_json["lplayer_size"] = paddle_height
#     for_json["rplayer_pos"] = rplayer_pos
#     for_json["rplayer_size"] = paddle_height
#     for_json["player_speed"] = paddle_speed
#     for_json["ball_pos"] = ball_pos
#     for_json["ball_speed"] = ball_speed

#     while running:

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 print_stat()

#         keys = pygame.key.get_pressed()

#         if point[0] == point_limit or point[1] == point_limit or keys[pygame.K_ESCAPE]:
#             running = False
#             print_stat()
        
#         if keys[pygame.K_UP] and rplayer_pos > 0:
#             rplayer_pos -= paddle_speed

#         elif keys[pygame.K_DOWN] and rplayer_pos < 900:
#             rplayer_pos += paddle_speed

#         # ball move
#         ball_pos += ball_speed

#         if 55 > ball_pos.x > (55 + ( 2 * ball_speed.x)) and ball_speed.x < 0 and lplayer_pos - (paddle_height / 2 + 5) < ball_pos.y < lplayer_pos + (paddle_height / 2 + 5):
#             ball_speed.x *= -(1 + ball_acceleration) 
#             ball_speed.y = (ball_pos.y - lplayer_pos) / paddle_radius

#         elif 1145 < ball_pos.x < (1145 + ( 2 * ball_speed.x)) and ball_speed.x > 0 and rplayer_pos - (paddle_height / 2 + 5) < ball_pos.y < rplayer_pos + (paddle_height / 2 + 5):
#             ball_speed.x *= -(1 + ball_acceleration)
#             ball_speed.y = (ball_pos.y - rplayer_pos) / paddle_radius

#         if ball_pos.y < 5 and ball_speed.y < 0 or ball_pos.y > 895 and ball_speed.y > 0:
#             ball_speed.y *= -1
#             ball_bonce += 1
        
#         if ball_pos.x > 1200:
#             ball_pos = pygame.Vector2( 1200 - 50, 450 )
#             ball_speed = pygame.Vector2(-3, random.uniform(-1, 1))
#             lplayer_pos = 450
#             rplayer_pos = 450
#             point[0] += 1
#             print(f"{point[0]} IA | Player {point[1]}")
#             screen.fill("black")
#             if exchange > max_exchange:
#                 max_exchange = exchange
#             exchange = 0
#             pygame.time.delay(500)

#         if ball_pos.x < 0:
#             ball_pos = pygame.Vector2( 50, 450 )
#             ball_speed = pygame.Vector2(3, random.uniform(-1, 1))
#             lplayer_pos = 450
#             rplayer_pos = 450
#             point[1] += 1
#             print(f"{point[0]} IA | Player {point[1]}")
#             screen.fill("black")
#             if exchange > max_exchange:
#                 max_exchange = exchange
#             exchange = 0
#             pygame.time.delay(500)

#         # IA move


#         if IA_counter == 0:
#             IA_target = path_estimation( 1, ball_pos.copy(), ball_speed.copy(), 20 )

#         IA_counter += 1

#         if IA_counter > 240:
#             IA_counter = 0
        
#         lplayer_pos = paddle_move( lplayer_pos, IA_target, paddle_speed )

#         # pygame.display.flip()
#         for_json["lplayer_pos"] = lplayer_pos
#         for_json["rplayer_pos"] = rplayer_pos
#         for_json["ball_pos"] = ball_pos

#         widow(for_json, screen, clock)

#         clock.tick(240) / 1000

#     pygame.quit()


if __name__ == "__main__":
    main()
