# -*- coding: utf-8 -*-
import pygame
import random
import math
from pygame import mixer

#create a class "alien" with a class variable alive, then,
#if alive is True: the enemy is blitted on to the screen, else, the enemy is not.

#initialize the pygame
pygame.init()

#create the screen with size
screen = pygame.display.set_mode((800, 600))

#Title and Icon
pygame.display.set_caption("Quebrada Invaders")
icon = pygame.image.load('logo.png')
pygame.display.set_icon(icon)

#Background
background = pygame.image.load('bkg.png')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy 1
enemy1Img = []
enemy1X = []
enemy1Y = []
enemy1X_change = []
enemy1Y_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemy1Img.append(pygame.image.load('t1.png'))
    enemy1X.append(random.randint(0,735))
    enemy1Y.append(random.randint(50,150))
    enemy1X_change.append(5)
    enemy1Y_change.append(40)

# Pokeball
pokeballImg = pygame.image.load('pokeball.png')
pokeballX = 0
pokeballY = 480
pokeballX_change = 0
pokeballY_change = 10
pokeball_state = "ready"

#Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 222
textY = 10

#Game Over text

over_font = pygame.font.Font('8-BIT.TTF', 64)

def show_score(x, y):
    score = font.render("PONTOS :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (125, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy1(x, y, i):
    screen.blit(enemy1Img[i], (x, y))

def fire_pokeball(x, y):
    global pokeball_state
    pokeball_state = "fire"
    screen.blit(pokeballImg, (x + 16, y + 10))

def isCollision(enemy1X, enemy1Y, pokeballX, pokeballY):
    distance = math.sqrt(math.pow(enemy1X-pokeballX,2) + (math.pow(enemy1Y-pokeballY,2)))
    if distance < 27:
        return True
    else:
        return False



#Game mechanics while game running
running = True
while running:

    # RGB
    screen.fill((0, 128, 128))
    #bg image
    screen.blit(background, (0, 0))

#continue of the command for close the game on 'X'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #keyboard movement
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -7
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_SPACE:
                if pokeball_state is "ready":
                    pokeball_Sound = mixer.Sound('shot.wav')
                    pokeball_Sound.play()
                    #get the x cordinate of the spaceship
                    fire_pokeball(playerX, pokeballY)
                    pokeballX = playerX

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #checking for boundaries for spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    #enemy movement
    for i in range(num_of_enemies):

        #Game Over
        if enemy1Y[i] > 440:
            mixer.music.stop()
            over_Sound = mixer.Sound('GameOver.wav')
            over_Sound.play()
            for j in range(num_of_enemies):
                enemy1Y[j] = 2000
            game_over_text()
            break

        enemy1X[i] += enemy1X_change[i]
        if enemy1X[i] <= 0:
            enemy1X_change[i] = 4
            enemy1Y[i] += enemy1Y_change[i]
        elif enemy1X[i] >= 736:
            enemy1X_change[i] = -4
            enemy1Y[i] += enemy1Y_change[i]
        # Collision
        collision = isCollision(enemy1X[i], enemy1Y[i], pokeballX, pokeballY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            pokeballY = 480
            pokeball_state = "ready"
            score_value += 1
            enemy1X[i] = random.randint(0,735)
            enemy1Y[i] = random.randint(50,150)

        enemy1(enemy1X[i], enemy1Y[i], i)

    #bullet movement
    if pokeballY <= 0:
        pokeballY = 480
        pokeball_state = "ready"

    if pokeball_state is "fire":
        fire_pokeball(pokeballX, pokeballY)
        pokeballY -= pokeballY_change



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
