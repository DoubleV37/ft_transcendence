import pygame
import random
import math


# pygame setup
pygame.init()

window_width = 1200
window_height = 900
screen = pygame.display.set_mode((window_width, window_height))


clock = pygame.time.Clock()
pygame.display.set_caption("PONG")
running = True
dt = 0
player_pos = window_height / 2
point = [0, 0]

#rules
paddle_height = 100
paddle_width = 10
paddle_padding = 50
paddle_speed = 3
ball_start_speed = [3, random.uniform(-1, 1)]
ball_acceleration = 0.2
paddle_radius = 8
IA_lvl = 20
IA_dumb = 4

# ball move
ball_radius = 5
ball_speed = pygame.Vector2( ball_start_speed )
ball_pos = pygame.Vector2( paddle_padding, window_height / 2)
ball_old_pos = []

# IA move
IA_pos = window_height / 2
IA_target = window_height / 2
IA_counter = 0
IA_random = random.randint( -IA_lvl, IA_lvl )
IA_rand_dumb = random.randint( 0, IA_dumb )


#stats
ball_max_speed = [0, 0]
ball_bonce = 0
max_exchange = 0
exchange = 0

def path_estimation( player, pos , speed ):

    if IA_rand_dumb == 0:
        pos.x += random.choice([-paddle_padding, paddle_padding])

    if player == 1:
        if speed.x > 0:
            return window_height / 2
        while pos.x > paddle_padding + paddle_width:
            pos += speed
            if pos.y < ball_radius or pos.y > window_height - ball_radius:
                speed.y *= -1
        return pos.y + IA_random

    else:
        if speed.x < 0:
            return window_height / 2
        while pos.x < window_width - paddle_padding:
            pos += speed
            if pos.y < ball_radius or pos.y > window_height - ball_radius:
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

    if point[0] == 5 or point[1] == 5 or keys[pygame.K_ESCAPE]:
        running = False
        print_stat()
    
    if keys[pygame.K_UP] and player_pos > 0:
        player_pos -= paddle_speed

    elif keys[pygame.K_DOWN] and player_pos < window_height:
        player_pos += paddle_speed

    screen.fill("black")
    
    # draw middle line
    pygame.draw.rect(screen, "white", (window_width / 2 - 2, 0, 4, window_height))

    # draw IA
    IA = pygame.draw.rect(screen, "white", ( paddle_padding - paddle_width, IA_pos - (paddle_height / 2), paddle_width, paddle_height))

    # draw ball
    ball = pygame.draw.circle(screen, "white", ball_pos, 2 * ball_radius)

    # draw player
    player = pygame.draw.rect(screen, "white", ( window_width - paddle_padding, player_pos - (paddle_height / 2), paddle_width, paddle_height))

    # draw ball trail
    ball_old_pos.append(ball_pos.copy())
    if len(ball_old_pos) > 100:
        ball_old_pos.pop(0)
    raptici = 0
    for i in range(1, len(ball_old_pos)):
        raptici += 12/100 
        pygame.draw.circle(screen, "white", ball_old_pos[i], raptici)


    # ball move
    ball_pos += ball_speed

    if (paddle_padding + ball_radius) > ball_pos.x > ((paddle_padding + ball_radius) + ( 2 * ball_speed.x)) and ball_speed.x < 0 and IA_pos - (paddle_height / 2 + ball_radius) < ball_pos.y < IA_pos + (paddle_height / 2 + ball_radius):
        ball_speed.x *= -1
        ball_speed.x += ball_acceleration
        ball_speed.y = (ball_pos.y - IA_pos) / paddle_radius
        IA_random = random.randint( -IA_lvl, IA_lvl )
        IA_rand_dumb = random.randint( 0, IA_dumb )
        exchange += 1
        ball_bonce += 1
        if math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 ) > ball_max_speed[0]:
            ball_max_speed[0] = math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 )

    elif (window_width - paddle_padding - paddle_width + ball_radius) < ball_pos.x < ((window_width - paddle_padding - paddle_width + ball_radius) + ( 2 * ball_speed.x)) and ball_speed.x > 0 and player_pos - (paddle_height / 2 + ball_radius) < ball_pos.y < player_pos + (paddle_height / 2 + ball_radius):
        ball_speed.x *= -1
        ball_speed.x -= ball_acceleration
        ball_speed.y = (ball_pos.y - player_pos) / paddle_radius
        IA_random = random.randint( -IA_lvl, IA_lvl )
        IA_rand_dumb = random.randint( 0, IA_dumb )
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
        IA_pos = window_height / 2
        player_pos = window_height / 2
        point[0] += 1
        pygame.display.set_caption(f"{point[0]} IA | Player {point[1]}")
        screen.fill("black")
        if exchange > max_exchange:
            max_exchange = exchange
        exchange = 0
        pygame.time.delay(500)

    if ball_pos.x < 0:
        ball_pos = pygame.Vector2( paddle_padding, window_height / 2 )
        ball_speed = pygame.Vector2(3, random.uniform(-1, 1))
        IA_pos = window_height / 2
        player_pos = window_height / 2
        point[1] += 1
        pygame.display.set_caption(f"{point[0]} IA | Player {point[1]}")
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
    
    # player_pos = paddle_move( player_pos, path_estimation( 0, ball_pos.copy(), ball_speed.copy()), paddle_speed)

    IA_pos = paddle_move( IA_pos, IA_target, paddle_speed )

    pygame.display.flip()

    # dt = clock.tick(1000) / 1000
    dt = clock.tick(240) / 1000

pygame.quit()
