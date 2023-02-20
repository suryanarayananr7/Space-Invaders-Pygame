import pygame
import random
import math
from pygame import mixer

# Initialize pygame.
pygame.init()

# Create window for the game.
screen = pygame.display.set_mode((800, 600))

# Add Background Image for the game.
background = pygame.image.load('background.png')

# Set Title and Icon for the game. [Get icon from flaticon.com size 32x32.]
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Setting player spaceship.
playerImg = pygame.image.load('player.png')

# Setting coordinates of player spaceship.
playerX = 370
playerY = 480
playerX_change = 0



# Setting enemy spaceship.
enemyImg = pygame.image.load('enemy.png')

# Setting coordinates of enemy spaceship.
enemyX = random.randint(0,730)
enemyY = random.randint(50,150)
enemyX_change = 5
enemyY_change = 40

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
# Setting Bullet for spaceship.
bulletImg = pygame.image.load('bullet.png')

# Setting coordinates of enemy spaceship.
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state="ready"

# Score
score_value=0
font = pygame.font.Font('freesansbold.ttf',32)

textx= 10
texty = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
# Ready state means we can't see bullet on the screen.
# Fire state means we can see the bullet moving on the screen.


# Ctrl+ALT+L to format code neatly.

# Function to blit/draw player or enemy.
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10)) # x+16 and y+10 are done so that the bullet comes out from the center of the spaceship.

def isCollision(x1, y1, x2, y2):
    distance =math.hypot(x1 - x2, y1 - y2)
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score = font.render("Score:"+ str(score_value), True, (255,255,255)) # Render score and set color of score to white.
    screen.blit(score, (x,y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# Game Loop for game to run.
running = True
while running:
    # Setting Background color for the game.
    screen.fill((0, 0, 0))  # Used to draw the screen for the game.

    # Draw background image to our game.
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # To perform movement of player either left or right.
        if event.type == pygame.KEYDOWN:  # KEYDOWN MEANS the key is being pressed.
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE: # Calls fire_bullet() function when space bar is pressed.
                if bullet_state=="ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:  # KEYUP means the pressed key is now released.
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Update player position after key is pressed.
    playerX += playerX_change

    # Setting boundary for the player.
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # [It is 736 because pixel size of spaceship is 64x64. Therefore 800-64=736].
        playerX = 736


    for i in range(num_of_enemies):

        # Gameover.
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # Update enemy movement position
        enemyX[i] +=enemyX_change[i]



        # Setting Enemy Movement.
        if enemyX[i] <=0:
            enemyX_change[i]=5 # Enemy moves right after hitting 0.
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]=-5 # Enemy moves left after hitting 0.
            enemyY[i]+=enemyY_change[i]
        # Collision
        x1 = enemyX[i]
        y1 = enemyY[i]
        collision = isCollision(x1, y1, bulletX, bulletY)
        if collision:
            collision_Sound = mixer.Sound('explosion.wav')
            collision_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 730)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)
    # Bullet Movement.
    if bulletY<=0:
        bulletY=480         # Position of bullet is resetted so that we can fire multiple bullets.
        bullet_state="ready"
    if bullet_state=="fire":
        fire_bullet(bulletX,bulletY)
        bulletY-=bulletY_change


    player(playerX, playerY)
    show_score(textx,texty)
    pygame.display.update()
