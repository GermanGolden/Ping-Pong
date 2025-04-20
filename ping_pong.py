import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 640, 480
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BACKGROUND_COLOR = (135, 206, 235)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг")

ball_image = pygame.image.load('ball.png')
wall_image = pygame.image.load('wall.png')

ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))
wall_image = pygame.transform.scale(wall_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.reset()

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-7, 7])
        self.speed_y = random.choice([-7, 7])

class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= 10
        elif not up and self.rect.bottom < HEIGHT:
            self.rect.y += 10

ball = Ball()
paddle1 = Paddle(30)
paddle2 = Paddle(WIDTH - PADDLE_WIDTH - 30)

score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.move(up=True)
    if keys[pygame.K_s]:
        paddle1.move(up=False)
    if keys[pygame.K_UP]:
        paddle2.move(up=True)
    if keys[pygame.K_DOWN]:
        paddle2.move(up=False)

    ball.move()

    if ball.rect.colliderect(paddle1.rect) or ball.rect.colliderect(paddle2.rect):
        ball.speed_x *= -1

    if ball.rect.left <= 0:
        score2 += 1
        ball.reset()
    elif ball.rect.right >= WIDTH:
        score1 += 1
        ball.reset()

    screen.fill(BACKGROUND_COLOR)
    screen.blit(ball_image, ball.rect.topleft)
    screen.blit(wall_image, paddle1.rect.topleft)
    screen.blit(wall_image, paddle2.rect.topleft)

    score_text = font.render(f"{score1} : {score2}", True, (255, 255, 255))
    text_rect = score_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(score_text, text_rect)

    pygame.display.flip()
    pygame.time.delay(20)