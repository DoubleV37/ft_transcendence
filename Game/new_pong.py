import pygame
import random
import math
import json
import time


# Global settings
window_width = 1200
window_height = 900
point_limit = 10
paddle_height = 100
paddle_width = 10
paddle_padding = 50
paddle_speed = 3
ball_acceleration = 0.2
ball_radius = 5
paddle_radius = 8
IA_lvl = 20

pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
pygame.display.set_caption("PONG")

# Global variables

running = True
lplayer_pos = window_height / 2
point = [0, 0]
ball_max_speed = [0, 0]
ball_bonce = 0
max_exchange = 0
exchange = 0
rplayer_pos = window_height / 2
IA_target = window_height / 2
IA_counter = 0
ball_speed = pygame.Vector2( [3, random.uniform(-1, 1)] )
ball_pos = pygame.Vector2( paddle_padding, window_height / 2)
IA_random = random.randint( -IA_lvl, IA_lvl )


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
def widow(data, screen, clock):
    screen.fill("black")
    pygame.draw.rect(screen, "white", (598, 0, 4, 900))
    pygame.draw.rect(screen, "white", (40, data["lplayer_pos"] - (data["lplayer_size"] / 2), 10, data["lplayer_size"]))
    pygame.draw.rect(screen, "white", (1150, data["rplayer_pos"] - (data["rplayer_size"] / 2), 10, data["rplayer_size"]))
    pygame.draw.circle(screen, "white", data["ball_pos"], 10)
    ball_old_pos.append(ball_pos.copy())
    if len(ball_old_pos) > 30:
        ball_old_pos.pop(0)
    raptici = 0
    for i in range(1, len(ball_old_pos)):
        raptici += 12/30 
        pygame.draw.circle(screen, "white", ball_old_pos[i], raptici)
    pygame.display.flip()


def path_estimation( player, pos , speed ):

    if player == 1:
        if speed.x > 0:
            return window_height / 2
        while pos.x > paddle_padding + paddle_width:
            pos += speed
            if ball_radius > pos.y or pos.y > window_height - ball_radius:
                speed.y *= -1
        return pos.y + IA_random

    if speed.x < 0:
        return window_height / 2
    while pos.x < window_width - paddle_padding:
        pos += speed
        if ball_radius > pos.y or pos.y > window_height - ball_radius:
            speed.y *= -1
    return pos.y + IA_random


def paddle_move( pos, target, speed ):
    if 0 < pos > target + speed:
        pos -= speed
    elif window_height > pos < target - speed:
        pos += speed
    return pos

def print_stat():
    if point[0] > point[1]:
        print("\nPlayer 1 WINS\n")
    else:
        print("\nPlayer 2 WINS\n")
    print("score: ", point[0], " - ", point[1])
    print("max speed: ", round(ball_max_speed[0] * 10, 1), " - ", round(ball_max_speed[1] * 10, 1))
    print("bounce: ", ball_bonce)
    print("max exchange: ", max_exchange)

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

    elif keys[pygame.K_DOWN] and rplayer_pos < window_height:
        rplayer_pos += paddle_speed

    # ball move
    ball_pos += ball_speed

    if (paddle_padding + ball_radius) > ball_pos.x > ((paddle_padding + ball_radius) + ( 2 * ball_speed.x)) and ball_speed.x < 0 and lplayer_pos - (paddle_height / 2 + ball_radius) < ball_pos.y < lplayer_pos + (paddle_height / 2 + ball_radius):
        ball_speed.x *= -1
        ball_speed.x += ball_acceleration
        ball_speed.y = (ball_pos.y - lplayer_pos) / paddle_radius
        IA_random = random.randint( -IA_lvl, IA_lvl )
        exchange += 1
        ball_bonce += 1
        if math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 ) > ball_max_speed[0]:
            ball_max_speed[0] = math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 )

    elif (window_width - paddle_padding - paddle_width + ball_radius) < ball_pos.x < ((window_width - paddle_padding - paddle_width + ball_radius) + ( 2 * ball_speed.x)) and ball_speed.x > 0 and rplayer_pos - (paddle_height / 2 + ball_radius) < ball_pos.y < rplayer_pos + (paddle_height / 2 + ball_radius):
        ball_speed.x *= -1
        ball_speed.x -= ball_acceleration
        ball_speed.y = (ball_pos.y - rplayer_pos) / paddle_radius
        IA_random = random.randint( -IA_lvl, IA_lvl )
        exchange += 1
        ball_bonce += 1
        if math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 ) > ball_max_speed[1]:
            ball_max_speed[1] = math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 )

    if ball_pos.y < ball_radius and ball_speed.y < 0 or ball_pos.y > window_height - ball_radius and ball_speed.y > 0:
        ball_speed.y *= -1
        ball_bonce += 1
    
    if ball_pos.x > window_width:
        ball_pos = pygame.Vector2( window_width - paddle_padding, window_height / 2 )
        ball_speed = pygame.Vector2(-3, random.uniform(-1, 1))
        lplayer_pos = window_height / 2
        lplayer_pos = window_height / 2
        point[0] += 1
        print(f"{point[0]} IA | Player {point[1]}")
        screen.fill("black")
        if exchange > max_exchange:
            max_exchange = exchange
        exchange = 0
        pygame.time.delay(500)

    if ball_pos.x < 0:
        ball_pos = pygame.Vector2( paddle_padding, window_height / 2 )
        ball_speed = pygame.Vector2(3, random.uniform(-1, 1))
        lplayer_pos = window_height / 2
        lplayer_pos = window_height / 2
        point[1] += 1
        print(f"{point[0]} IA | Player {point[1]}")
        screen.fill("black")
        if exchange > max_exchange:
            max_exchange = exchange
        exchange = 0
        pygame.time.delay(500)

    # IA move

    if IA_counter == 0:
        IA_target = path_estimation( 1, ball_pos.copy(), ball_speed.copy() )

    IA_counter += 1

    if IA_counter > 240:
        IA_counter = 0
    
    lplayer_pos = paddle_move( lplayer_pos, IA_target, paddle_speed )

    # pygame.display.flip()
    for_json["lplayer_pos"] = lplayer_pos
    for_json["rplayer_pos"] = rplayer_pos
    for_json["ball_pos"] = ball_pos
    widow(for_json, screen, clock)

    clock.tick(240) / 1000

pygame.quit()
