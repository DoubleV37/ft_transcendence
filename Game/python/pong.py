import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# ball move
ball_speed = pygame.Vector2( 10, random.randint( -10, 10 ))
ball_pos = pygame.Vector2(100, 360)
ball_old_pos = []

# IA move
IA_speed = 8
IA_pos = 360
IA_rand = random.randint(0, 60)

pygame.display.set_caption(" 0 IA | Player 0")
pygame.display.set_icon(pygame.image.load("pong.jpeg"))

IA_points = 0
player_points = 0
start = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # get mouse position
    mouse = pygame.mouse.get_pos()

    # EXIT
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if IA_points == 5:
        running = False
        print("\nIA WINS")

    if player_points == 5:
        running = False
        print("\nPlayer WINS")

    # walll = pygame.draw.rect(screen, "black", (0, 0, 60, 720))
    # wallr = pygame.draw.rect(screen, "black", (1230, 0, 50, 720))
    
    # draw middle line
    for i in range(0, 17):
        pygame.draw.rect(screen, "white", (638, 33 + i * 40, 4, 15))

    # draw IA
    IA = pygame.draw.rect(screen, "white", (50, IA_pos - 50, 10, 100))

    # draw ball
    ball = pygame.draw.circle(screen, "white", ball_pos, 12)

    ball_old_pos.append(ball_pos.copy())
    if len(ball_old_pos) > 24:
        ball_old_pos.pop(0)
    for i in range(1, len(ball_old_pos)):
        pygame.draw.circle(screen, "white", ball_old_pos[i], i/2)

    # draw player
    player = pygame.draw.rect(screen, "white", (1230, mouse[1] - 50, 10, 100))

    if start:
        pygame.display.flip()
        pygame.time.delay(1500)
        start = False

    # ball move
    ball_pos += ball_speed
    if ball.colliderect(IA) and ball_speed.x < 0:
        ball_speed.x *= -1
        # ball_speed.x += 1
        ball_speed.y = (ball_pos.y - IA_pos)
        IA_rand = random.randint(0, 60)

    if ball.colliderect(player) and ball_speed.x > 0:
        ball_speed.x *= -1
        # ball_speed.x -= 1
        ball_speed.y = (ball_pos.y - (mouse[1])) / 4

    if ball_pos.y < 10 and ball_speed.y < 0 or ball_pos.y > 710 and ball_speed.y > 0:
        ball_speed.y *= -1
    
    if ball_pos.x > 1280:
        ball_pos = pygame.Vector2(1180, 360)
        ball_speed = pygame.Vector2(-10, random.randint( -10, 10 ))
        IA_pos = 360
        IA_points += 1
        pygame.display.set_caption(f"{IA_points} IA | Player {player_points}")
        screen.fill("black")
        pygame.time.delay(500)

    if ball_pos.x < 0:
        ball_pos = pygame.Vector2(100, 360)
        ball_speed = pygame.Vector2(10, random.randint( -10, 10 ))
        IA_pos = 360
        player_points += 1
        pygame.display.set_caption(f"{IA_points} IA | Player {player_points}")
        screen.fill("black")
        pygame.time.delay(500)

    if ball_pos.y + 30 > IA_pos + IA_rand:
        if IA_pos + IA_speed > ball_pos.y:
            IA_pos = ball_pos.y
        else:
            IA_pos += IA_speed
    else:
        if IA_pos - IA_speed < ball_pos.y:
            IA_pos = ball_pos.y
        else:
            IA_pos -= IA_speed

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
