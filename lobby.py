import pygame
from pygame.locals import *


pygame.init()


X= 1366
Y= 768
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('lobby')

character = pygame.image.load('loby/character.png') # Chargez une image pour représenter le personnage
character_rect = character.get_rect() # Récupérez les coordonnées du personnage
character_rect.x = 50 # Positionnez le personnage sur l'axe des x
character_rect.y = 50 # Positionnez le personnage sur l'axe des y

PERSO_SPEED_Y = 7
PERSO_SPEED_X = 7

last_update=0
animation_delay=200


def move_perso(paddle, direction):
    if direction == "up":
        character_rect.y -= PERSO_SPEED_Y
    elif direction == "down":
        character_rect.y += PERSO_SPEED_Y
    elif direction == "left":
        character_rect.x -= PERSO_SPEED_X
    elif direction == "right":
        character_rect.x += PERSO_SPEED_X


index=1

running = True
while running:
    screen.blit(pygame.image.load("loby/background_trophe.png"), (0,0))
    time = pygame.time.get_ticks()
    t = Rect(185,65,200,200)
    b = Rect(784,110,562,90)
    p = Rect(828,522,396,170)
    image = pygame.image.load(f"loby/perso/{index}.png")
    screen.blit(image, (character_rect.x , character_rect.y))

    if pygame.Rect.colliderect(t,character_rect) == True:
        font = pygame.font.Font(None, 60)
        text = font.render("appuyer sur R pour jouer au judo", True, (0, 0, 0))
        screen.blit(text, (X/4, 0))
    if pygame.Rect.colliderect(b, character_rect) == True:
        text1 = font.render("appuyer sur R pour jouer au saut en longueur", True, (0, 0, 0))
        screen.blit(text1, (X/6, 0))
    if pygame.Rect.colliderect(p, character_rect) == True:
        text1 = font.render("appuyer sur R pour jouer au ping pong", True, (0, 0, 0))
        screen.blit(text1, (X/5, 0))


    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.set_mode((0,0), FULLSCREEN)
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_mode((0,0), RESIZABLE)
            if event.key == pygame.K_r:
                if pygame.Rect.colliderect(t,character_rect) == True:
                    running = False
                    pygame.quit()
                    with open("judo_game.py") as f:
                        exec(f.read())
                if pygame.Rect.colliderect(p, character_rect) == True:
                    running = False
                    pygame.quit()
                    with open("pong_derniere_version.py") as f:
                        exec(f.read())
                if pygame.Rect.colliderect(b, character_rect) == True:
                    running = False
                    pygame.quit()
                    with open("saut_en_longueur.py") as f:
                        exec(f.read())
    if keys[pygame.K_UP]:
        move_perso(character_rect, "up")
    if keys[pygame.K_DOWN]:
        move_perso(character_rect, "down")
    if keys[pygame.K_LEFT]:
        move_perso(character_rect, "left")
        if time-last_update >= animation_delay:
            image = pygame.image.load(f"loby/perso/{index}.png")
            screen.blit(image, (character_rect.x , character_rect.y))
            index+=1
            last_update=time
            if index>4:
                index=3
    if keys[pygame.K_RIGHT]:
        move_perso(character_rect, "right")
        if time-last_update >= animation_delay:
            image = pygame.image.load(f"loby/perso/{index}.png")
            screen.blit(image, (character_rect.x , character_rect.y))
            index+=1
            last_update=time
            if index>2:
                index=1


    pygame.display.flip()
pygame.quit()
