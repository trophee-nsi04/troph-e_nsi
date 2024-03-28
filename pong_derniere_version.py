import pygame
import sys
from pygame.locals import *

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

# Couleurs
TABLE = (18, 98, 183)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 183)
GREEN = (0, 255, 0)
GREY = (118, 118, 118)

# Initialisation de l'écran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
font = pygame.font.Font('freesansbold.ttf', 32)
SCORE1 = 0
SCORE2 = 0

# Paramètres de la raquette et de la balle
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7
BALL_SIZE = 10
BALL_SPEED_X = 7
BALL_SPEED_Y = 9

SCORE_INCREMENT = 1


# Position initiale des raquettes et de la balle
paddle1_pos = [10, ((SCREEN_HEIGHT + 100) // 2 ) - PADDLE_HEIGHT // 2]
paddle2_pos = [SCREEN_WIDTH - 30, ((SCREEN_HEIGHT + 100) // 2 ) - PADDLE_HEIGHT // 2]
ball_pos = [SCREEN_WIDTH // 2 - BALL_SIZE // 2, (SCREEN_HEIGHT // 2 + 100) - BALL_SIZE // 2]

# Vitesse de la balle
ball_speed = [BALL_SPEED_X, BALL_SPEED_Y]

# Fonction pour déplacer la raquette
def move_paddle(paddle, direction):
    if direction == "up":
        paddle[1] -= PADDLE_SPEED
    elif direction == "down":
        paddle[1] += PADDLE_SPEED

# Boucle principale
after_game = True
while after_game :

    if SCORE1 == 11:
        after_game = False

    elif SCORE2 == 11:
        after_game = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        move_paddle(paddle1_pos, "up")
    if keys[pygame.K_s]:
        move_paddle(paddle1_pos, "down")
    if keys[pygame.K_UP]:
        move_paddle(paddle2_pos, "up")
    if keys[pygame.K_DOWN]:
        move_paddle(paddle2_pos, "down")

    # Mouvement de la balle
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Rebond sur les bords verticaux
    if ball_pos[1] <= 100 or ball_pos[1] >= SCREEN_HEIGHT - BALL_SIZE:
        ball_speed[1] = -ball_speed[1]

    # Rebond sur les raquettes
    if (ball_pos[0] <= paddle1_pos[0] + PADDLE_WIDTH and paddle1_pos[1] <= ball_pos[1] <= paddle1_pos[1] + PADDLE_HEIGHT):
        ball_speed[0] = -ball_speed[0]

    elif (ball_pos[0] >= paddle2_pos[0] - BALL_SIZE and paddle2_pos[1] <= ball_pos[1] <= paddle2_pos[1] + PADDLE_HEIGHT):
        ball_speed[0] = -ball_speed[0]

    # Sortie de la balle
    if ball_pos[0] <= 0 :
        ball_speed[0] = -ball_speed[0]
        ball_speed[1] = -ball_speed[1]
        SCORE2 += SCORE_INCREMENT
        ball_pos = [SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2]
    elif ball_pos[0] >= SCREEN_WIDTH - BALL_SIZE :
        ball_speed[0] = -ball_speed[0]
        ball_speed[1] = -ball_speed[1]
        SCORE1 += SCORE_INCREMENT
        ball_pos = [SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2]

    # Dessiner

    screen.fill(TABLE)
    pygame.draw.rect(screen, BLACK, pygame.Rect(0,0,SCREEN_WIDTH,99))
    pygame.draw.rect(screen, WHITE, pygame.Rect(0, (SCREEN_HEIGHT + 100) // 2 - 5, SCREEN_WIDTH, 10))
    pygame.draw.rect(screen, RED, pygame.Rect(paddle1_pos[0], paddle1_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, BLUE, pygame.Rect(paddle2_pos[0], paddle2_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, pygame.Rect(ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))

    # Bandes Blanches autour de la table

    pygame.draw.rect(screen, WHITE, pygame.Rect(0,100,10,SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, pygame.Rect(0,100,SCREEN_WIDTH,10))
    pygame.draw.rect(screen, WHITE, pygame.Rect(0,SCREEN_HEIGHT - 10,SCREEN_WIDTH,10))
    pygame.draw.rect(screen, WHITE, pygame.Rect(SCREEN_WIDTH - 10,100,10,SCREEN_HEIGHT))
    pygame.draw.rect(screen, GREY, pygame.Rect(SCREEN_WIDTH // 2, 100, 10, SCREEN_HEIGHT))

    # Score joueur 1 et 2

    score1_text = font.render(f'Joueur 1 : {SCORE1}', True, WHITE)
    score2_text = font.render(f'Joueur 2 : {SCORE2}', True, WHITE)
    screen.blit(score1_text,(0,15))
    screen.blit(score2_text,(SCREEN_WIDTH - 300, 15))
    pygame.display.flip()

    pygame.time.Clock().tick(60)


    for event in pygame.event.get():
        if event.type == QUIT:
            after_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.set_mode((0,0), FULLSCREEN)
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_mode((0,0), RESIZABLE)
            if event.key == pygame.K_r:
                after_game = False
                with open("pong_derniere_version.py") as f:
                    exec(f.read())
            if event.key == pygame.K_t:
                after_game = False
                pygame.quit()
                with open("lobby.py") as f:
                    exec(f.read())
while after_game==False:
    keys = pygame.key.get_pressed()
    pygame.time.Clock().tick(60)
    if SCORE1 == 11:
        screen.blit(pygame.image.load("pong/p1_won.jpg"), (0,0))
    elif SCORE2 == 11:
        screen.blit(pygame.image.load("pong/p2_won.jpg"), (0,0))
    font1 = pygame.font.Font(None, 60)
    text1 = font1.render("appuyer sur R pour recommencer", True, (255, 255, 255))
    screen.blit(text1, (SCREEN_WIDTH/3.8, SCREEN_HEIGHT/3.6))
    text2 = font1.render("et T pour retourner au lobby", True, (255, 255, 255))
    screen.blit(text2, (SCREEN_WIDTH/3.2, SCREEN_HEIGHT/2.8))

    for event in pygame.event.get():
        if event.type == QUIT:
            after_game = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.set_mode((0,0), FULLSCREEN)
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_mode((0,0), RESIZABLE)
            if event.key == pygame.K_r:
                after_game = True
                with open("pong_derniere_version.py") as f:
                    exec(f.read())
            if event.key == pygame.K_t:
                after_game = True
                pygame.quit()
                with open("lobby.py") as f:
                    exec(f.read())

    pygame.display.flip()
pygame.quit()