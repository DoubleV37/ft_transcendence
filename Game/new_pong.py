import pygame
import random
import math
import json
import time

def widow(data, screen, clock, ball_old_pos):
    screen.fill("black")
    pygame.draw.rect(screen, "white", (598, 0, 4, 900))
    pygame.draw.rect(screen, "white", (40, data["lplayer_pos"] - (data["lplayer_size"] / 2), 10, data["lplayer_size"]))
    pygame.draw.rect(screen, "white", (1150, data["rplayer_pos"] - (data["rplayer_size"] / 2), 10, data["rplayer_size"]))
    pygame.draw.circle(screen, "white", data["ball_pos"], 10)
    ball_old_pos.append(data["ball_pos"])
    if len(ball_old_pos) > 30:
        ball_old_pos.pop(0)
    raptici = 0
    for i in range(1, len(ball_old_pos)):
        raptici += 12/30 
        pygame.draw.circle(screen, "white", ball_old_pos[i], raptici)
    pygame.display.flip()


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

# def print_stat():
#     if point[0] > point[1]:
#         print("\nPlayer 1 WINS\n")
#     else:
#         print("\nPlayer 2 WINS\n")
#     print("score: ", point[0], " - ", point[1])
#     print("max speed: ", round(ball_max_speed[0] * 10, 1), " - ", round(ball_max_speed[1] * 10, 1))
#     print("bounce: ", ball_bonce)
#     print("max exchange: ", max_exchange)


class Pong():

    def __init__(self, start, point_limit):
        self.point_limit = point_limit
        self.lplayer_pos = 450
        self.lplayer_size = 100
        self.rplayer_pos = 450
        self.rplayer_size = 100
        self.player_speed = 3
        if start == 1:
            self.ball_speed = [3, random.uniform(-1, 1)]
            self.ball_pos = [100, 450]
        else:
            self.ball_speed = [-3, random.uniform(-1, 1)]
            self.ball_pos = [1100, 450]


def main():

# Global settings
    point_limit = 10
    paddle_height = 100
    paddle_speed = 3
    ball_acceleration = 0.2
    paddle_radius = 8
    IA_lvl = 20

    running = True
    lplayer_pos = 450
    point = [0, 0]
    ball_max_speed = [0, 0]
    ball_bonce = 0
    max_exchange = 0
    exchange = 0
    rplayer_pos = 450
    IA_target = 450
    IA_counter = 0
    ball_speed = pygame.Vector2( [3, random.uniform(-1, 1)] )
    ball_pos = pygame.Vector2( 50, 450)

    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    clock = pygame.time.Clock()
    pygame.display.set_caption("PONG")

    for_json = {}
    for_json["running"] = True
    for_json["point"] = [0, 0]
    for_json["lplayer_pos"] = lplayer_pos
    for_json["lplayer_size"] = paddle_height
    for_json["rplayer_pos"] = rplayer_pos
    for_json["rplayer_size"] = paddle_height
    for_json["player_speed"] = paddle_speed
    for_json["ball_pos"] = ball_pos
    for_json["ball_speed"] = ball_speed

    ball_old_pos = []
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print_stat()

        keys = pygame.key.get_pressed()

        if point[0] == point_limit or point[1] == point_limit or keys[pygame.K_ESCAPE]:
            running = False
            print_stat()
        
        if keys[pygame.K_UP] and rplayer_pos > 0:
            rplayer_pos -= paddle_speed

        elif keys[pygame.K_DOWN] and rplayer_pos < 900:
            rplayer_pos += paddle_speed

        # ball move
        ball_pos += ball_speed

        if 55 > ball_pos.x > (55 + ( 2 * ball_speed.x)) and ball_speed.x < 0 and lplayer_pos - (paddle_height / 2 + 5) < ball_pos.y < lplayer_pos + (paddle_height / 2 + 5):
            ball_speed.x *= -1
            ball_speed.x += ball_acceleration
            ball_speed.y = (ball_pos.y - lplayer_pos) / paddle_radius
            IA_random = random.randint( -IA_lvl, IA_lvl )
            exchange += 1
            ball_bonce += 1
            if math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 ) > ball_max_speed[0]:
                ball_max_speed[0] = math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 )

        elif 1145 < ball_pos.x < (1145 + ( 2 * ball_speed.x)) and ball_speed.x > 0 and rplayer_pos - (paddle_height / 2 + 5) < ball_pos.y < rplayer_pos + (paddle_height / 2 + 5):
            ball_speed.x *= -1
            ball_speed.x -= ball_acceleration
            ball_speed.y = (ball_pos.y - rplayer_pos) / paddle_radius
            IA_random = random.randint( -IA_lvl, IA_lvl )
            exchange += 1
            ball_bonce += 1
            if math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 ) > ball_max_speed[1]:
                ball_max_speed[1] = math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 )

        if ball_pos.y < 5 and ball_speed.y < 0 or ball_pos.y > 895 and ball_speed.y > 0:
            ball_speed.y *= -1
            ball_bonce += 1
        
        if ball_pos.x > 1200:
            ball_pos = pygame.Vector2( 1200 - 50, 450 )
            ball_speed = pygame.Vector2(-3, random.uniform(-1, 1))
            lplayer_pos = 450
            rplayer_pos = 450
            point[0] += 1
            print(f"{point[0]} IA | Player {point[1]}")
            screen.fill("black")
            if exchange > max_exchange:
                max_exchange = exchange
            exchange = 0
            pygame.time.delay(500)

        if ball_pos.x < 0:
            ball_pos = pygame.Vector2( 50, 450 )
            ball_speed = pygame.Vector2(3, random.uniform(-1, 1))
            lplayer_pos = 450
            rplayer_pos = 450
            point[1] += 1
            print(f"{point[0]} IA | Player {point[1]}")
            screen.fill("black")
            if exchange > max_exchange:
                max_exchange = exchange
            exchange = 0
            pygame.time.delay(500)

        # IA move

        if IA_counter == 0:
            IA_target = path_estimation( 1, ball_pos.copy(), ball_speed.copy(), IA_lvl )

        IA_counter += 1

        if IA_counter > 240:
            IA_counter = 0
        
        lplayer_pos = paddle_move( lplayer_pos, IA_target, paddle_speed )

        # pygame.display.flip()
        for_json["lplayer_pos"] = lplayer_pos
        for_json["rplayer_pos"] = rplayer_pos
        for_json["ball_pos"] = ball_pos

        widow(for_json, screen, clock, ball_old_pos)

        clock.tick(240) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
