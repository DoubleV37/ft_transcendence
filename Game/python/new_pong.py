import pygame
import random
import math

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PONG")
        pygame.display.set_icon(pygame.image.load("pong.jpeg"))
        self.running = True
        self.player_pos = 360
        self.point = [0, 0]
        self.paddle_size = 100
        self.paddle_speed = 3
        self.ball_start_speed = [3, random.uniform(-1, 1)]
        self.ball_acceleration = 0.2
        self.paddle_radius = 8
        self.IA_lvl = 50
        self.IA_dumb = 10
        self.ball_speed = pygame.Vector2(self.ball_start_speed)
        self.ball_pos = pygame.Vector2(100, 360)
        self.ball_old_pos = []
        self.IA_pos = 360
        self.IA_target = 360
        self.IA_counter = 0
        self.IA_random = random.randint(-self.IA_lvl, self.IA_lvl)
        self.IA_rand_dumb = random.randint(0, self.IA_dumb)
        self.ball_max_speed = [0, 0]
        self.ball_bonce = 0
        self.max_exchange = 0
        self.playerdistances = [0, 0]
        self.exchange = 0

    def path_estimation(self, pos):
        cpball = self.ball_pos.copy()
        cpball_speed = self.ball_speed.copy()
        if self.IA_rand_dumb == 0:
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
            return cpball.y + self.IA_random

        else:
            if cpball_speed.x < 0:
                return 360
            while cpball.x < 1230:
                cpball += cpball_speed
                if cpball.y < 6 or cpball.y > 714:
                    cpball_speed.y *= -1
                if cpball.x < 50:
                    break
            return cpball.y + self.IA_random

    def draw_middle_line(self):
        for i in range(0, 17):
            pygame.draw.rect(self.screen, "white", (638, 33 + i * 40, 4, 15))

    def draw_ball_trail(self):
        self.ball_old_pos.append(self.ball_pos.copy())
        if len(self.ball_old_pos) > 100:
            self.ball_old_pos.pop(0)
        raptici = 0
        for i in range(1, len(self.ball_old_pos)):
            raptici += 12/100 
            pygame.draw.circle(self.screen, "white", self.ball_old_pos[i], raptici)

    def update_ball_position(self):
        self.ball_pos += self.ball_speed
        if self.ball_pos.y < 10 and self.ball_speed.y < 0 or self.ball_pos.y > 710 and self.ball_speed.y > 0:
            self.ball_speed.y *= -1
            self.ball_bonce += 1

    def update_IA_position(self):
        if self.IA_pos > self.IA_target + self.paddle_speed and self.IA_pos > 0:
            self.IA_pos -= self.paddle_speed
            self.playerdistances[0] += self.paddle_speed
        elif self.IA_pos < self.IA_target - self.paddle_speed and self.IA_pos < 720:
            self.IA_pos += self.paddle_speed
            self.playerdistances[0] += self.paddle_speed

    def update_player_position(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_pos > 0:
            self.player_pos -= self.paddle_speed
            self.playerdistances[1] += self.paddle_speed
        elif keys[pygame.K_DOWN] and self.player_pos < 720:
            self.player_pos += self.paddle_speed
            self.playerdistances[1] += self.paddle_speed

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update_player_position()
            self.update_ball_position()
            self.update_IA_position()

            self.screen.fill("black")
            self.draw_middle_line()
            self.draw_ball_trail()

            # Dessin des objets
            pygame.draw.rect(self.screen, "white", (50, self.IA_pos - 50, 10, self.paddle_size))
            pygame.draw.circle(self.screen, "white", self.ball_pos, 12)
            pygame.draw.rect(self.screen, "white", (1230, (self.player_pos - 50), 10, self.paddle_size))

            pygame.display.flip()
            dt = self.clock.tick(240) / 1000

if __name__ == "__main__":
    game = PongGame()
    game.game_loop()
    pygame.quit()
