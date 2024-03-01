import pygame
import random
import math


def path_estimation( pos ):
    cpball = ball_pos.copy()
    cpball_speed = ball_speed.copy()
    if IA_rand_dumb == 0:
        cpball.x += random.choice([-50, 50])

    if pos == 1:
        if cpball_speed.x > 0:
            return 360
        while cpball.x > 50:
            cpball += cpball_speed
            if cpball.y < 6 or cpball.y > 714:
                cpball_speed.y *= -1
            if cpball.x > 1230:
                break
        return cpball.y + IA_random

    else:
        if cpball_speed.x < 0:
            return 360
        while cpball.x < 1230:
            cpball += cpball_speed
            if cpball.y < 6 or cpball.y > 714:
                cpball_speed.y *= -1
            if cpball.x < 50:
                break
        return cpball.y + IA_random



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("PONG")
pygame.display.set_icon(pygame.image.load("pong.jpeg"))
running = True
dt = 0
player_pos = 360
point = [0, 0]

#rules
paddle_size = 100
paddle_speed = 3
ball_start_speed = [3, random.uniform(-1, 1)]
ball_acceleration = 0.2
paddle_radius = 8
IA_lvl = 50
IA_dumb = 10

# ball move
ball_speed = pygame.Vector2( ball_start_speed )
ball_pos = pygame.Vector2(100, 360)
ball_old_pos = []

# IA move
IA_pos = 360
IA_target = 360
IA_counter = 0
IA_random = random.randint( -IA_lvl, IA_lvl )
IA_rand_dumb = random.randint( 0, IA_dumb )


#stats
ball_max_speed = [0, 0]
ball_bonce = 0
max_exchange = 0
playerdistances = [0, 0]
exchange = 0


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if point[0] == 5:
        running = False
        print("\nIA WINS")
        print("score: ", point[0], " - ", point[1])
        print("max speed: ", round(ball_max_speed[0] * 10, 1), " - ", round(ball_max_speed[1] * 10, 1))
        print("player distances: ", round(playerdistances[0] / 100), " - ", round(playerdistances[1] / 100))
        print("bounce: ", ball_bonce)
        print("max exchange: ", max_exchange)


    if point[1] == 5:
        running = False
        print("\nPlayer WINS")
        print("score: ", point[0], " - ", point[1])
        print("max speed: ", round(ball_max_speed[0] * 10, 1), " - ", round(ball_max_speed[1] * 10, 1))
        print("player distances: ", round(playerdistances[0] / 100), " - ", round(playerdistances[1] / 100))
        print("bounce: ", ball_bonce)
        print("max exchange: ", max_exchange)
    
    if keys[pygame.K_UP] and player_pos > 0:
        player_pos -= paddle_speed
        playerdistances[1] += paddle_speed

    elif keys[pygame.K_DOWN] and player_pos < 720:
        player_pos += paddle_speed
        playerdistances[1] += paddle_speed

    screen.fill("black")
    
    # draw middle line
    for i in range(0, 17):
        pygame.draw.rect(screen, "white", (638, 33 + i * 40, 4, 15))

    # draw IA
    IA = pygame.draw.rect(screen, "white", (50, IA_pos - 50, 10, paddle_size))

    # draw ball
    ball = pygame.draw.circle(screen, "white", ball_pos, 12)

    # draw player
    player = pygame.draw.rect(screen, "white", (1230, (player_pos - 50), 10, paddle_size))

    # draw ball trail
    ball_old_pos.append(ball_pos.copy())
    if len(ball_old_pos) > 100:
        ball_old_pos.pop(0)
    raptici = 0
    for i in range(1, len(ball_old_pos)):
        raptici += 12/100 
        pygame.draw.circle(screen, "white", ball_old_pos[i], raptici)


    player_target = path_estimation( 2 )
    if player_pos > player_target + paddle_speed:
        player_pos -= paddle_speed
        playerdistances[1] += paddle_speed
    elif player_pos < player_target - paddle_speed:
        player_pos += paddle_speed
        playerdistances[1] += paddle_speed

    # ball move
    ball_pos += ball_speed
    if ball.colliderect(IA) and ball_speed.x < 0:
        ball_speed.x *= -1
        ball_speed.x += ball_acceleration
        ball_speed.y = (ball_pos.y - IA_pos) / paddle_radius
        IA_random = random.randint( -IA_lvl, IA_lvl )
        IA_rand_dumb = random.randint( 0, IA_dumb )
        exchange += 1
        ball_bonce += 1
        if math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 ) > ball_max_speed[0]:
            ball_max_speed[0] = math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 )

    if ball.colliderect(player) and ball_speed.x > 0:
        ball_speed.x *= -1
        ball_speed.x -= ball_acceleration
        ball_speed.y = (ball_pos.y - player_pos) / paddle_radius
        IA_random = random.randint( -IA_lvl, IA_lvl )
        IA_rand_dumb = random.randint( 0, IA_dumb )
        exchange += 1
        ball_bonce += 1
        if math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 ) > ball_max_speed[1]:
            ball_max_speed[1] = math.sqrt( ball_speed.x ** 2 + ball_speed.y ** 2 )

    if ball_pos.y < 10 and ball_speed.y < 0 or ball_pos.y > 710 and ball_speed.y > 0:
        ball_speed.y *= -1
        ball_bonce += 1
    
    if ball_pos.x > 1280:
        ball_pos = pygame.Vector2(1180, 360)
        ball_speed = pygame.Vector2(-3, random.uniform(-1, 1))
        IA_pos = 360
        player_pos = 360
        point[0] += 1
        pygame.display.set_caption(f"{point[0]} IA | Player {point[1]}")
        screen.fill("black")
        if exchange > max_exchange:
            max_exchange = exchange
        exchange = 0
        pygame.time.delay(500)

    if ball_pos.x < 0:
        ball_pos = pygame.Vector2(100, 360)
        ball_speed = pygame.Vector2(3, random.uniform(-1, 1))
        IA_pos = 360
        player_pos = 360
        point[1] += 1
        pygame.display.set_caption(f"{point[0]} IA | Player {point[1]}")
        screen.fill("black")
        if exchange > max_exchange:
            max_exchange = exchange
        exchange = 0
        pygame.time.delay(500)

    if IA_counter == 0:
        IA_target = path_estimation( 1 )

    
    IA_counter += 1

    if IA_counter > 240:
        IA_counter = 0

    # IA move
    
    if IA_pos > IA_target + paddle_speed:
        IA_pos -= paddle_speed
        playerdistances[0] += paddle_speed
    elif IA_pos < IA_target - paddle_speed:
        IA_pos += paddle_speed
        playerdistances[0] += paddle_speed

    pygame.display.flip()

    dt = clock.tick(240) / 1000

pygame.quit()
