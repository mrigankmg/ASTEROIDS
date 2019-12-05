import sys
import pygame as pyg
import math
import random
import os

from pygame.gfxdraw import filled_circle

pyg.init()

WIDTH = 1280
HEIGHT = 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 202, 54)
ORANGE = (255, 136, 0)
LIGHT_GREY = (179, 179, 179)
GREEN = (17, 255, 0)
TEAL = (70, 189, 185)
TURN_SPEED = math.radians(5)
PLAYER_SIZE = 40
PLAYER_THRUST = 0.1
FRICTION = 0.01
NUM_ASTEROIDS = 3
ASTEROID_SPEED = 1
ASTEROID_SIZE = 133
ASTEROID_VERTICES = 10
ASTEROID_ROUGHNESS = 0.45
PLAYER_EXPLODE_DURATION = 30
PLAYER_INVINCIBILITY_DURATION = 150
PLAYER_BLINK_DURATION = 5
MAX_LASER = 8
LASER_SPEED = 7
LASER_DISTANCE = 0.35
LASER_EXPLODE_DURATION = 3
TEXT_SIZE = 80
MAX_TEXT_DURATION = 60
TEXT_ALPHA_SPEED = 2.5
SCORE_TEXT_SIZE = 40
MAX_LIVES = 3
FONT_STYLE = 'trench100free.ttf'
LRG_ASTEROID_POINTS = 5
MED_ASTEROID_POINTS = 10
SML_ASTEROID_POINTS = 20
HIGH_SCORE_FILE = "high_score.txt"

### developer flags ###
SHOW_CENTROID = False
SHOW_BOUNDING = False

class Player:
  def __init__(self, x, y, size, angle):
    self.pos = [x, y]
    self.size = size
    self.radius = size/2
    self.angle = math.radians(angle)
    self.rotation = 0
    self.is_thrusting = False
    self.thrust = [0, 0]
    self.explodeTime = 0
    self.blinkTime = PLAYER_BLINK_DURATION
    self.blinkNum = PLAYER_INVINCIBILITY_DURATION/PLAYER_BLINK_DURATION
    self.canShoot = True
    self.lasers = []
    self.dead = False

class Asteroid:
  def __init__(self, x, y, size):
    self.speed_multiplier = 1 + 0.15 * level
    self.pos = [x, y]
    self.xv = random.random() * ASTEROID_SPEED * self.speed_multiplier * (1 if random.random() < 0.5 else -1)
    self.yv = random.random() * ASTEROID_SPEED * self.speed_multiplier * (1 if random.random() < 0.5 else -1)
    self.size = size
    self.radius = math.ceil(size/2)
    self.angle =  math.radians(random.random() * 360)
    self.vertices = math.floor(random.random() * (ASTEROID_VERTICES + 1) + ASTEROID_VERTICES/2)
    self.offsets = [random.random() * ASTEROID_ROUGHNESS * 2 + 1 - ASTEROID_ROUGHNESS for i in range(self.vertices)]

class Laser:
    def __init__(self, x, y):
        self.pos = [x, y]
        self.xv = LASER_SPEED * math.cos(player.angle)
        self.yv = -LASER_SPEED * math.sin(player.angle)
        self.distance = 0
        self.explodeTime = 0

def createAsteroids():
    asteroids = []
    for i in range(NUM_ASTEROIDS + level):
        while True:
            x = math.floor(random.random() * WIDTH)
            y = math.floor(random.random() * HEIGHT)
            distance_to_player = ((player.pos[0] - x) ** 2 + (player.pos[1] - y) ** 2) ** 0.5
            if distance_to_player >= ASTEROID_SIZE * 2 + player.radius:
                break
        asteroids.append(Asteroid(x, y, ASTEROID_SIZE))
    return asteroids

def newGame():
    global player, level, lives, score, highScore
    score = 0
    level = 0
    if not os.path.exists('./' + HIGH_SCORE_FILE):
       highScore = 0
    else:
        file_in = open('./' + HIGH_SCORE_FILE, 'r')
        highScore = int(file_in.read())
        file_in.close()
    lives = MAX_LIVES
    player = Player(WIDTH/2, HEIGHT/2, PLAYER_SIZE, 90)
    newLevel()

def newLevel():
    global asteroids, text, text_alpha, level, text_fade_in, text_duration
    text_fade_in = True
    text_alpha = 2.5
    text_duration = MAX_TEXT_DURATION
    asteroids = createAsteroids()

