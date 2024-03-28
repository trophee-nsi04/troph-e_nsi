from math import sqrt
import pygame
from pygame.locals import *
from pygame import mixer
import random

class Jodoka:
    def __init__(self,color,x,y):
        self.rage=True
        self.x = x
        self.y = y
        self.color=color
        self.frames=[]

    def draw(self,frame):
        if self.color == "b":
            self.sprite = pygame.transform.scale(pygame.image.load("judo/judoka blanc_"+frame+".png"),(120,120))
        elif self.color == "r" and self.rage:
            self.sprite = pygame.transform.scale(pygame.image.load("judo/judoka rouge_"+frame+".png"),(120,120))
        elif self.color == "r" and not self.rage:
            self.sprite = pygame.transform.scale(pygame.image.load("judo/judoka vert_"+frame+".png"),(120,120))
        display.blit(self.sprite,(self.x,self.y))

pygame.init()
window_width=600
window_height=600
display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('judo game')

mixer.music.load("judo/judoMusic.wav")
mixer.music.set_volume(0.05)
mixer.music.play(-1)



player = Jodoka("b",0,240)
opponent = Jodoka("r",window_width-120,240)
end = ""
last_update=0
animation_delay=500
frame=1
rage_count=0

def draw_bg():
    for j in range(5):
        for i in range(5):
            bg = pygame.transform.scale(pygame.image.load("judo/tuile.png"),(120,120))
            display.blit(bg,(120*i,120*j))


pygame.display.flip()
running = True
after_game=True
while running:
    draw_bg()

    current_time = pygame.time.get_ticks()
    print(current_time)
    if current_time-last_update >= animation_delay:
        frame+=1
        last_update=current_time
        if frame > 2:
            frame=1

    for event in pygame.event.get():

        if rage_count==0:
                    opponent.rage=not opponent.rage
                    rage_count=random.randint(2,5)+1

        if event.type == QUIT:
            running = False
            after_game=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.set_mode((0,0), FULLSCREEN)
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_mode((0,0), RESIZABLE)
            if event.key == pygame.K_RIGHT:
                if player.x<window_width-120:
                    player.x+=120
            if event.key == pygame.K_LEFT:
                if player.x>=120:
                    player.x-=120
            if event.key == pygame.K_UP:
                if player.y>=120:
                    player.y-=120
            if event.key == pygame.K_DOWN:
                if player.y<window_height-120:
                    player.y+=120


            if event.key == pygame.K_UP or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:

                mixer.Sound("judo/Whoosh.wav").play()

                rage_count-=1
                dists={}

                if opponent.x>=120:#left
                    dists.update({sqrt((opponent.y-player.y)**2+((opponent.x-120)-player.x)**2):"left"})

                if opponent.y>=120:#up
                    dists.update({sqrt(((opponent.y-120)-(player.y))**2+(opponent.x-player.x)**2):"up"})

                if opponent.y<window_height-120:#down
                    dists.update({sqrt(((opponent.y+120)-(player.y))**2+(opponent.x-player.x)**2):"down"})

                if opponent.x<window_width-120:#right
                    dists.update({sqrt((opponent.y-player.y)**2+((opponent.x+120)-player.x)**2):"right"})



                if opponent.rage:
                    action=dists[min(dists)]
                else:
                    action=dists[max(dists)]
                if random.randint(1,2)==1:
                    action=random.choice(["up","down","right","left","none"])

                if action=="up":
                    if opponent.y>=120:
                        opponent.y-=120
                if action=="down":
                    if opponent.y<window_height-120:
                        opponent.y+=120
                if action=="left":
                    if opponent.x>=120:
                        opponent.x-=120
                if action=="right":
                    if opponent.x<window_width-120:
                        opponent.x+=120



            if player.x == opponent.x and player.y == opponent.y:
                running=False
                if opponent.rage:
                    end="l"
                else:
                    end="w"
    opponent.draw(str(frame))
    player.draw(str(frame))
    pygame.display.flip()

font = pygame.font.SysFont(None, 30)
textReplay = font.render('press R to replay', True, (0,0,0))
textMenu = font.render('press T to go to the menu', True, (0,0,0))


while after_game:
    for event in pygame.event.get():
        if event.type == QUIT:
            after_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                after_game = False
                with open("judo_game.py") as f:
                    exec(f.read())
            if event.key == pygame.K_t:
                after_game = False
                pygame.quit()
                with open("lobby.py") as f:
                    exec(f.read())
    if end == "w":
        display.blit(pygame.transform.scale(pygame.image.load("judo/win.png"),(600,600)),(0,0))
    elif end == "l":
        display.blit(pygame.transform.scale(pygame.image.load("judo/lose.png"),(600,600)),(0,0))

    display.blit(textReplay, (20, 370))
    display.blit(textMenu, (20, 390))

    pygame.display.flip()
pygame.quit()