import pygame
from pygame.locals import *
import random
import time
import math
import subprocess
from pygame import mixer


pygame.init()


X= 1366
Y= 768
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption('saut en longueur')
background_color = (135,206,235)
ground_color = (139, 69, 19)
border_color = (120, 50, 0)
cloud_count = 7
cloud_color = (255, 255, 255)
cloud_size = 20
b=X-510
j=X-460
n=X-400
v=X-350
r=X-290
s=random.randint(2000, 3000)
yy=500
ss=0

sound = pygame.mixer.Sound("saut/course.wav")
sound1 = pygame.mixer.Sound("saut/sifflet.wav")

rejouer=False


def calculate_trajectory(t,h):
    xp1 = 700 + 75 * math.cos(math.radians(45)) * t
    yp1 = 450 - (70 * math.sin(math.radians(45)) * t - h * 9.81 * t**2)  # Inversion de l'axe y
    return xp1, yp1
t=1
h=0.65
#SCORE
affiche_score=0
score = False

#mouv
stop = False

#PERSO COURT
clock = pygame.time.Clock()
xp = 50
yp = 400
index = 1
court =True

#PERSO SAUTE
saute = False
xp1 = 750
yp1 = 450

#2024
q=100

re=X/2

#SPECT
spect_count = 6
ys = 160
spect = []
for i in range(6):
    for _ in range(spect_count):
        xs = random.randint(-100,1600)
        spect.append((xs, ys))
    ys+=50

#MOUV SPECT
dx = -10

#AIGUILLE
radius = 200
angle = 180
speed = 10
coord_factor = 720.0 / 400

# Point de départ et de fin de la ligne
x1 = 225 + radius * math.cos(math.radians(angle + 10)) / coord_factor
y1 = 720 + radius * math.sin(math.radians(angle + 10)) / coord_factor


clouds = []
for _ in range(cloud_count):
    x = random.randint(0, X)
    y = random.randint(0, Y-700)
    clouds.append((x, y))

song=0
sound.set_volume(0.02)
sound.play()

