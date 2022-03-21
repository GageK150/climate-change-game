import math
import random

import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((600, 400))



# Background Sound

mixer.music.load('Battle-Revamp.mid')
mixer.music.play(-1)



# Title and icon
pygame.display.set_caption("Defender of The Blue")
icon = pygame.image.load("Submarine of Vengeance.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Protagonist.png')
playerX = 250
playerY = 300
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Antagonist.png'))
    enemyX.append(random.randint(0, 500))
    enemyY.append(random.randint(10, 100))
    enemyX_change.append(0.1)
    enemyY_change.append(20)

# Energy Blast

# Ready - You can't see the bullet state on the screen
# Fire - The blast is currently moving
energyblastImg = pygame.image.load('energy-blasts.png')
energyblastX = 0
energyblastY = 300
energyblastX_change = 0
energyblastY_change = 1
energyblast_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10
game_over_font = pygame.font.Font('freesansbold.ttf',50)
# Game Over Text

def show_score(x,y):
    score = font.render("Score :" + str(score_value),True, (250,100,0))
    screen.blit(score, (x, y))

def game_over_text():
    game_over_text = game_over_font.render("GAME OVER",True, (250,0,0))
    screen.blit(game_over_text, (150, 100))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_energyblast(x, y):
    global energyblast_state
    energyblast_state = "fire"
    screen.blit(energyblastImg, (x + -1, y + 10))


def isCollison(enemyX, enemyY, energyblastX, energyblastY):
    distance = math.sqrt((math.pow(enemyX - energyblastX, 2)) + (math.pow(enemyY - energyblastY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 128))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE:
                if energyblast_state is "ready":
                    energyblast_sound = mixer.Sound('Energy Blast.mp3')
                    energyblast_sound.play()
                    # Get the current x coordinate of the submarine
                    energyblastX = playerX
                    fire_energyblast(energyblastX, energyblastY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    # Checking for boundaries of submarine so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 500:
        playerX = 500

    # enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 272:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 500:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collison = isCollison(enemyX[i], enemyY[i], energyblastX, energyblastY)
        if collison:
            explosion_Sound = mixer.Sound('Explode.mp3')
            explosion_Sound.play()
            energyblastY = 300
            energyblast_state = "ready"
            score_value += 50
            enemyX[i] = random.randint(0, 500)
            enemyY[i] = random.randint(10, 100)

        enemy(enemyX[i],enemyY[i], i)

    # energy blast movement
    if energyblastY <= 0:
        energyblastY = 300
        energyblast_state = "ready"

    if energyblast_state is "fire":
        fire_energyblast(energyblastX, energyblastY)
        energyblastY -= energyblastY_change


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
