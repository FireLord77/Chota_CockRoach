import pygame
import random

pygame.mixer.init()
pygame.init()

screen_width = 900
screen_height = 700

gameWindow = pygame.display.set_mode((screen_width,screen_height))

bgimg = pygame.image.load("snack_back_img.png")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

welimg = pygame.image.load("wlcome.png")
welimg = pygame.transform.scale(welimg,(screen_width,screen_height)).convert_alpha()

pygame.display.set_caption("SMOHKEY")
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)

eat_sound = pygame.mixer.Sound('snack_eat.mp3')
crash_sound = pygame.mixer.Sound('snak_crash.mp3')

def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((255,255,0))
        gameWindow.blit(welimg, (0, 0))
        text_screen("Welcome to SMOHKEY",(0,0,255),230,300)
        text_screen("Press Space Bar to Play", (0, 0, 255), 230, 350)
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
            gameWindow.fill((135,190,50))
            text_screen("GAME OVER !!!! Press Enter to Continue",red,100,310)

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
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]
            if head in snk_list[:-1]:
                pygame.mixer.music.load('snak_crash.mp3')
                pygame.mixer.music.play()
                game_over = True
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('snak_crash.mp3')
                pygame.mixer.music.play()


            pygame.draw.rect(gameWindow,green,[snake_x,snake_y,snake_size,snake_size])


            plot_snake(gameWindow,(0,255,255),snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()
welcome()