import sys
import pygame as pyg
from pygame.gfxdraw import filled_circle
import math
import random

pyg.init()

WIDTH = 1280
HEIGHT = 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (181, 248, 255)
RED = (255, 0, 0)
YELLOW = (255, 202, 54)
ORANGE = (255, 136, 0)
LIGHT_GREY = (179, 179, 179)
GREEN = (17, 255, 0)
TEXT_POS = (25, 15)
TURN_SPEED = math.radians(10)
PLAYER_SIZE = 40
PLAYER_THRUST = 0.1 #acceleration of ship in px/s
FRICTION = 0.01
NUM_ASTEROIDS = 5
ASTEROID_SPEED = 1
ASTEROID_SIZE = 100
ASTEROID_VERTICES = 10
ASTEROID_ROUGHNESS = 0.37
PLAYER_EXPLODE_DURATION = 15
PLAYER_INVINCIBILITY_DURATION = 150
PLAYER_BLINK_DURATION = 5

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

class Asteroid:
  def __init__(self, x, y, size):
    self.pos = [x, y]
    self.xv = random.random() * ASTEROID_SPEED * (1 if random.random() < 0.5 else -1)
    self.yv = random.random() * ASTEROID_SPEED * (1 if random.random() < 0.5 else -1)
    self.size = size
    self.radius = size/2
    self.angle =  math.radians(random.random() * 360)
    self.vertices = math.floor(random.random() * (ASTEROID_VERTICES + 1) + ASTEROID_VERTICES/2)
    self.offset = [random.random() * ASTEROID_ROUGHNESS * 2 + 1 - ASTEROID_ROUGHNESS for i in range(self.vertices)]

asteroids = []
player = Player(WIDTH/2, HEIGHT/2, PLAYER_SIZE, 90)
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption('Asteroids Neural Network')
font = pyg.font.Font('trench100free.ttf', 40)
text = font.render('SCORE:', True, WHITE, BLACK)

def createAsteroidBelt():
    global asteroids
    asteroids = []
    for i in range(NUM_ASTEROIDS):
        while True:
            x = math.floor(random.random() * WIDTH)
            y = math.floor(random.random() * HEIGHT)
            distance_to_player = ((player.pos[0] - x) ** 2 + (player.pos[1] - y) ** 2) ** 0.5
            if distance_to_player >= ASTEROID_SIZE * 2 + player.radius:
                break
        asteroids.append(Asteroid(x, y, ASTEROID_SIZE))

createAsteroidBelt()

def explodePlayer():
    player.explodeTime = PLAYER_EXPLODE_DURATION

while True:
    blinkOn = player.blinkNum % 2 == 0
    exploding = player.explodeTime > 0
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            sys.exit()
    ##### player coordinate and angle update #####
    player_tip = (player.pos[0] + 4/3 * player.radius * math.cos(player.angle), player.pos[1] - 4/3 * player.radius * math.sin(player.angle))
    player_rear_left = (player.pos[0] - player.radius * (2/3 * math.cos(player.angle) + math.sin(player.angle)), player.pos[1] + player.radius * (2/3 * math.sin(player.angle) - math.cos(player.angle)))
    player_rear_right = (player.pos[0] - player.radius * (2/3 * math.cos(player.angle) - math.sin(player.angle)), player.pos[1] + player.radius * (2/3 * math.sin(player.angle) + math.cos(player.angle)))
    keys_pressed = pyg.key.get_pressed()
    if keys_pressed[pyg.K_ESCAPE]:
        sys.exit()
    else:
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
        if keys_pressed[pyg.K_SPACE]:
            pass
    screen.fill(BLACK)
    if player.is_thrusting:
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
        if blinkOn:
            ##### draw player #####
            pyg.draw.line(screen, LIGHT_BLUE, player_tip, player_rear_left, width=player.size//15)
            pyg.draw.line(screen, LIGHT_BLUE, player_rear_left, player_rear_right, width=player.size//15)
            pyg.draw.line(screen, LIGHT_BLUE, player_tip, player_rear_right, width=player.size//15)
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
            start = (ast.pos[0] + ast.radius * ast.offset[i] * math.cos(ast.angle + i * math.pi * 2 / ast.vertices), ast.pos[1] + ast.radius * math.sin(ast.angle + i * math.pi * 2 / ast.vertices))
            if i == ast.vertices - 1:
                end = (ast.pos[0] + ast.radius * ast.offset[0] * math.cos(ast.angle), ast.pos[1] + ast.radius * math.sin(ast.angle))
            else:
                end = (ast.pos[0] + ast.radius * ast.offset[i + 1] * math.cos(ast.angle + (i + 1) * math.pi * 2 / ast.vertices), ast.pos[1] + ast.radius * math.sin(ast.angle + (i + 1) * math.pi * 2 / ast.vertices))
            pyg.draw.line(screen, LIGHT_GREY, start, end, width=player.size//15)
            if SHOW_BOUNDING:
                pyg.draw.circle(screen, GREEN, (ast.pos[0], ast.pos[1]), ast.radius, width=player.size//15)

    if SHOW_CENTROID:
        pyg.draw.rect(screen, WHITE, (player.pos[0]-1, player.pos[1]-1, 2, 2))

    if SHOW_BOUNDING:
        pyg.draw.circle(screen, GREEN, (player.pos[0], player.pos[1]), player.radius, width=player.size//15)

    if not exploding:
        if player.blinkNum == 0:
            for ast in asteroids:
                distance_to_player = ((player.pos[0] - ast.pos[0]) ** 2 + (player.pos[1] - ast.pos[1]) ** 2) ** 0.5
                if distance_to_player < ast.radius + player.radius:
                    explodePlayer()
        player.angle += player.rotation
        player.pos[0] += player.thrust[0]
        player.pos[1] += player.thrust[1]
    else:
        player.explodeTime -= 1
        if player.explodeTime == 0:
            player = Player(WIDTH/2, HEIGHT/2, PLAYER_SIZE, 90)

    ##### player back on screen when gone off screen #####
    if player.pos[0] < -player.radius:
        player.pos[0] = WIDTH + player.radius
    elif player.pos[0] > WIDTH + player.radius:
        player.pos[0] = -player.radius
    if player.pos[1] < -player.radius:
        player.pos[1] = HEIGHT + player.radius
    elif player.pos[1] > HEIGHT + player.radius:
        player.pos[1] = -player.radius

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

    screen.blit(text, TEXT_POS)
    pyg.display.flip()
