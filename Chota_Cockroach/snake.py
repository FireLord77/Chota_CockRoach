import pygame
import random
import math

pygame.mixer.init()
pygame.init()

screen_width = 900
screen_height = 700

gameWindow = pygame.display.set_mode((screen_width,screen_height))

bgimg = pygame.image.load("snack_back_img.png")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

welimg = pygame.image.load("welcome.png")
welimg = pygame.transform.scale(welimg,(screen_width,screen_height)).convert_alpha()

head_img = pygame.image.load("banana.png")
head_img = pygame.transform.scale(head_img, (25, 25)).convert_alpha()

over_img = pygame.image.load("game_over.png")
over_img = pygame.transform.scale(over_img, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("CHOTA COCKROACH")
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)

eat_sound = pygame.mixer.Sound('snack_eat.ogg')
crash_sound = pygame.mixer.Sound('snack_crash.ogg')

def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])


def draw_graphic_banana(surface, x, y):
    target_size = 25
    resolution = 128
    pixel_size = target_size / resolution

    angle = -0.78
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    HIGHLIGHT = (255, 250, 140)

    HIGHLIGHT = (255, 250, 140)
    BODY_LIGHT = (255, 235, 40)
    BODY_SHADE = (220, 180, 5)
    DARK_SHADOW = (145, 105, 10)
    STEM_GREEN = (155, 185, 45)
    STEM_BROWN = (100, 70, 35)
    TIP_BROWN = (45, 30, 15)

    for row in range(resolution):
        for col in range(resolution):
            raw_nx = (col / resolution) * 2.0 - 1.0
            raw_ny = (row / resolution) * 2.0 - 1.0
            nx = raw_nx * cos_a - raw_ny * sin_a
            ny = raw_nx * sin_a + raw_ny * cos_a

            arc_bend = 0.55 * (ny ** 2) - 0.25
            adjusted_nx = nx + arc_bend

            thickness = 0.35 * math.cos(ny * 1.5)

            dist_from_core = abs(adjusted_nx)

            if dist_from_core < thickness and -0.85 < ny < 0.85:
                shading_vector = adjusted_nx / thickness

                if shading_vector < -0.6:
                    color = HIGHLIGHT
                elif shading_vector < 0.0:
                    color = BODY_LIGHT
                elif shading_vector < 0.5:
                    color = BODY_SHADE
                else:
                    color = DARK_SHADOW

                if ny < -0.65:
                    color = tuple(int(color[i] * 0.5 + STEM_GREEN[i] * 0.5) for i in range(3))

                px = x + int(col * pixel_size)
                py = y + int(row * pixel_size)
                pygame.draw.rect(surface, color, [px, py, 2, 2])

            elif dist_from_core < 0.08 and -0.95 <= ny <= -0.85:
                px = x + int(col * pixel_size)
                py = y + int(row * pixel_size)
                pygame.draw.rect(surface, STEM_BROWN, [px, py, 2, 2])

            elif dist_from_core < 0.06 and 0.85 <= ny <= 0.90:
                px = x + int(col * pixel_size)
                py = y + int(row * pixel_size)
                pygame.draw.rect(surface, TIP_BROWN, [px, py, 2, 2])

def draw_graphic_cockroach(surface, x, y, size=25):
    body_brown = (139, 69, 19)
    dark_brown = (80, 35, 10)
    antenna_color = (60, 30, 5)

    cx = x + size // 2
    cy = y + size // 2

    for side in [-1, 1]:
        for offset_y in [-4, 0, 4]:
            pygame.draw.line(surface, antenna_color, (cx, cy + offset_y), (cx + (side * 11), cy + offset_y - 2), 2)

    pygame.draw.ellipse(surface, body_brown, [x + 4, y + 4, 17, 18])

    for line_y in [y + 8, y + 12, y + 16]:
        pygame.draw.line(surface, dark_brown, (x + 6, line_y), (x + 19, line_y), 1)

    pygame.draw.circle(surface, dark_brown, (cx, y + 5), 4)

    pygame.draw.line(surface, antenna_color, (cx - 2, y + 5), (x - 2, y - 4), 1)
    pygame.draw.line(surface, antenna_color, (cx + 2, y + 5), (x + size + 2, y - 4), 1)


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((255,255,0))
        gameWindow.blit(welimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('snack_back_audio.mp3')
                    pygame.mixer.music.play(loops=-1)
                    gameloop()

        pygame.display.update()
        clock.tick(60)


def gameloop():
    snk_list = []
    snk_length = 1

    snake_x = 450
    snake_y = 350
    snake_size = 25

    velocity_x = 0
    velocity_y = 0
    init_velocity = 5

    exit_game = False
    game_over = False

    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)

    fps = 60

    score = 0

    eat_diff = 20

    food_x = random.randint(100, screen_width - 100)
    food_y = random.randint(100, screen_height - 100)

    with open("Snake_Scores.txt", "r") as f:
        hiscore = f.read()
    while not exit_game:
        if game_over:
            with open("Snake_Scores.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill((255, 255, 0))
            gameWindow.blit(over_img, (0, 0))

            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RIGHT:
                        if velocity_x == 0:
                            velocity_x = init_velocity
                            velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        if velocity_x == 0:
                            velocity_x = -init_velocity
                            velocity_y = 0
                    if event.key == pygame.K_UP:
                        if velocity_y == 0:
                            velocity_y = -init_velocity
                            velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        if velocity_y == 0:
                            velocity_y = init_velocity
                            velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x)<eat_diff and abs(snake_y-food_y)<eat_diff:
                eat_sound.play()
                score += 10
                food_x = random.randint(100, screen_width - 100)
                food_y = random.randint(100, screen_height - 100)
                snk_length += 10
                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill((190,210,220))
            gameWindow.blit(bgimg,(0,0))
            text_screen("Score: " + str(score) + "               High Score: " + str(hiscore), blue, 5, 5)
            draw_graphic_banana(gameWindow, food_x, food_y)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                pygame.mixer.music.stop()
                crash_sound.play()
                game_over = True
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.stop()
                crash_sound.play()

            for i, segment in enumerate(snk_list):
                if i == len(snk_list) - 1:
                    gameWindow.blit(head_img, (segment[0], segment[1]))
                else:
                    draw_graphic_cockroach(gameWindow, segment[0], segment[1], snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()
welcome()