running = True
while running:

    #CIEL
    screen.fill((background_color))

    #NUAGE
    for x, y in clouds:
        nuage_image = pygame.image.load("saut/nuage.png")
        nuage_position = (x, y)
        screen.blit(nuage_image, nuage_position)

    #SOL
    pygame.draw.rect(screen, ground_color, (0, Y - 150, X, 150))
    pygame.draw.line(screen, border_color, (0, Y - 150), (X, Y - 150), 5)

    #TRIBUNES
    pygame.draw.rect(screen, (128,128,128), (0, 200 , X, 300))
    a=200
    for i in range (7):
        pygame.draw.rect(screen, (158,158,158), (0, a, X, 10))
        a+=50
    pygame.draw.rect(screen, (158,158,158), (0, 500, X, 125))
    pygame.draw.rect(screen, (158,158,158), (0, 160, X, 50))

    #LIGNE BLANCHE
    pygame.draw.rect(screen, (255,255,255), (0, 725, 1500, 10))
    pygame.draw.rect(screen, (255,255,255), (0, 650, 1500, 10))

    #LIGNE BLANCHE DIAGO
    pygame.draw.line(screen, (255,255,255), (s-100, 650), (s-150, 725), 35)

    #BAC A SABLE
    screen.blit(pygame.image.load("saut/sable.png"), (s,650))

    #SYMBOLE JO
    pygame.draw.arc(screen, (0, 0, 255), (b, 10, 100, 100), 0, 72, 5)# bleu
    pygame.draw.arc(screen, (255, 255, 0), (j, 60, 100, 100), 0, 72, 5)#jaune
    pygame.draw.arc(screen, (0, 0, 0), (n, 10, 100, 100), 0, 72, 5)#noir
    pygame.draw.arc(screen, (0, 255, 0), (v, 60, 100, 100), 0, 72, 5)#vert
    pygame.draw.arc(screen, (255, 0, 0), (r, 10, 100, 100), 0, 72, 5)#rouge

    #2024
    font = pygame.font.Font(None, 200)
    text = font.render("2024", True, (0, 0, 0))
    screen.blit(text, (q, 50))

    #SPECT
    for xs, ys in spect:
        personnage_image = pygame.image.load("saut/spect.png")
        personnage_position = (xs, ys)
        screen.blit(personnage_image, personnage_position)

    #PERSO COURT
    if court==True:
        image = pygame.image.load(f"saut/perso court/{index}.png")
        screen.blit(image, (xp-35 , yp))
        index += 1
        if index >= 8:
            index = 1
        if xp<=600:
            xp+=20
        song += 1
        if song >= 145:
            sound.set_volume(2)
            sound.play()
            song = 0


    #PERSO STOP
    if court==False:
        sound.stop()
        if saute==False:
            image = pygame.image.load(f"saut/perso saute/1.png")
            screen.blit(image, (xp,450))

        #CIBLE
        screen.blit(pygame.image.load("saut/cible.png"), (50,500))

        #AIGUILLE
        pygame.draw.line(screen, (0, 0, 0), (175, 718), (int(x1), int(y1)), 5)
        x1 = 175 + radius * math.cos(math.radians(angle + 10)) / coord_factor
        y1 = 720 + radius * math.sin(math.radians(angle + 10)) / coord_factor
        if saute==False:
            angle += speed
        if angle == 180:
            speed=-speed
        if angle == 340:
            speed=-speed
        #SCORE
        if score==True:
            if 600<=s<=1200:
                if angle == 260:
                    affiche_score=9.5
                elif 250<=angle<=270:
                    affiche_score=8.5
                elif 240<=angle<=280:
                    affiche_score=7.5
                elif 230<=angle<=290:
                    affiche_score=6.5
                elif 220<=angle<=300:
                    affiche_score=5.5
                elif 210<=angle<=310:
                    affiche_score=4.5
                elif 200<=angle<=320:
                    affiche_score=3.5
                elif 190<=angle<=330:
                    affiche_score=2.5
                elif 180<=angle<=340:
                    affiche_score=1.5
                affiche_score-=((s-860)/50)
            if s>1100:
                affiche_score='vous avez saute trop tot'
                if song==0:
                    sound1.set_volume(0.04)
                    sound1.play()
                    song+=1
            elif s<825:
                affiche_score='vous avez saute trop tard (mordu)'
                if song==0:
                    sound1.set_volume(0.04)
                    sound1.play()
                    song+=1
            elif affiche_score>=8.96:
                affiche_score="nouveau record du monde "+str(affiche_score)+"m"
                l_score=len(affiche_score)*10
                font = pygame.font.Font(None, 40)
                text = font.render("l'ancien record du monde etait de 8,95m et detenu par Mike Powell", True, (0, 0, 0))
                xx=(X/2.3)-l_score
                screen.blit(text, (xx, yy+60))
                if song==0:
                    mixer.Sound("saut/new_record.wav").play()
                    song+=1
            else:
                affiche_score=str(affiche_score)+"m"
            l_score=len(affiche_score)*10
            font = pygame.font.Font(None, 90)
            text = font.render(f"{affiche_score}", True, (0, 0, 0))
            xx=(X/2.3)-l_score
            screen.blit(text, (xx, yy))
            if song==0:
                mixer.Sound("saut/nice_jump.wav").play()
                song+=1
            #rejouer
            rejouer=True
            font = pygame.font.Font(None, 90)
            text = font.render("appuyer sur R pour recommencer", True, (255, 255, 255))
            screen.blit(text, (re, Y/2.8))
            text1 = font.render("et T pour retourner au lobby", True, (255, 255, 255))
            screen.blit(text1, (re, Y/2.3))
            re-=5
            if re<-1000:
                re=1450



    #PERSO SAUTE
    if saute ==True:
        xp1, yp1 = calculate_trajectory(t / 9 , h)
        if yp1<450:
            t+=3
        if xp1<=X/1.60:
            image = pygame.image.load(f"saut/perso saute/2.png")
            screen.blit(image, (xp1,yp1+5))
        elif X/1.60<=xp1<=X/1.5:
            image = pygame.image.load(f"saut/perso saute/3.png")
            screen.blit(image, (xp1,yp1+10))
        elif X/1.5<=xp1<=X/1.25:
            image = pygame.image.load(f"saut/perso saute/4.png")
            screen.blit(image, (xp1,yp1+15))
        elif xp1>=X/1.25:
            image = pygame.image.load(f"saut/perso saute/5.png")
            screen.blit(image, (xp1,yp1+20))
            score = True



    #MOUV
    if stop == False:
        #BAC A SABLE
        screen.blit(pygame.image.load("saut/sable.png"), (s,650))

        #LIGNE BLANCHE DIAGO
        pygame.draw.line(screen, (255,255,255), (s-100, 650), (s-150, 725), 35)
        s-=15
        if s<=0:
            stop =True
            court=False
            saute=True
        if xp>=600:
            #MOUV SPECT
            for i in range(len(spect)):
                xs, ys = spect[i]
                xs += dx-5
                if xs < -200:
                    xs = X
                spect[i] = (xs, ys)

            #2024
            screen.blit(text, (q, 50))
            q-=15
            if q==-350:
                q=1500

            #JO
            pygame.draw.arc(screen, (0, 0, 255), (b, 10, 100, 100), 0, 72, 5)# bleu
            pygame.draw.arc(screen, (255, 255, 0), (j, 60, 100, 100), 0, 72, 5)#jaune
            pygame.draw.arc(screen, (0, 0, 0), (n, 10, 100, 100), 0, 72, 5)#noir
            pygame.draw.arc(screen, (0, 255, 0), (v, 60, 100, 100), 0, 72, 5)#vert
            pygame.draw.arc(screen, (255, 0, 0), (r, 10, 100, 100), 0, 72, 5)#rouge
            b-=15
            j-=15
            n-=15
            v-=15
            r-=15
            if b==-350:
                b=1500
                j=1550
                n=1610
                v=1660
                r=1720

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.set_mode((0,0), FULLSCREEN)
            if event.key == pygame.K_ESCAPE:
                pygame.display.set_mode((0,0), RESIZABLE)
            if xp>=600:
                if event.key == pygame.K_SPACE:
                    stop = True
                    court = False
                    if ss==0:
                        song=0
                        ss+=1
                if event.key == pygame.K_UP and stop == True:
                    saute = True
            if rejouer==True:
                if event.key ==pygame.K_r:
                    running = False
                    with open("saut_en_longueur.py") as f:
                        exec(f.read())
                if event.key ==pygame.K_t:
                    running = False
                    with open("lobby.py") as f:
                        exec(f.read())



    pygame.display.flip()
    clock.tick(100)


pygame.quit()