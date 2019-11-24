import sys
import pygame as pyg
import math
import random

pyg.init()

WIDTH = 1280
HEIGHT = 720
BACKGROUND_COLOR = (0, 0, 0) #Black
TEXT_COLOR = (255, 255, 255) #White
PLAYER_COLOR = (245, 66, 66) #Red
FIRE_FILL_COLOR = (255, 202, 54) #Yellow
FIRE_OUTLINE_COLOR = (255, 136, 0) #Orange
ASTEROID_COLOR = (235, 235, 235) #Light Grey
TEXT_POS = (25, 15)
TURN_SPEED = math.radians(10)
PLAYER_SIZE = 40
PLAYER_THRUST = 0.1 #acceleration of ship in px/s
FRICTION = 0.01
NUM_ASTEROIDS = 3
ASTEROID_SPEED = 1
ASTEROID_SIZE = 100
ASTEROID_VERTICES = 10

class Player:
  def __init__(self, x, y, size, angle):
    self.pos = [x, y]
    self.size = size
    self.radius = size/2
    self.angle = math.radians(angle)
    self.rotation = 0
    self.is_thrusting = False
    self.thrust = [0, 0]

class Asteroid:
  def __init__(self, x, y, size):
    self.pos = [x, y]
    self.xv = random.random() * ASTEROID_SPEED * (1 if random.random() < 0.5 else -1)
    self.yv = random.random() * ASTEROID_SPEED * (1 if random.random() < 0.5 else -1)
    self.size = size
    self.radius = size/2
    self.angle =  math.radians(random.random() * 360)
    self.vertices = math.floor(random.random() * (ASTEROID_VERTICES + 1) + ASTEROID_VERTICES/2)

asteroids = []

def createAsteroidBelt():
    global asteroids
    asteroids = []
    for i in range(NUM_ASTEROIDS):
        x = math.floor(random.random() * WIDTH)
        y = math.floor(random.random() * HEIGHT)
        asteroids.append(Asteroid(x, y, ASTEROID_SIZE))

player = Player(WIDTH/2, HEIGHT/2, PLAYER_SIZE, 90)
screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption('Asteroids Neural Network')
font = pyg.font.Font('trench100free.ttf', 40)
text = font.render('SCORE:', True, TEXT_COLOR, BACKGROUND_COLOR)
game_over = False
createAsteroidBelt()

while not game_over:
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
    screen.fill(BACKGROUND_COLOR)
    if player.is_thrusting:
        player.thrust[0] += PLAYER_THRUST * math.cos(player.angle)
        player.thrust[1] -= PLAYER_THRUST * math.sin(player.angle)
        fire_tip = (player.pos[0] - 5/3 * player.radius * math.cos(player.angle), player.pos[1] + 5/3 * player.radius * math.sin(player.angle))
        fire_rear_left = (player.pos[0] - player.radius * (2/3 * math.cos(player.angle) + 0.5 * math.sin(player.angle)), player.pos[1] + player.radius * (2/3 * math.sin(player.angle) - 0.5 * math.cos(player.angle)))
        fire_rear_right = (player.pos[0] - player.radius * (2/3 * math.cos(player.angle) - 0.5 * math.sin(player.angle)), player.pos[1] + player.radius * (2/3 * math.sin(player.angle) + 0.5 * math.cos(player.angle)))
        ##### draw fire #####
        pyg.draw.polygon(screen, FIRE_FILL_COLOR, [fire_tip, fire_rear_left, fire_rear_right])
        pyg.draw.line(screen, FIRE_OUTLINE_COLOR, fire_tip, fire_rear_left, width=player.size//12)
        pyg.draw.line(screen, FIRE_OUTLINE_COLOR, fire_rear_left, fire_rear_right, width=player.size//12)
        pyg.draw.line(screen, FIRE_OUTLINE_COLOR, fire_tip, fire_rear_right, width=player.size//12)
    else:
        player.thrust[0] -= FRICTION * player.thrust[0]
        player.thrust[1] -= FRICTION * player.thrust[1]
    ##### draw player #####
    pyg.draw.line(screen, PLAYER_COLOR, player_tip, player_rear_left, width=player.size//15)
    pyg.draw.line(screen, PLAYER_COLOR, player_rear_left, player_rear_right, width=player.size//15)
    pyg.draw.line(screen, PLAYER_COLOR, player_tip, player_rear_right, width=player.size//15)

    ##### draw asteroids #####
    for ast in asteroids:
        for i in range(ast.vertices):
            start = (ast.pos[0] + ast.radius * math.cos(ast.angle + i * math.pi * 2 / ast.vertices), ast.pos[1] + ast.radius * math.sin(ast.angle + i * math.pi * 2 / ast.vertices))
            if i == ast.vertices - 1:
                end = (ast.pos[0] + ast.radius * math.cos(ast.angle), ast.pos[1] + ast.radius * math.sin(ast.angle))
            else:
                end = (ast.pos[0] + ast.radius * math.cos(ast.angle + (i + 1) * math.pi * 2 / ast.vertices), ast.pos[1] + ast.radius * math.sin(ast.angle + (i + 1) * math.pi * 2 / ast.vertices))
            pyg.draw.line(screen, ASTEROID_COLOR, start, end, width=player.size//15)

    ##### centroid check test #####
    # pyg.draw.rect(screen, TEXT_COLOR, (player.pos[0]-1, player.pos[1]-1, 2, 2))
    ###############################
    player.angle += player.rotation
    player.pos[0] += player.thrust[0]
    player.pos[1] += player.thrust[1]
    ##### back on screen when gone off screen #####
    if player.pos[0] < -player.radius:
        player.pos[0] = WIDTH + player.radius
    elif player.pos[0] > WIDTH + player.radius:
        player.pos[0] = -player.radius
    if player.pos[1] < -player.radius:
        player.pos[1] = HEIGHT + player.radius
    elif player.pos[1] > HEIGHT + player.radius:
        player.pos[1] = -player.radius
    screen.blit(text, TEXT_POS)
    pyg.display.flip()
