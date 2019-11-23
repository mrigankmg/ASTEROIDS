import sys
import pygame as pyg
import math
from pygame.math import Vector2

pyg.init()

class Player:
  def __init__(self, x, y, size, angle):
    self.pos = [x, y]
    self.size = size
    self.radius = size/2
    self.angle = angle
    self.rotation = 0
    self.is_thrusting = False
    self.thrust = [0, 0]

WIDTH = 1280
HEIGHT = 720
BACKGROUND_COLOR = (0, 0, 0) #Black
TEXT_COLOR = (255, 255, 255) #White
PLAYER_COLOR = (245, 66, 66) #Red
FIRE_FILL_COLOR = (255, 202, 54) #Yellow
FIRE_OUTLINE_COLOR = (255, 136, 0) #Orange
TEXT_POS = (88, 32)
player = Player(WIDTH/2, HEIGHT/2, 40, math.radians(90))
TURN_SPEED = math.radians(10)
PLAYER_THRUST = 0.1 #acceleration of ship in px/s
FRICTION = 0.01

screen = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption('Asteroids Neural Network')
font = pyg.font.Font('trench100free.ttf', 40)
text = font.render('SCORE:', True, TEXT_COLOR, BACKGROUND_COLOR)
textRect = text.get_rect()
textRect.center = (TEXT_POS[0], TEXT_POS[1])
game_over = False

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
    screen.blit(text, textRect)
    pyg.display.flip()