newGame()
screen = pyg.display.set_mode((WIDTH, HEIGHT))
score_font = pyg.font.Font(FONT_STYLE, 40)
pyg.display.set_caption('Asteroids Neural Network')

def drawPlayer(x, y, angle, radius, color):
    ##### player coordinate and angle update #####
    player_tip = (x + 4/3 * radius * math.cos(angle), y - 4/3 * radius * math.sin(angle))
    player_rear_left = (x - radius * (2/3 * math.cos(angle) + math.sin(angle)), y + radius * (2/3 * math.sin(angle) - math.cos(angle)))
    player_rear_right = (x - radius * (2/3 * math.cos(angle) - math.sin(angle)), y + radius * (2/3 * math.sin(angle) + math.cos(angle)))
    ##### draw player #####
    pyg.draw.line(screen, color, player_tip, player_rear_left, width=player.size//15)
    pyg.draw.line(screen, color, player_rear_left, player_rear_right, width=player.size//15)
    pyg.draw.line(screen, color, player_tip, player_rear_right, width=player.size//15)

def shootLaser():
    if player.canShoot and len(player.lasers) < MAX_LASER:
        player.lasers.append(Laser(player.pos[0] + 4/3 * player.radius * math.cos(player.angle), player.pos[1] - 4/3 * player.radius * math.sin(player.angle)))
    player.canShoot = False

def explodePlayer():
    player.explodeTime = PLAYER_EXPLODE_DURATION

def destroyAsteroid(index):
    global asteroids, level, score, highScore
    if asteroids[index].size > ASTEROID_SIZE/4:
        if asteroids[index].size == ASTEROID_SIZE:
            score += LRG_ASTEROID_POINTS
        else:
            score += MED_ASTEROID_POINTS
        asteroids.append(Asteroid(asteroids[index].pos[0], asteroids[index].pos[1], asteroids[index].size/2))
        asteroids.append(Asteroid(asteroids[index].pos[0], asteroids[index].pos[1], asteroids[index].size/2))
    else:
        score += SML_ASTEROID_POINTS
    if score > highScore:
        highScore = score
    asteroids = asteroids[:index] + asteroids[index + 1:]
    if len(asteroids) == 0:
        level += 1
        newLevel()

def gameOver():
    global text_alpha, text_fade_in, score, highScore
    if score == highScore:
        file_out = open('./' + HIGH_SCORE_FILE, 'w')
        file_out.write(str(highScore))
        file_out.close()
    player.dead = True
    text_alpha = 2.5
    text_fade_in = True

while True:
    blinkOn = player.blinkNum % 2 == 0
    exploding = player.explodeTime > 0
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            if score == highScore:
                file_out = open('./' + HIGH_SCORE_FILE, 'w')
                file_out.write(str(highScore))
                file_out.close()
            sys.exit()
    keys_pressed = pyg.key.get_pressed()
    if keys_pressed[pyg.K_ESCAPE]:
        if score == highScore:
            file_out = open('./' + HIGH_SCORE_FILE, 'w')
            file_out.write(str(highScore))
            file_out.close()
        sys.exit()
    if not player.dead:
        if keys_pressed[pyg.K_UP]:
            player.is_thrusting = True
        else:
            player.is_thrusting = False
        if keys_pressed[pyg.K_RIGHT]:
            player.rotation = -TURN_SPEED
        if keys_pressed[pyg.K_LEFT]:
            player.rotation = TURN_SPEED
        if not(keys_pressed[pyg.K_LEFT] or keys_pressed[pyg.K_RIGHT]):
            player.rotation = 0
        if not exploding:
            if keys_pressed[pyg.K_SPACE]:
                shootLaser()
            else:
                player.canShoot = True
    screen.fill(BLACK)
    if player.is_thrusting and not player.dead:
        player.thrust[0] += PLAYER_THRUST * math.cos(player.angle)
        player.thrust[1] -= PLAYER_THRUST * math.sin(player.angle)
        fire_tip = (player.pos[0] - 5/3 * player.radius * math.cos(player.angle), player.pos[1] + 5/3 * player.radius * math.sin(player.angle))
        fire_rear_left = (player.pos[0] - player.radius * (2/3 * math.cos(player.angle) + 0.5 * math.sin(player.angle)), player.pos[1] + player.radius * (2/3 * math.sin(player.angle) - 0.5 * math.cos(player.angle)))
        fire_rear_right = (player.pos[0] - player.radius * (2/3 * math.cos(player.angle) - 0.5 * math.sin(player.angle)), player.pos[1] + player.radius * (2/3 * math.sin(player.angle) + 0.5 * math.cos(player.angle)))
        if not exploding and blinkOn:
            ##### draw fire #####
            pyg.draw.polygon(screen, YELLOW, [fire_tip, fire_rear_left, fire_rear_right])
            pyg.draw.line(screen, ORANGE, fire_tip, fire_rear_left, width=player.size//12)
            pyg.draw.line(screen, ORANGE, fire_rear_left, fire_rear_right, width=player.size//12)
            pyg.draw.line(screen, ORANGE, fire_tip, fire_rear_right, width=player.size//12)
    else:
        player.thrust[0] -= FRICTION * player.thrust[0]
        player.thrust[1] -= FRICTION * player.thrust[1]

    if not exploding:
        if blinkOn and not player.dead:
            drawPlayer(player.pos[0], player.pos[1], player.angle, player.radius, TEAL)
        if player.blinkNum > 0:
            player.blinkTime -= 1
            if player.blinkTime == 0:
                player.blinkTime = PLAYER_BLINK_DURATION
                player.blinkNum -= 1
    else:
        ##### draw explosion #####
        filled_circle(screen, int(player.pos[0]), int(player.pos[1]), int(player.radius * 1.5), RED)
        filled_circle(screen, int(player.pos[0]), int(player.pos[1]), int(player.radius * 1.2), ORANGE)
        filled_circle(screen, int(player.pos[0]), int(player.pos[1]), int(player.radius * 0.9), YELLOW)
        filled_circle(screen, int(player.pos[0]), int(player.pos[1]), int(player.radius * 0.6), WHITE)

    ##### draw asteroids #####
    for ast in asteroids:
        for i in range(ast.vertices):
            start = (ast.pos[0] + ast.radius * ast.offsets[i] * math.cos(ast.angle + i * math.pi * 2 / ast.vertices), ast.pos[1] + ast.radius * math.sin(ast.angle + i * math.pi * 2 / ast.vertices))
            if i == ast.vertices - 1:
                end = (ast.pos[0] + ast.radius * ast.offsets[0] * math.cos(ast.angle), ast.pos[1] + ast.radius * math.sin(ast.angle))
            else:
                end = (ast.pos[0] + ast.radius * ast.offsets[i + 1] * math.cos(ast.angle + (i + 1) * math.pi * 2 / ast.vertices), ast.pos[1] + ast.radius * math.sin(ast.angle + (i + 1) * math.pi * 2 / ast.vertices))
            pyg.draw.line(screen, LIGHT_GREY, start, end, width=player.size//15)
            if SHOW_BOUNDING:
                pyg.draw.circle(screen, GREEN, ast.pos, ast.radius, width=player.size//15)

    if SHOW_CENTROID:
        pyg.draw.rect(screen, WHITE, (player.pos[0]-1, player.pos[1]-1, 2, 2))

    if SHOW_BOUNDING:
        pyg.draw.circle(screen, GREEN, player.pos, player.radius, width=player.size//15)

    for laser in player.lasers:
        if laser.explodeTime == 0:
            pyg.draw.circle(screen, WHITE, laser.pos, PLAYER_SIZE/15)
        else:
            filled_circle(screen, int(laser.pos[0]), int(laser.pos[1]), int(player.radius * 0.5), ORANGE)
            filled_circle(screen, int(laser.pos[0]), int(laser.pos[1]), int(player.radius * 0.25), YELLOW)

    if text_alpha > 0:
        font = pyg.font.Font(FONT_STYLE, TEXT_SIZE)
        if not player.dead:
            text = font.render('LEVEL ' + str(level), True, WHITE)
            position = text.get_rect(center=(WIDTH/2, HEIGHT * 0.75))
        else:
            text = font.render('GAME OVER', True, WHITE)
            position = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        text.set_alpha(text_alpha)
        screen.blit(text, position)
        if text_fade_in:
            text_alpha += TEXT_ALPHA_SPEED
            if text_alpha == 255:
                text_fade_in = False
        elif text_duration > 0:
            text_duration -= 1
        if text_duration == 0:
            text_alpha -= TEXT_ALPHA_SPEED
            if text_alpha == 0:
                text_duration = MAX_TEXT_DURATION
    elif player.dead:
        newGame()

    score_text = score_font.render('SCORE: ' + str(score), True, WHITE)
    screen.blit(score_text, (player.size/2, player.size/2.5))

    high_score_text = score_font.render('TOP SCORE: ' + str(highScore), True, WHITE)
    position = high_score_text.get_rect(center=(WIDTH/2, player.size))
    screen.blit(high_score_text, (position[0], player.size/2.5))

    for i in range(lives):
        color = RED if exploding and i == lives - 1 else WHITE
        drawPlayer(WIDTH - PLAYER_SIZE - i * PLAYER_SIZE * 1.3, PLAYER_SIZE * 1.2, math.radians(90), player.size/2.5, color)

    for i in range(len(asteroids) - 1, -1, -1):
        for j in range(len(player.lasers) - 1, -1, -1):
            if player.lasers[j].explodeTime == 0 and ((player.lasers[j].pos[0] - asteroids[i].pos[0]) ** 2 + (player.lasers[j].pos[1] - asteroids[i].pos[1]) ** 2) ** 0.5 < asteroids[i].radius:
                destroyAsteroid(i)
                player.lasers[j].explodeTime = math.ceil(LASER_EXPLODE_DURATION)
                break

    if not exploding:
        if player.blinkNum == 0 and not player.dead:
            for i in range(len(asteroids) - 1, -1, -1):
                distance_to_player = ((player.pos[0] - asteroids[i].pos[0]) ** 2 + (player.pos[1] - asteroids[i].pos[1]) ** 2) ** 0.5
                if distance_to_player < asteroids[i].radius + player.radius:
                    destroyAsteroid(i)
                    explodePlayer()
                    break
        player.angle += player.rotation
        player.pos[0] += player.thrust[0]
        player.pos[1] += player.thrust[1]
    else:
        player.explodeTime -= 1
        if player.explodeTime == 0:
            lives -= 1
            if lives > 0:
                player = Player(WIDTH/2, HEIGHT/2, PLAYER_SIZE, 90)
            else:
                gameOver()

    ##### player back on screen when gone off screen #####
    if player.pos[0] < -player.radius:
        player.pos[0] = WIDTH + player.radius
    elif player.pos[0] > WIDTH + player.radius:
        player.pos[0] = -player.radius
    if player.pos[1] < -player.radius:
        player.pos[1] = HEIGHT + player.radius
    elif player.pos[1] > HEIGHT + player.radius:
        player.pos[1] = -player.radius

    for i in range(len(player.lasers) - 1, -1, -1):
        if player.lasers[i].distance > LASER_DISTANCE * WIDTH:
            player.lasers = player.lasers[:i] + player.lasers[i + 1:]
        else:
            if player.lasers[i].explodeTime > 0:
                player.lasers[i].explodeTime -= 1
                if player.lasers[i].explodeTime == 0:
                    player.lasers = player.lasers[:i] + player.lasers[i + 1:]
            else:
                player.lasers[i].pos[0] += player.lasers[i].xv
                player.lasers[i].pos[1] += player.lasers[i].yv
                player.lasers[i].distance += (player.lasers[i].xv ** 2 + player.lasers[i].yv ** 2) ** 0.5
                if player.lasers[i].pos[0] < 0:
                    player.lasers[i].pos[0] = WIDTH
                elif player.lasers[i].pos[0] > WIDTH:
                    player.lasers[i].pos[0] = 0
                if player.lasers[i].pos[1] < 0:
                    player.lasers[i].pos[1] = HEIGHT
                elif player.lasers[i].pos[1] > HEIGHT:
                    player.lasers[i].pos[1] = 0

    for ast in asteroids:
        ast.pos[0] += ast.xv
        ast.pos[1] += ast.yv
        ##### asteroids back on screen when gone off screen #####
        if ast.pos[0] < -ast.radius:
            ast.pos[0] = WIDTH + ast.radius
        elif ast.pos[0] > WIDTH + ast.radius:
            ast.pos[0] = -ast.radius
        if ast.pos[1] < -ast.radius:
            ast.pos[1] = HEIGHT + ast.radius
        elif ast.pos[1] > HEIGHT + ast.radius:
            ast.pos[1] = -ast.radius

    pyg.display.flip()
