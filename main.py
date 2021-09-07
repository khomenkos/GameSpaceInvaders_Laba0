import pygame
import random
import math
from pygame import mixer

pygame.init()

# create the screen
win = pygame.display.set_mode((500, 500))

# Caption and Icon

pygame.display.set_caption("Space Invader")
icon = pygame.image.load("Spacecraft.png")
pygame.display.set_icon(icon)

bg = pygame.image.load("bg.png")

# Sound

mixer.music.load("game_sound.wav")
mixer.music.play(-1)

# Player

playerImg = pygame.image.load("1.png")
playerX = 220
playerY = 400
playerX_change = 0

#Monsters
monsterImg = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
countMonsters = 6

for i in range(countMonsters):
    monsterImg.append(pygame.image.load("monster.png"))
    monsterX.append(random.randint(0, 436))
    monsterY.append(random.randint(50, 150))
    monsterX_change.append(0.7)
    monsterY_change.append(40)

#Bullet

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 400
bulletX_change = 0
bulletY_change = 3
bulletState = "ready"

# Score

scoreVAL = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 40)

def show_score(x, y):
    score = font.render("Score : " + str(scoreVAL), True, (255, 255, 255))
    win.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    win.blit(over_text, (130, 250))

def player(x, y):
    win.blit(playerImg, (x, y ))

def monster(x, y, i):
    win.blit(monsterImg[i], (x, y ))

def shot_bullet(x, y):
    global bulletState
    bulletState = "fire"
    win.blit(bulletImg, (x + 16, y + 10))

def isCollision(monterX, monsterY, bulletX, bulletY):
    distance = math.sqrt(math.pow(monterX - bulletX, 2) + (math.pow(monsterY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

run = True
while(run):

    win.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    bulletSound = mixer.Sound("shoot.wav")
                    bulletSound.play()
                    bulletX = playerX
                    shot_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

#Player move

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 436:
        playerX = 436

#Monsters Move

    for i in range(countMonsters):

        # Game Over
        if monsterY[i] > 340:
            for j in range(countMonsters):
                monsterY[j] = 2000
            game_over_text()
            break

        monsterX[i] += monsterX_change[i]
        if monsterX[i] <= 0:
            monsterX_change[i] = 0.7
            monsterY[i] += monsterY_change[i]
        elif monsterX[i] >= 436:
            monsterX_change[i] = -0.7
            monsterY[i] += monsterY_change[i]

# collision
        collision = isCollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("crash.wav")
            explosionSound.play()
            bulletY = 380
            bulletState = "ready"
            scoreVAL += 1
            monsterX[i] = random.randint(0, 436)
            monsterY[i] = random.randint(50, 150)

        monster(monsterX[i], monsterY[i], i)

# Bullet move

    if bulletY <= 0:
        bulletY = 380
        bulletState = "ready"
    if bulletState == "fire":
        shot_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

##pygame.quit()
