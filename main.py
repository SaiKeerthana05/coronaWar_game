import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init()

#initialize the game window
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Corona War")
logo = pygame.image.load("coronavirus.png")
pygame.display.set_icon(logo)
background = pygame.image.load("background.jpg")
player_img = pygame.image.load("healthWorker.png")
playerX = 700
playerY = 500
playerX_change = 0
num_of_enemies = 10
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("coronavirus.png"))
    enemyX.append(random.randint(0, 768))
    enemyY.append(random.randint(0, 440))
    enemyX_change.append(1.3)
syringe_img = pygame.image.load("syringe.png")
syringeX = 0
syringeY = 500
syringeY_change = 3
syringe_state = "ready"
score_value = 0
scoreX = 0
scoreY = 0
font = pygame.font.Font("freesansbold.ttf",32)
over_font = pygame.font.Font("freesansbold.ttf",55)

def player(x,y):
    screen.blit(player_img,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_img[i],(x,y))

def release_syringe(x,y):
    global syringe_state
    syringe_state = "release"
    screen.blit(syringe_img,(x,y))

def is_collision(x1,x2,y1,y2):
    distance = math.sqrt((math.pow((x1-x2),2))+(math.pow((y1-y2),2)))
    if distance < 27 : return True
    else: return False

def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,(0,0,0))
    screen.blit(score,(x,y))

def game_over():
    game_over_text = over_font.render("GAME OVER",True,(0,0,0))
    screen.blit(game_over_text,(245,275))

running = True
while running:
    screen.fill((204,255,204))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 2.5
            if event.key == pygame.K_SPACE:
                if syringe_state == "ready":
                    syringe_sound = mixer.Sound("Syringe.wav")
                    syringe_sound.play()
                    syringeX = playerX
                    release_syringe(syringeX, syringeY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    if score_value//5 <= 9:num_of_enemies = (score_value//5)+1
    else : num_of_enemies = 10
    playerX += playerX_change
    if syringe_state == "release":
        release_syringe(syringeX,syringeY)
        syringeY -= syringeY_change
    for k in range(num_of_enemies):
        if enemyY[k] >= 470:
            for i in range(num_of_enemies):
                enemyY[i] = 2000
            playerY = 2000
            syringeY += syringeY_change
            game_over()
        collision = is_collision(enemyX[k],syringeX,enemyY[k],syringeY)
        if collision is True :
            blast = mixer.Sound("Blast.wav")
            blast.play()
            score_value += 1
            enemyX[k] = random.randint(0, 768)
            enemyY[k] = random.randint(0, 450)

        if enemyX[k] < 0:
            enemyX[k] = 0
            enemyY[k] += 8
            enemyX_change[k] = 1.3
        if enemyX[k] > 768:
            enemyX[k] = 768
            enemyY[k] += 8
            enemyX_change[k] = -1.3
        enemyX[k] += enemyX_change[k]
        enemy(enemyX[k],enemyY[k],k)

    if playerX < 0 : playerX = 0
    if playerX > 768 : playerX = 768
    if syringeY <=0 :
        syringeY = 500
        syringe_state = "ready"
    player(playerX,playerY)
    show_score(scoreX,scoreY)
    pygame.display.update()
