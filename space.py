#importando libreria pygame
from turtle import distance
import pygame
import random
import math
from pygame import mixer

pygame.init()
screen_width = 800
screen_height = 600

size = (screen_width, screen_height)

screen = pygame.display.set_mode(size)

background = pygame.image.load("fondeespacio.jpg")

#Musica de fondo
mixer.music.load("fondo.wav")
mixer.music.play(-1)

bullet_sound = mixer.Sound("bala.wav")
bullet_sound.set_volume(0.5)

explotion_sound= mixer.Sound("explocion.wav")

#definir titulo
pygame.display.set_caption("Space Invaders")
#Icon
icon = pygame.image.load("universe.png")
pygame.display.set_icon(icon)

#Game over posicion
go_font= pygame.font.Font("VCR_OSD_MONO_1.001.ttf", 64)
go_x= 200
go_y= 250

#Personaje
player_x=370
player_y=480
player_img = pygame.image.load("rocket.png")
player_x_change = 0

enemy_img = []
enemy_x= []
enemy_y= []
enemy_x_change= []
enemy_y_change= []

numer_enemies=10

#enemigos
for item in range(numer_enemies):
    enemy_img.append(pygame.image.load("alien.png"))
    enemy_x.append(random.randint(0,735))
    enemy_y.append(random.randint(50,150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(20)

bullet_img = pygame.image.load("bala.png")
bullet_x=0
bullet_y=480
bullet_x_change=10
bullet_y_change=0.8
bullet_state="ready"

score=0 
score_font= pygame.font.Font("VCR_OSD_MONO_1.001.ttf", 32)

text_x= 10
text_y= 10

def show_text(x, y):
    score_text= score_font.render("Score : " + str(score), True, (255,255,255))
    screen.blit(score_text, (x,y))

def player(x,y):
    screen.blit(player_img, (x,y))

def enemy (x,y):
    screen.blit(enemy_img[item], (x,y))

def fire(x,y):
    global bullet_state
    bullet_state= "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision (enemy_x, enemy_y, bullet_x, bullet_y):
    distance= math.sqrt((enemy_x-bullet_x)**2 + (enemy_y-bullet_y)**2)

    if distance <27:
        return True
    else:
        return False

def game_over(x,y):
    go_text = go_font.render("GAME OVER!", True, (255,255,255))
    screen.blit(go_text, (x,y))

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.4
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.4
        if event.type==pygame.KEYUP:
            if event.key== pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change=0
            if event.key == pygame.K_SPACE:
                if bullet_state== "ready":
                    bullet_sound= mixer.Sound("bala.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                fire(player_x, bullet_y )

#fondo de la pantalla
    rgb= (26, 32, 50 )
    screen.fill(rgb)
    screen.blit(background, (0,0))
    player_x += player_x_change

    if player_x<=0:
        player_x=0
    elif player_x>=736:
        player_x = 736


    for item in range(numer_enemies):
        if enemy_y[item] >440:
            for j in range (numer_enemies):
                enemy_y[j]=2000
            game_over(go_x, go_y)
            break

        enemy_x[item] += enemy_x_change[item]

        if enemy_x[item] <= 0:
            enemy_x_change[item]= 0.5
            enemy_y[item] += enemy_y_change[item]

        elif enemy_x[item] >=736:
            enemy_x_change[item]=-0.3
            enemy_y[item]+= enemy_y_change[item]

        collision = is_collision(enemy_x[item], enemy_y[item], bullet_x, bullet_y)
        if collision:
            explotion_sound.play()
            bullet_y = 480
            bullet_state= "ready"
            score += 1
            print (score)
            enemy_x[item] = random.randint(0, 735)
            enemy_y[item]= random.randint(50, 150)
        enemy(enemy_x[item], enemy_y[item])
    if bullet_y <=0:
        bullet_y=480
        bullet_state = "ready" 

    if bullet_state == "fire":
        fire(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_text(text_x,text_y)
    
    pygame.display.update()



