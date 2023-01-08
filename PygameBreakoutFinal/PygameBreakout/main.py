import pygame
import time

pygame.init()

# Creating the window and naming the game
screen = pygame.display.set_mode((600, 800))
pygame.display.set_caption("Breakout")

# sound effects
bounce_sound_effect = pygame.mixer.Sound('bounce.wav')
scoring_sound_effect = pygame.mixer.Sound('bleep_sound.wav')

# Drawing the objects
drawGroup = pygame.sprite.Group()

# Color list
blue = (77, 109, 243)
red = (162, 8, 0)
orange = (183, 119, 0)
green = (0, 127, 33)
yellow = (197, 199, 37)

edge = pygame.sprite.Sprite(drawGroup)
paddle = pygame.sprite.Sprite(drawGroup)
ball = pygame.sprite.Sprite(drawGroup)


def draw_objects(obj, w, h, x, y, data):
    obj.image = pygame.image.load(data)
    obj.image = pygame.transform.scale(obj.image, [w, h])
    obj.rect = pygame.Rect(x, y, 0, 0)


def hud_draw(x, y, score):
    font = pygame.font.Font('PressStart2P.ttf', 32)
    text = font.render(f"{score}", True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)

def draw_border_details():
    pygame.draw.line(screen, blue, (24, 713), (24, 731), 12)
    pygame.draw.line(screen, blue, (576, 713), (576, 731), 12)
    pygame.draw.line(screen, red, (24, 180), (24, 207), 12)
    pygame.draw.line(screen, red, (576, 180), (576, 207), 12)
    pygame.draw.line(screen, orange, (24, 208), (24, 237), 12)
    pygame.draw.line(screen, orange, (576, 208), (576, 237), 12)
    pygame.draw.line(screen, green, (24, 238), (24, 267), 12)
    pygame.draw.line(screen, green, (576, 238), (576, 267), 12)
    pygame.draw.line(screen, yellow, (24, 268), (24, 296), 12)
    pygame.draw.line(screen, yellow, (576, 268), (576, 296), 12)


draw_objects(edge, 600, 900, 7, 0, "Edge.png")
draw_objects(paddle, 40, 60, 270, 700, "Paddle.png")
draw_objects(ball, 8, 8, 298, 700, "Ball.png")


# Drawing the bricks
colors = ['YellowBrick', 'YellowBrick', 'GreenBrick', 'GreenBrick',
          'OrangeBrick', 'OrangeBrick', 'RedBrick', 'RedBrick']
bricks_count = []
x_pos = []
y_pos = []
y = 300

for i in range(8):
    y = y - 15
    x = 30
    for j in range(14):
        brick = pygame.sprite.Sprite(drawGroup)
        brick.image = pygame.image.load(f"{colors[i]}.png")
        brick.image = pygame.transform.scale(brick.image, [35, 11])
        brick.rect = pygame.Rect(x, y, 0, 0)
        x_pos.append(x)
        y_pos.append(y)
        bricks_count.append(brick)

        x = x + 39
print(x_pos)
print(y_pos)
print(len(bricks_count))

# Initial scores

birth_score = 1
brick_score = 0

# Initial ball coordinates
ball_dx = 4
ball_dy = 4

# Game looping
game_loop = True

while game_loop:

    for event in pygame.event.get():

        # Command to close the game
        if event.type == pygame.QUIT:
            game_loop = False

    # Paddle moves
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if paddle.rect.x == 514:
            paddle.rect.x = 514
        else:
            paddle.rect.x += 4
    if keys[pygame.K_LEFT]:
        if paddle.rect.x == 26:
            paddle.rect.x = 26
        else:
            paddle.rect.x -= 4

    # Ball movement
    ball.rect.x += ball_dx
    ball.rect.y -= ball_dy

    # Collision with the right wall
    if ball.rect.x >= 565:
        ball_dx *= -1
        bounce_sound_effect.play()

    # Collision with the left wall
    if ball.rect.x <= 25:
        ball_dx *= -1
        bounce_sound_effect.play()

    # Collision with the roof
    if ball.rect.y <= 15:
        ball_dy *= -1
        bounce_sound_effect.play()

    # Collision with the paddle
    if ball.rect.y == paddle.rect.y and paddle.rect.x + 50 > ball.rect.x > paddle.rect.x - 30:
        ball_dy *= -1
        bounce_sound_effect.play()

    # Collision with the floor
    if ball.rect.y > paddle.rect.y + 100:
        time.sleep(2)
        ball.rect.y = paddle.rect.y - 400
        ball.rect.x = 300
        paddle.rect.x = 270
        birth_score += 1

    # Collision with the brick
    if birth_score <= 100:
        for brick in bricks_count:
            if brick.rect.y > ball.rect.y > brick.rect.y - 20 \
                    and brick.rect.x + 20 > ball.rect.x > brick.rect.x - 20:
                brick.rect = pygame.Rect(1000, 1000, 0, 0)
                ball_dy *= -1
                brick_score += 1
                bricks_count.remove(brick)
                bounce_sound_effect.play()

    if birth_score > 100:
        paddle.rect.x = -35
        paddle.image = pygame.transform.scale(paddle.image, [655, 60])

        for brick in bricks_count:
            if ball.rect.y < brick.rect.y + 25 and brick.rect.x + 20 > ball.rect.x > brick.rect.x - 20:
                ball_dy *= -1

        if ball.rect.y == 700:
            ball_dy *= -1

    screen.fill([0, 0, 0])

    # Draw Hud
    drawGroup.draw(screen)
    draw_border_details()

    if len(bricks_count) == 112:
        hud_draw(80, 60, '1')
        hud_draw(110, 100, '000')
        hud_draw(440, 60, birth_score)
        hud_draw(470, 100, '000')

    else:
        hud_draw(80, 60, '1')
        hud_draw(110, 100, brick_score)
        hud_draw(440, 60, birth_score)
        hud_draw(470, 100, '000')

    # Game ending
    if len(bricks_count) == 0:
        hud_draw(300, 400, 'GAME IS OVER! YOU WON!')

    # Display update
    pygame.display.flip()
